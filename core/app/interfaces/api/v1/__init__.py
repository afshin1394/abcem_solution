from fastapi import APIRouter

from app.interfaces.api.v1.endpoints.validation import router_v1 as validation_router
from app.interfaces.api.v1.endpoints.authentication import router_v1 as authentication_router
from app.interfaces.api.v1.endpoints.walk_test import router_v1 as walk_test_router
from app.interfaces.api.v1.endpoints.technology_type import router_v1 as technology_router
from app.interfaces.api.v1.endpoints.complaint_type import router_v1 as complaint_router
from app.interfaces.api.v1.endpoints.service_type import router_v1 as service_type_router
from app.interfaces.api.v1.endpoints.test_step_type import router_v1 as test_step_type_router
from app.interfaces.api.v1.endpoints.device_info import router_v1 as device_info_router
from app.interfaces.api.v1.endpoints.speed_test import router_v1 as speed_test_router
from app.interfaces.api.v1.endpoints.health_check import router_v1 as health_checker_router


router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(validation_router)
router_v1.include_router(authentication_router)
router_v1.include_router(walk_test_router)
router_v1.include_router(technology_router)
router_v1.include_router(complaint_router)
router_v1.include_router(service_type_router)
router_v1.include_router(test_step_type_router)
router_v1.include_router(device_info_router)
router_v1.include_router(speed_test_router)
router_v1.include_router(health_checker_router)
