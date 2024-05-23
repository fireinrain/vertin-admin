from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import MethodType


class BaseMonitor(BaseModel):
    sn: str = Field(..., description="SN编码", example="JX000001")
    content: str = Field("", description="监控数据", example="00100020001")
    report_time: datetime = Field(None, description="上报时间", example=1714039740000)
    start_time: datetime = Field(None, description="起始时间", example=1714039740000)
    end_time: datetime = Field(None, description="结束时间", example=1714039741000)


class MonitorCreate(BaseMonitor):
    ...


class MonitorUpdate(BaseMonitor):
    id: int

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})
