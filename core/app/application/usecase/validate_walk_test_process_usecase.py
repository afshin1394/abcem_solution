
from app.application.feature.commands.update_entered_at_walk_test_command import UpdateEnteredAtWalkTestCommand
from app.application.feature.queries.check_entered_at_walk_test_query import CheckEnteredAtWalkTestQuery
from app.application.feature.queries.get_walk_test_coordinates_query import GetWalkTestCoordinatesQuery
from app.application.feature.queries.validate_walk_test_time_duration_query import ValidateWalkTestTimeDurationQuery
from app.application.mediator import Mediator
from app.application.usecase.base_use_case import BaseUseCase
from app.domain.exceptions import WalkTestTimeDurationExceeded, WalkTestLocationInvalid
from app.domain.services.gis_service import GISService
from app.interfaces.dto.request.validate_walk_test_process_request import ValidateWalkTestProcessRequest


class ValidateWalkTestProcessUseCase(BaseUseCase):

    def __init__(self, mediator: Mediator, gis_service: GISService):
        self.mediator = mediator
        self.gis_service = gis_service

    async def __execute__(self, **kwargs) -> bool:
        request = kwargs.get("validate_walk_test_process_request")
        if isinstance(request, ValidateWalkTestProcessRequest):

            is_time_duration_valid = await self.mediator.send(
                ValidateWalkTestTimeDurationQuery(walk_test_id=request.walk_test_id))
            print(f"is_time_duration_valid {is_time_duration_valid}")
            if is_time_duration_valid:
                coordinates = await self.mediator.send(
                    GetWalkTestCoordinatesQuery(walk_test_id=request.walk_test_id))

                print(f"coordinates {coordinates}")
                is_with_in = await self.gis_service.validate_location_within_offset(offset=50,
                                                                       walk_test_coords=coordinates,
                                                                       gps_coords=(
                                                                           request.gps_lat, request.gps_lon),
                                                                       user_input_coords=(
                                                                           request.map_lat, request.map_lon))
                print(f"is_with_in {is_with_in}")

                if is_with_in:
                    has_entered = await self.mediator.send(CheckEnteredAtWalkTestQuery(walk_test_id=request.walk_test_id))
                    print(f"has_entered {has_entered}")
                    if not has_entered:
                        await self.mediator.send(UpdateEnteredAtWalkTestCommand(walk_test_id=request.walk_test_id))
                    return is_with_in
                else:
                    raise WalkTestLocationInvalid()

            else:
                raise WalkTestTimeDurationExceeded()


        else:
            print("The argument is not of type 'validate_walk_test_process_request'")

        return False

