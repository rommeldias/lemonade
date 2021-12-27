"""Change tables fields types.

Revision ID: cbf95b5e48c7
Revises: 3646db1b8453
Create Date: 2021-11-15 15:57:16.279802

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cbf95b5e48c7'
down_revision = '3646db1b8453'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('deployment', 'request_cpu',
               existing_type=mysql.DECIMAL(precision=10, scale=2),
               type_=sa.String(length=200),
               existing_nullable=False)
    op.alter_column('deployment', 'limit_cpu',
               existing_type=mysql.DECIMAL(precision=10, scale=2),
               type_=sa.String(length=200),
               existing_nullable=True)
    op.alter_column('deployment_target', 'authentication_info',
               existing_type=mysql.VARCHAR(length=500),
               type_=sa.String(length=2500),
               existing_nullable=True)
    op.alter_column('deployment_target', 'target_type',
               existing_type=mysql.ENUM('SUPERVISOR', 'KUBERNETES', 'DOCKER', 'MARATHON'),
               type_=sa.Enum('DOCKER', 'KUBERNETES', 'MARATHON', 'SUPERVISOR', name='DeploymentTypeEnumType'),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('deployment_target', 'target_type',
               existing_type=sa.Enum('DOCKER', 'KUBERNETES', 'MARATHON', 'SUPERVISOR', name='DeploymentTypeEnumType'),
               type_=mysql.ENUM('SUPERVISOR', 'KUBERNETES', 'DOCKER', 'MARATHON'),
               existing_nullable=False)
    op.alter_column('deployment_target', 'authentication_info',
               existing_type=sa.String(length=2500),
               type_=mysql.VARCHAR(length=500),
               existing_nullable=True)
    op.alter_column('deployment', 'limit_cpu',
               existing_type=sa.String(length=200),
               type_=mysql.DECIMAL(precision=10, scale=2),
               existing_nullable=True)
    op.alter_column('deployment', 'request_cpu',
               existing_type=sa.String(length=200),
               type_=mysql.DECIMAL(precision=10, scale=2),
               existing_nullable=False)
    # ### end Alembic commands ###
