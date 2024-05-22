from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.monitor import monitor_controller
from app.schemas import Success, SuccessExtra
from app.schemas.monitor import *

router = APIRouter()


@router.get("/monitor", summary="查看监控数据")
async def list_api(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    sn: str = Query(None, description="SN号码"),
    start_time: str = Query(None, description="记录起始时间"),
    end_time: str = Query(None, description="记录结束时间"),
):
    q = Q()
    if sn:
        q &= Q(sn__contains=sn)
    if start_time:
        q &= Q(start_time__contains=start_time)
    if end_time:
        q &= Q(end_time__contains=end_time)
    total, api_objs = await monitor_controller.list(page=page, page_size=page_size, search=q, order=["report_time", "id"])
    data = [await obj.to_dict() for obj in api_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看监控数据")
async def get_api(
    monitor_id: int = Query(..., description="Monitor Record Id"),
):
    api_obj = await monitor_controller.get(id=monitor_id)
    data = await api_obj.to_dict()
    return Success(data=data)


@router.post("/create", summary="新建监控数据")
async def create_api(
    monitor_in: MonitorCreate,
):
    await monitor_controller.create(obj_in=monitor_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新监控数据")
async def update_api(
    monitor_in: MonitorUpdate,
):
    await monitor_controller.update(id=monitor_in.id, obj_in=monitor_in.update_dict())
    return Success(msg="Update Successfully")


@router.delete("/delete", summary="删除监控数据")
async def delete_api(
    monitor_id: int = Query(..., description="监控记录ID"),
):
    await monitor_controller.remove(id=monitor_id)
    return Success(msg="Deleted Success")

