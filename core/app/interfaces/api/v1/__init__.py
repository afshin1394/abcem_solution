from fastapi import APIRouter

from app.interfaces.api.v1.endpoints.configurations import router_configs
from app.interfaces.api.v1.endpoints.health_check import router_health_check
from app.interfaces.api.v1.endpoints.speed_test import router_speed_test
from app.interfaces.api.v1.endpoints.walk_test import router_public as walk_test_public_router, router_walk_test
from app.interfaces.api.v1.endpoints.walk_test import router_private as walk_test_private_router
from app.interfaces.api.v1.endpoints.walk_test import router_protected as walk_test_protected_router

from app.interfaces.api.v1.endpoints.walk_test_results import router_public as walk_test_results_public_router, \
    router_walk_test_results
from app.interfaces.api.v1.endpoints.walk_test_results import router_private as walk_test_results_private_router
from app.interfaces.api.v1.endpoints.walk_test_results import router_protected as walk_test_results_protected_router


from app.interfaces.api.v1.endpoints.walk_test_results import router_private as walk_test_results_private_router
from app.interfaces.api.v1.endpoints.walk_test_results import router_protected as walk_test_results_protected_router



router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(router_configs)
router_v1.include_router(router_health_check)
router_v1.include_router(router_speed_test)
router_v1.include_router(router_walk_test)
router_v1.include_router(router_walk_test_results)

