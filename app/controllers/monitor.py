from app.core.crud import CRUDBase
from app.models.admin import Monitor
from app.schemas.monitor import MonitorCreate, MonitorUpdate


class MonitorController(CRUDBase[Monitor, MonitorCreate, MonitorUpdate]):
    def __init__(self):
        super().__init__(model=Monitor)


monitor_controller = MonitorController()
