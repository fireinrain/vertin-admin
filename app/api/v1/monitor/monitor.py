import httpx
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.monitor import monitor_controller, monitorset_controller
from app.core.bgtask import IntervalTaskScheduler
from app.log import logger
from app.models import MonitorSet
from app.schemas import Success, SuccessExtra
from app.schemas.monitor import *

router = APIRouter()


@router.get("/list", summary="查看监控数据")
async def list_monitor(
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量"),
        sn: str = Query(None, description="SN号码"),
        start_time: datetime = Query(None, description="记录起始时间"),
        end_time: datetime = Query(None, description="记录结束时间"),
):
    q = Q()
    if sn:
        q &= Q(sn__contains=sn)
    if start_time:
        q &= Q(start_time__gte=start_time)
    if end_time:
        q &= Q(end_time__lte=end_time)
    total, moni_objs = await monitor_controller.list(page=page, page_size=page_size, search=q,
                                                     order=["-report_time", "-id"])
    data = [await obj.to_dict() for obj in moni_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看监控数据")
async def get_monitor(
        monitor_id: int = Query(..., description="Monitor Record Id"),
):
    moni_obj = await monitor_controller.get(id=monitor_id)
    data = await moni_obj.to_dict()
    return Success(data=data)


@router.post("/create", summary="新建监控数据")
async def create_monitor(
        monitor_in: MonitorCreate,
):
    await monitor_controller.create(obj_in=monitor_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新监控数据")
async def update_monitor(
        monitor_in: MonitorUpdate,
):
    await monitor_controller.update(id=monitor_in.id, obj_in=monitor_in.update_dict())
    return Success(msg="Update Successfully")


@router.delete("/delete", summary="删除监控数据")
async def delete_monitor(
        monitor_id: int = Query(..., description="监控记录ID"),
):
    await monitor_controller.remove(id=monitor_id)
    return Success(msg="Deleted Success")


################################

@router.get("/capture/list", summary="查看监控配置列表")
async def capture_list_monitorset(
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量"),
        sn: str = Query(None, description="SN号码"),
        api_url: str = Query(None, description="api地址"),
        fetch_interval: int = Query(None, description="采集间隔"),
):
    q = Q()
    if sn:
        q &= Q(sn__contains=sn)
    if api_url:
        q &= Q(api_url__contains=api_url)
    if fetch_interval:
        q &= Q(fetch_interval=fetch_interval)
    total, moniset_objs = await monitorset_controller.list(page=page, page_size=page_size, search=q,
                                                           order=["sn", "id"])
    data = [await obj.to_dict() for obj in moniset_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/capture/get", summary="查看监控配置")
async def capture_get_monitorset(
        monitorset_id: int = Query(..., description="Monitor Record Id"),
):
    moniset_obj = await monitor_controller.get(id=monitorset_id)
    data = await moniset_obj.to_dict()
    return Success(data=data)


@router.post("/capture/create", summary="新建监控配置")
async def capture_create_monitorset(
        monitorset_in: MonitorSetCreate,
):
    await monitorset_controller.create(obj_in=monitorset_in)
    return Success(msg="Created Successfully")


@router.post("/capture/update", summary="更新监控设置")
async def capture_update_monitorset(
        monitorset_in: MonitorSetUpdate,
):
    await monitorset_controller.update(id=monitorset_in.id, obj_in=monitorset_in.update_dict())
    return Success(msg="Update Successfully")


@router.delete("/capture/delete", summary="删除监控设置")
async def capture_delete_monitorset(
        monitorset_id: int = Query(..., description="监控设置ID"),
):
    await monitorset_controller.remove(id=monitorset_id)
    return Success(msg="Deleted Success")


@router.post("/capture/refresh", summary="刷新后台监控任务")
async def capture_refresh_monitorset():
    q = Q()
    logger.info("Before capture_refresh_monitorset jobs status: ")
    IntervalTaskScheduler.print_jobs()
    monitor_sets = await monitorset_controller.model.filter(q).all()
    for m_set in monitor_sets:
        job = None
        try:
            job = IntervalTaskScheduler.get_job(str(m_set.id))
        except Exception as e:
            logger.info(f"Can not find job id of: {m_set.id},skip for cancel")
            continue
        if job:
            # Remove the job from the scheduler
            logger.info(f"Task ID: {m_set.id} is running, and do cancel for next check.")
            IntervalTaskScheduler.remove_job(str(m_set.id))
    # 重新加入定时任务
    refresh_q = Q(enable="true")
    monitor_sets = await monitorset_controller.model.filter(refresh_q).all()
    for m_set in monitor_sets:
        logger.info(f"定时任务已经刷新: {m_set}")
        interval_int = int(m_set.fetch_interval)
        IntervalTaskScheduler.add_job(fetch_monitor_data, IntervalTrigger(seconds=interval_int), id=str(m_set.id),
                                      args=[m_set])
    logger.info("After capture_refresh_monitorset jobs status: ")

    IntervalTaskScheduler.print_jobs()

    return Success(msg="OK")


async def fetch_monitor_data(m_set: MonitorSet):
    url = f"{m_set.api_url}?sn={m_set.sn}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/124.0.0.0 Safari/537.36'
    }
    # Corrected the query parameter syntax
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            text = response.text
            logger.error(f"Error fetching monitor data: {response.status_code}, {text}")
            return None
        logger.info(f"Job excute at: {datetime.now()}, url:{url}, response: {response.json()['data']}")

        data = response.json()['data']
        if isinstance(data, list):
            for d in data:
                sn = d.get('sn')
                content = d.get('content')
                report_time = d.get('reportTime')
                start_time = d.get('startTime')
                end_time = d.get('endTime')
                monitor_his = await monitor_controller.model.filter(sn=sn, content=content,
                                                                    report_time=report_time, start_time=start_time,
                                                                    end_time=end_time).exists()

                if not monitor_his:
                    logger.info(f"发现新监控记录,保存更新中...{d}")

                    await monitor_controller.create(MonitorCreate(
                        sn=d['sn'],
                        content=d['content'],
                        report_time=d['reportTime'],
                        start_time=d['startTime'],
                        end_time=d['endTime']
                    ))
        elif isinstance(data, dict):
            sn = data.get('sn')
            content = data.get('content')
            report_time = data.get('reportTime')
            start_time = data.get('startTime')
            end_time = data.get('endTime')
            monitor_his = await monitor_controller.model.filter(sn=sn, content=content,
                                                                report_time=report_time, start_time=start_time,
                                                                end_time=end_time).exists()

            if not monitor_his:
                logger.info(f"发现新监控记录,保存更新中...{data}")

                await monitor_controller.create(MonitorCreate(
                    sn=data['sn'],
                    content=data['content'],
                    report_time=data['reportTime'],
                    start_time=data['startTime'],
                    end_time=data['endTime']
                ))


@router.get("/dash/list", summary="监控设备列表")
async def dash_list_monitor(
        page: int = Query(1, description="页码"),
        page_size: int = Query(10, description="每页数量"),
):
    total = await monitorset_controller.model.all().distinct().values_list('sn', flat=False)
    total = len(total)
    moni_objs = await monitorset_controller.model.all().distinct().offset(
        (page - 1) * page_size).limit(page_size).limit(page_size).order_by('id').values_list('sn', flat=False)
    data = [{'sn': v[0], 'id': index} for index, v in enumerate(moni_objs)]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/dash/detail", summary="监控设备历史数据")
async def dash_hist_monitor(
        sn: str = Query(..., description="SN编码"),
):
    datas = await monitor_controller.model.filter(sn=sn).order_by("report_time").all()
    data = [await obj.to_dict() for obj in datas]

    return Success(data=data)
