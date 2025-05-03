"""init_db

Revision ID: 761b94c6004b
Revises: 
Create Date: 2025-03-25 05:03:36.212621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '761b94c6004b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:


    # Step 2: Now create your tables normally

    op.create_table(
        'table_base_config',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('value', sa.String(), nullable=False),
        sa.Column('scale', sa.String(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("timezone('Asia/Tehran', now())"),
                  nullable=True),
        schema='core_service',
    )
    op.create_table('table_complaint_type',
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='core_service',

                    )
    op.create_table('table_problematic_service',
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='core_service',

                    )
    op.create_table('table_service_type',
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='core_service',

                    )
    op.create_table(
        'table_speed_test_servers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('sponsor', sa.String(), nullable=True),
        sa.Column('country', sa.String(), nullable=True),
        sa.Column('lat', sa.String(), nullable=True),
        sa.Column('lon', sa.String(), nullable=True),
        sa.Column('distance', sa.Float(), nullable=True),
        sa.Column('host', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("timezone('Asia/Tehran', now())"),
                  nullable=True),
        schema='core_service',

    )
    op.create_table('table_step_test_type',
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
    schema = 'core_service',

    )
    op.create_table('table_technology_type',
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='core_service',

                    )
    op.create_table('table_walk_test_status',
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='core_service',

                    )
    op.create_table('table_walk_test',
                    sa.Column('ref_id', sa.String(), nullable=True),
                    sa.Column('province', sa.String(), nullable=True),
                    sa.Column('region', sa.String(), nullable=True),
                    sa.Column('city', sa.String(), nullable=True),
                    sa.Column('is_village', sa.Boolean(), nullable=True),
                    sa.Column('latitude', sa.Float(), nullable=True),
                    sa.Column('longitude', sa.Float(), nullable=True),
                    sa.Column('serving_cell', sa.String(), nullable=True),
                    sa.Column('serving_site', sa.String(), nullable=True),
                    sa.Column('is_at_all_hours', sa.Boolean(), nullable=True),
                    sa.Column('start_time_of_issue', sa.Time(), nullable=True),
                    sa.Column('end_time_of_issue', sa.Time(), nullable=True),
                    sa.Column('times_of_day', sa.String(), nullable=True),
                    sa.Column('msisdn', sa.String(), nullable=True),
                    sa.Column('related_tt', sa.String(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
                    sa.Column('technology_type_id', sa.Integer(), nullable=False),
                    sa.Column('complaint_type_id', sa.Integer(), nullable=False),
                    sa.Column('problematic_service_id', sa.Integer(), nullable=False),
                    sa.Column('service_type_id', sa.Integer(), nullable=False),
                    sa.Column('walk_test_status_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.Column('entered_at', sa.TIMESTAMP(timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(['complaint_type_id'], ['table_complaint_type.id'], ),
                    sa.ForeignKeyConstraint(['problematic_service_id'], ['table_problematic_service.id'], ),
                    sa.ForeignKeyConstraint(['service_type_id'], ['table_service_type.id'], ),
                    sa.ForeignKeyConstraint(['technology_type_id'], ['table_technology_type.id'], ),
                    sa.ForeignKeyConstraint(['walk_test_status_id'], ['table_walk_test_status.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('ref_id'),
                    schema='core_service',

                    )
    op.create_table('table_device_info',
                    sa.Column('security_patch', sa.DateTime(), nullable=False),
                    sa.Column('sdk', sa.Integer(), nullable=False),
                    sa.Column('os_version', sa.Integer(), nullable=False),
                    sa.Column('brand', sa.String(), nullable=False),
                    sa.Column('device', sa.String(), nullable=False),
                    sa.Column('hardware', sa.String(), nullable=False),
                    sa.Column('model', sa.String(), nullable=False),
                    sa.Column('walk_test_id', sa.String(), nullable=False),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.ForeignKeyConstraint(['walk_test_id'], ['table_walk_test.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    schema = 'core_service',

    )
    op.create_table('table_walk_test_detail',
                    sa.Column('step_number', sa.Integer(), nullable=True),
                    sa.Column('step_type_id', sa.Integer(), nullable=True),
                    sa.Column('walk_test_id', sa.String(), nullable=False),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.ForeignKeyConstraint(['step_type_id'], ['table_step_test_type.id'], ),
                    sa.ForeignKeyConstraint(['walk_test_id'], ['table_walk_test.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    schema='core_service',

                    )
    op.create_table('table_call_test',
                    sa.Column('drop_call', sa.Integer(), nullable=False),
                    sa.Column('is_voltE', sa.Boolean(), nullable=False),
                    sa.Column('technology_id', sa.Integer(), nullable=False),
                    sa.Column('walk_test_detail_id', sa.String(), nullable=False),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.ForeignKeyConstraint(['technology_id'], ['table_technology_type.id'], ),
                    sa.ForeignKeyConstraint(['walk_test_detail_id'], ['table_walk_test_detail.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    schema='core_service',

                    )
    op.create_table('table_cell_info',
                    sa.Column('cell_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
                    sa.Column('level', sa.Integer(), nullable=True),
                    sa.Column('quality', sa.Integer(), nullable=True),
                    sa.Column('walk_test_detail_id', sa.String(), nullable=True),
                    sa.Column('technology_id', sa.Integer(), nullable=True),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.ForeignKeyConstraint(['technology_id'], ['table_technology_type.id'], ),
                    sa.ForeignKeyConstraint(['walk_test_detail_id'], ['table_walk_test_detail.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    schema='core_service',

                    )
    op.create_table('table_speed_test_results',
                    sa.Column('download', sa.Float(), nullable=False),
                    sa.Column('upload', sa.Float(), nullable=False),
                    sa.Column('ping', sa.Float(), nullable=False),
                    sa.Column('jitter', sa.Float(), nullable=False),
                    sa.Column('technology_id', sa.Integer(), nullable=True),
                    sa.Column('walk_test_detail_id', sa.String(), nullable=True),
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("timezone('Asia/Tehran', now())"), nullable=True),
                    sa.ForeignKeyConstraint(['technology_id'], ['table_technology_type.id'], ),
                    sa.ForeignKeyConstraint(['walk_test_detail_id'], ['table_walk_test_detail.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    schema='core_service',

                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('table_speed_test_results')
    op.drop_table('table_cell_info')
    op.drop_table('table_call_test')
    op.drop_table('table_walk_test_detail')
    op.drop_table('table_device_info')
    op.drop_table('table_walk_test')
    op.drop_table('table_walk_test_status')
    op.drop_table('table_technology_type')
    op.drop_table('table_step_test_type')
    op.drop_table('table_speed_test_servers')
    op.drop_table('table_service_type')
    op.drop_table('table_problematic_service')
    op.drop_table('table_complaint_type')
    op.drop_table('table_base_config')

    # ### end Alembic commands ###
