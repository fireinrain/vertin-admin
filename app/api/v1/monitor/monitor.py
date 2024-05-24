from datetime import datetime

from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.monitor import monitor_controller,monitorset_controller
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
                                                     order=["report_time", "id"])
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
