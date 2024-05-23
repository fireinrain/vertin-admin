from app.core.crud import CRUDBase
from app.models.admin import Monitor, MonitorSet
from app.schemas.monitor import MonitorCreate, MonitorUpdate, MonitorSetCreate, MonitorSetUpdate


class MonitorController(CRUDBase[Monitor, MonitorCreate, MonitorUpdate]):
    def __init__(self):
        super().__init__(model=Monitor)


monitor_controller = MonitorController()


class MonitorSetController(CRUDBase[MonitorSet, MonitorSetCreate, MonitorSetUpdate]):
    def __init__(self):
        super().__init__(model=MonitorSet)


monitorset_controller = MonitorSetController()
