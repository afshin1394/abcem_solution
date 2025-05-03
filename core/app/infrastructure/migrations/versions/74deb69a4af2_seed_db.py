"""seed_db

Revision ID: 74deb69a4af2
Revises: 761b94c6004b
Create Date: 2025-03-25 05:03:54.210273

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.domain.enums.base_config_enum import BaseConfigEnum
from app.domain.enums.complaint_type_enum import ComplaintTypeEnum
from app.domain.enums.problematic_service_enum import ProblematicServiceEnum
from app.domain.enums.service_type_enum import ServiceTypeEnum
from app.domain.enums.step_test_type_enum import StepTestTypeEnum
from app.domain.enums.technology_enum import TechnologyEnum
from app.domain.enums.walk_test_state_enum import WalkTestStatusEnum

# revision identifiers, used by Alembic.
revision: str = '74deb69a4af2'
down_revision: Union[str, None] = '761b94c6004b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



# Define Tables
table_technology_type = sa.table(
    "table_technology_type",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String)
)

table_walk_test_status = sa.table(
    "table_walk_test_status",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String)
)

table_complaint_type = sa.table(
    "table_complaint_type",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String)
)

table_problematic_service = sa.table(
    "table_problematic_service",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String)
)

table_step_type = sa.table(
    "table_step_test_type",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String)
)

table_service_type = sa.table(
    "table_service_type",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String)
)

table_base_config = sa.table(
    "table_base_config",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String),
    sa.column("value", sa.String),
    sa.column("scale", sa.String)
)

def upgrade() -> None:
    # Convert Enum to dictionary format
    technology_data = [{"id": tech.value, "name": tech.name} for tech in TechnologyEnum]
    walk_test_status_data = [{"id": state.value, "name": state.name} for state in WalkTestStatusEnum]
    complaint_type_data = [{"id": complaint_type.value, "name": complaint_type.name} for complaint_type in ComplaintTypeEnum]
    problematic_service_data = [{"id": service.value, "name": service.name} for service in ProblematicServiceEnum]
    step_type_data = [{"id": step.value, "name": step.name} for step in StepTestTypeEnum]
    service_type_data = [{"id": service_type.value, "name": service_type.name} for service_type in ServiceTypeEnum]


    # Insert data into tables
    op.bulk_insert(table_technology_type, technology_data)
    op.bulk_insert(table_walk_test_status, walk_test_status_data)
    op.bulk_insert(table_complaint_type, complaint_type_data)
    op.bulk_insert(table_problematic_service, problematic_service_data)
    op.bulk_insert(table_step_type, step_type_data)
    op.bulk_insert(table_service_type,service_type_data)
    op.bulk_insert(
        table_base_config,
        [
            {'name': BaseConfigEnum.WALK_TEST_LOCATION_OFFSET.value, 'value': '50','scale' : 'meter'},
            {'name': BaseConfigEnum.WALK_TEST_VALIDATION_DURATION.value, 'value': '300','scale' : 'seconds'},
        ]
    )


def downgrade() -> None:
    pass
    # conn = op.get_bind()
    #
    # # Step 1: Drop Foreign Key Constraints
    # conn.execute(text("ALTER TABLE table_walk_test DROP CONSTRAINT table_walk_test_technology_type_id_fkey"))
    # conn.execute(text("ALTER TABLE table_walk_test DROP CONSTRAINT table_walk_test_walk_test_status_id_fkey"))
    # conn.execute(text("ALTER TABLE table_walk_test DROP CONSTRAINT table_walk_test_complaint_type_id_fkey"))
    # conn.execute(text("ALTER TABLE table_walk_test DROP CONSTRAINT table_walk_test_problematic_service_id_fkey"))
    # conn.execute(text("ALTER TABLE table_walk_test DROP CONSTRAINT table_walk_test_service_type_id_fkey"))
    #
    # # Step 2: Nullify Foreign Key References
    # conn.execute(text("UPDATE table_walk_test SET technology_type_id = NULL"))
    # conn.execute(text("UPDATE table_walk_test SET walk_test_status_id = NULL"))
    # conn.execute(text("UPDATE table_walk_test SET complaint_type_id = NULL"))
    # conn.execute(text("UPDATE table_walk_test SET problematic_service_id = NULL"))
    # conn.execute(text("UPDATE table_walk_test SET service_type_id = NULL"))
    #
    # # Step 3: Delete from Enum-Related Tables
    # conn.execute(text("DELETE FROM table_technology_type"))
    # conn.execute(text("DELETE FROM table_walk_test_status"))
    # conn.execute(text("DELETE FROM table_complaint_type"))
    # conn.execute(text("DELETE FROM table_problematic_service"))
    # conn.execute(text("DELETE FROM table_step_test_type"))
    # conn.execute(text("DELETE FROM table_service_type"))
    #
    # # Step 4: Restore Foreign Key Constraints
    # conn.execute(text("""
    #     ALTER TABLE table_walk_test
    #     ADD CONSTRAINT table_walk_test_technology_type_id_fkey
    #     FOREIGN KEY (technology_type_id)
    #     REFERENCES table_technology_type(id)
    #     ON DELETE SET NULL
    # """))
    #
    # conn.execute(text("""
    #     ALTER TABLE table_walk_test
    #     ADD CONSTRAINT table_walk_test_walk_test_status_id_fkey
    #     FOREIGN KEY (walk_test_status_id)
    #     REFERENCES table_walk_test_status(id)
    #     ON DELETE SET NULL
    # """))
    #
    # conn.execute(text("""
    #     ALTER TABLE table_walk_test
    #     ADD CONSTRAINT table_walk_test_complaint_type_id_fkey
    #     FOREIGN KEY (complaint_type_id)
    #     REFERENCES table_complaint_type(id)
    #     ON DELETE SET NULL
    # """))
    #
    # conn.execute(text("""
    #     ALTER TABLE table_walk_test
    #     ADD CONSTRAINT table_walk_test_problematic_service_id_fkey
    #     FOREIGN KEY (problematic_service_id)
    #     REFERENCES table_problematic_service(id)
    #     ON DELETE SET NULL
    # """))
    #
    # conn.execute(text("""
    #     ALTER TABLE table_walk_test
    #     ADD CONSTRAINT table_walk_test_service_type_id_fkey
    #     FOREIGN KEY (service_type_id)
    #     REFERENCES table_service_type(id)
    #     ON DELETE SET NULL
    # """))


