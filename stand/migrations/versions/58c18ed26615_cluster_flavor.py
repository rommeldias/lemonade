"""Cluster flavor

Revision ID: 58c18ed26615
Revises: 03dbc173d79a
Create Date: 2019-07-10 09:56:35.764441

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql
from stand.migration_utils import (is_mysql, get_psql_enum_alter_commands,
        upgrade_actions, downgrade_actions, is_psql)
# revision identifiers, used by Alembic.
revision = '58c18ed26615'
down_revision = '03dbc173d79a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if is_mysql():
        parameters_col = sa.Column('parameters', mysql.LONGTEXT(), nullable=False)

        op.execute("ALTER TABLE `stand`.`job_result` CHANGE `type` `type` "
               "ENUM('VISUALIZATION','HTML','TEXT','OTHER','MODEL','METRIC')")
    else:
        parameters_col = sa.Column('parameters', sa.Text(), nullable=False)

        values = ['VISUALIZATION','HTML','TEXT','OTHER','MODEL','METRIC']
        all_commands = [[get_psql_enum_alter_commands(['job_result'], ['type'],
            'ResultTypeEnumType', values, 'TEXT'), 
            None]]


    op.create_table('cluster_flavor',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=200), nullable=False),
                    sa.Column('enabled', sa.String(length=200), nullable=False),
                    parameters_col,
                    sa.Column('cluster_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['cluster_id'], ['cluster.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cluster_flavor')
    # ### end Alembic commands ###
