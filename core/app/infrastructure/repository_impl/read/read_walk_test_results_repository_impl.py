from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.walk_test_results_domain import WalkTestResultsDomain
from app.domain.repositories.read.read_walk_test_results_repository import ReadWalkTestResultsRepository




class ReadWalkTestResultsRepositoryImpl(ReadWalkTestResultsRepository):
    
    def __init__(self,db : AsyncSession):
        self.db = db

    async def get_walk_test_results_by_id(self, walk_test_id: str) -> list[WalkTestResultsDomain]:
        results = await self.db.execute(text("""
            SELECT 
                twtd.step_number, twtd.step_type_id, twtd.walk_test_id, twtd.id as walk_test_detail_id,
                tct.id as call_test_id, tct.drop_call, tct.technology_id, tct."is_voltE", 
                tci.id as cell_info_id, tci.cell_data, tci.level, tci.quality,
                tstr.id as speed_test_result_id, tstr.download, tstr.upload, tstr.ping, tstr.jitter, 
                tstr.technology_id as speed_test_result_technology_id
            FROM table_walk_test_detail AS twtd
            LEFT JOIN table_call_test AS tct ON twtd.id = tct.walk_test_detail_id
            LEFT JOIN table_cell_info AS tci ON twtd.id = tci.walk_test_detail_id
            LEFT JOIN table_speed_test_results AS tstr ON twtd.id = tstr.walk_test_detail_id
            WHERE twtd.walk_test_id = :walk_test_id  order by step_number
        """), {"walk_test_id": walk_test_id})

        rows = results.mappings().all()
        print("rows"+rows.__str__())

        # Manually map each row to a dataclass
        walk_test_results = [
            WalkTestResultsDomain(
                step_number=row['step_number'],
                step_type_id=row['step_type_id'],
                walk_test_id=row['walk_test_id'],
                walk_test_detail_id=row['walk_test_detail_id'],
                call_test_id=row.get('call_test_id'),
                drop_call=row.get('drop_call'),
                technology_id=row.get('technology_id'),
                is_voltE=row.get('is_voltE'),
                cell_info_id=row['cell_info_id'],
                cell_data=row.get('cell_data'),
                level=row.get('level'),
                quality=row.get('quality'),
                speed_test_result_id=row.get('speed_test_result_id'),
                download=row.get('download'),
                upload=row.get('upload'),
                ping=row.get('ping'),
                jitter=row.get('jitter'),
                speed_test_result_technology_id=row.get('speed_test_result_technology_id'),
            )
            for row in rows
        ]
        print("walk_test_results"+walk_test_results.__str__())
        return walk_test_results
