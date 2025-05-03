import asyncio

import math

from app.domain.services.gis_service import GISService


class GISServiceImpl(GISService):
    # Function to calculate distance between two lat/lon points using Haversine formula
   @staticmethod
   async def __haversine__(lat1, lon1, lat2, lon2):
        # Radius of the Earth in meters
        R = 6371000

        # Convert degrees to radians
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        # Haversine formula
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Distance in meters
        distance = R * c
        return distance

        # Function to check if all locations provided as kwargs are within the offset

   async def validate_location_within_offset(self, offset=50, **coords):
        # Ensure we have at least two coordinates to compare
        if len(coords) < 2:
            raise ValueError("At least two coordinates are needed to perform distance checks.")

        # Convert the kwargs into a list of coordinates
        coords_list = list(coords.values())

        # Compare all pairs of coordinates in the list
        for i in range(len(coords_list)):
            for j in range(i + 1, len(coords_list)):
                distance = await self.__haversine__(coords_list[i][0], coords_list[i][1], coords_list[j][0], coords_list[j][1])
                if distance > offset:
                    return False
        return True


if __name__ == '__main__':
   print(asyncio.run( GISServiceImpl().validate_location_within_offset(
        offset=50,
        walk_test_coords=(44.748817, 72.985428),  # Walk Test Coordinates
        gps_coords=(44.748917, 72.985518),  # GPS Coordinates
        user_input_coords=(44.748617, 72.985328)  # User Input Coordinates
    )))
