
from app.infrastructure.services_impl.speed_test_servers import Speedtest

async def get_speed_test() -> Speedtest:
    return Speedtest()


