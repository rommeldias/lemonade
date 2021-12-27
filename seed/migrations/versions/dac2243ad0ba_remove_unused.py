"""remove unused

Revision ID: dac2243ad0ba
Revises: 6b631acda388
Create Date: 2021-09-22 18:06:07.595184

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dac2243ad0ba'
down_revision = '6b631acda388'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('traceability')
    op.create_index(op.f('ix_client_deployment_id'), 'client', ['deployment_id'], unique=False)
    op.add_column('deployment', sa.Column('model_id', sa.Integer(), nullable=True))
    op.add_column('deployment', sa.Column('type', sa.Enum('MODEL', 'DASHBOARD', 'APP', name='DeploymentTypeEnumType'), nullable=False))
    op.add_column('deployment', sa.Column('replicas', sa.Integer(), nullable=False))
    op.add_column('deployment', sa.Column('request_memory', sa.String(length=200), nullable=False))
    op.add_column('deployment', sa.Column('limit_memory', sa.String(length=200), nullable=True))
    op.add_column('deployment', sa.Column('request_cpu', sa.Numeric(precision=10, scale=2), nullable=False))
    op.add_column('deployment', sa.Column('limit_cpu', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('deployment', sa.Column('extra_parameters', mysql.LONGTEXT(), nullable=True))
    op.add_column('deployment', sa.Column('input_spec', mysql.LONGTEXT(), nullable=True))
    op.add_column('deployment', sa.Column('output_spec', mysql.LONGTEXT(), nullable=True))
    op.alter_column('deployment', 'workflow_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.create_index(op.f('ix_deployment_image_id'), 'deployment', ['image_id'], unique=False)
    op.create_index(op.f('ix_deployment_target_id'), 'deployment', ['target_id'], unique=False)
    op.create_index(op.f('ix_deployment_log_deployment_id'), 'deployment_log', ['deployment_id'], unique=False)
    op.create_index(op.f('ix_deployment_metric_deployment_id'), 'deployment_metric', ['deployment_id'], unique=False)
    op.add_column('metric_value', sa.Column('deployment_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_metric_value_deployment_id'), 'metric_value', ['deployment_id'], unique=False)
    op.create_foreign_key('fk_metric_value_deployment_id', 'metric_value', 'deployment', ['deployment_id'], ['id'])
    op.drop_column('metric_value', 'tma_data')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('metric_value', sa.Column('tma_data', mysql.LONGTEXT(collation='utf8_unicode_ci'), nullable=True))
    op.drop_constraint('fk_metric_value_deployment_id', 'metric_value', type_='foreignkey')
    op.drop_index(op.f('ix_metric_value_deployment_id'), table_name='metric_value')
    op.drop_column('metric_value', 'deployment_id')
    op.drop_index(op.f('ix_deployment_metric_deployment_id'), table_name='deployment_metric')
    op.drop_index(op.f('ix_deployment_log_deployment_id'), table_name='deployment_log')
    op.drop_index(op.f('ix_deployment_target_id'), table_name='deployment')
    op.drop_index(op.f('ix_deployment_image_id'), table_name='deployment')
    op.alter_column('deployment', 'workflow_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_column('deployment', 'output_spec')
    op.drop_column('deployment', 'input_spec')
    op.drop_column('deployment', 'extra_parameters')
    op.drop_column('deployment', 'limit_cpu')
    op.drop_column('deployment', 'request_cpu')
    op.drop_column('deployment', 'limit_memory')
    op.drop_column('deployment', 'request_memory')
    op.drop_column('deployment', 'replicas')
    op.drop_column('deployment', 'type')
    op.drop_column('deployment', 'model_id')
    op.drop_index(op.f('ix_client_deployment_id'), table_name='client')
    op.create_table('traceability',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('source_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('source_type', mysql.ENUM('DATA_SOURCE', 'WORKFLOW', 'JOB', 'DEPLOYMENT', 'MODEL'), nullable=False),
    sa.Column('target_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('target_type', mysql.ENUM('DATA_SOURCE', 'WORKFLOW', 'JOB', 'DEPLOYMENT', 'MODEL'), nullable=False),
    sa.Column('created', mysql.DATETIME(), nullable=False),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('user_login', mysql.VARCHAR(collation='utf8_unicode_ci', length=100), nullable=False),
    sa.Column('user_name', mysql.VARCHAR(collation='utf8_unicode_ci', length=100), nullable=False),
    sa.Column('context', mysql.VARCHAR(collation='utf8_unicode_ci', length=100), nullable=False),
    sa.Column('module', mysql.ENUM('PEEL', 'JUICER', 'LIMONERO', 'CITRUS', 'SEED', 'STAND', 'TAHITI'), nullable=False),
    sa.Column('action', mysql.ENUM('UNDEPLOY', 'DISPLAY_DATA', 'DEPLOY', 'SAVE_DATA', 'INFER_SCHEMA', 'DISPLAY_SCHEMA', 'SAVE_VISUALIZATION', 'CREATE_MODEL', 'APPLY_MODEL'), nullable=False),
    sa.Column('job_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('workflow_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('workflow_name', mysql.VARCHAR(collation='utf8_unicode_ci', length=250), nullable=True),
    sa.Column('task_id', mysql.VARCHAR(collation='utf8_unicode_ci', length=200), nullable=True),
    sa.Column('task_name', mysql.VARCHAR(collation='utf8_unicode_ci', length=200), nullable=True),
    sa.Column('task_type', mysql.VARCHAR(collation='utf8_unicode_ci', length=200), nullable=True),
    sa.Column('risk_score', mysql.FLOAT(), nullable=True),
    sa.Column('platform_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8_unicode_ci',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
