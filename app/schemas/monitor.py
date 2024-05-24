from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# 监控历史数据
class BaseMonitor(BaseModel):
    sn: str = Field(..., description="SN编码", example="JX000001")
    content: str = Field("", description="监控数据", example="00100020001")
    report_time: int = Field(None, description="上报时间", example=1714039740000)
    start_time: Optional[int] = Field(None, description="起始时间", example=1714039740000)
    end_time: Optional[int] = Field(None, description="结束时间", example=1714039741000)


class MonitorCreate(BaseMonitor):
    ...


class MonitorUpdate(BaseMonitor):
    id: int

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


# 监控采集设置
class BaseMonitorSet(BaseModel):
    sn: str = Field(..., description="SN编码", example="JX000001")
    api_url: str = Field("", description="监控数据地址", example="https://example.com")
    fetch_interval: int = Field(30, description="采集间隔")
    enable: str = Field("true", description="是否开启")


class MonitorSetCreate(BaseMonitorSet):
    ...


class MonitorSetUpdate(BaseMonitorSet):
    id: int

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})
