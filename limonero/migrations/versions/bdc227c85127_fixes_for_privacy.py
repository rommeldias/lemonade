"""fixes for privacy

Revision ID: bdc227c85127
Revises: c996f5e0b931
Create Date: 2017-07-05 09:33:05.837827

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from limonero.migration_utils import is_sqlite

# revision identifiers, used by Alembic.
revision = 'bdc227c85127'
down_revision = 'c996f5e0b931'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if is_sqlite():
        with op.batch_alter_table('data_source') as batch_op:
            batch_op.add_column(sa.Column('text_delimiter', sa.String(length=4), nullable=True))

        with op.batch_alter_table('attribute_privacy') as batch_op:
            batch_op.add_column(sa.Column('data_type', sa.Enum('ENUM', 'LAT_LONG', 'DOUBLE', 'DECIMAL', 'FLOAT', 'CHARACTER', 'LONG', 'DATETIME', 'VECTOR', 'TEXT', 'TIME', 'DATE', 'INTEGER', 'TIMESTAMP', name='DataTypeEnumType'), 
                nullable=True))
            batch_op.add_column(sa.Column('is_global_law', sa.Boolean(), nullable=True))

            batch_op.alter_column('attribute_id', nullable=True)
            batch_op.alter_column('category_model', nullable=True)
            batch_op.alter_column('category_technique', nullable=True)
            batch_op.alter_column('hierarchical_structure_type', nullable=True)
            batch_op.alter_column('hierarchy', nullable=True)
            batch_op.alter_column('privacy_model', nullable=True)
            batch_op.alter_column('privacy_model_parameters', nullable=True)
            batch_op.alter_column('privacy_model_technique', nullable=True)
            batch_op.alter_column('unlock_privacy_key', nullable=True)

    else:
        op.add_column('data_source', sa.Column('text_delimiter', sa.String(length=4), nullable=True))
        op.add_column('attribute_privacy', sa.Column('data_type', sa.Enum('ENUM', 'LAT_LONG', 'DOUBLE', 'DECIMAL', 'FLOAT', 'CHARACTER', 'LONG', 'DATETIME', 'VECTOR', 'TEXT', 'TIME', 'DATE', 'INTEGER', 'TIMESTAMP', name='DataTypeEnumType'), nullable=True))
        op.add_column('attribute_privacy', sa.Column('is_global_law', sa.Boolean(), nullable=True))

        op.alter_column('attribute_privacy', 'attribute_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
        op.alter_column('attribute_privacy', 'category_model',
               existing_type=mysql.TEXT(),
               nullable=True)
        op.alter_column('attribute_privacy', 'category_technique',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        op.alter_column('attribute_privacy', 'hierarchical_structure_type',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        op.alter_column('attribute_privacy', 'hierarchy',
               existing_type=mysql.TEXT(),
               nullable=True)
        op.alter_column('attribute_privacy', 'privacy_model',
               existing_type=mysql.TEXT(),
               nullable=True)
        op.alter_column('attribute_privacy', 'privacy_model_parameters',
               existing_type=mysql.TEXT(),
               nullable=True)
        op.alter_column('attribute_privacy', 'privacy_model_technique',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        op.alter_column('attribute_privacy', 'unlock_privacy_key',
               existing_type=mysql.VARCHAR(length=400),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if is_sqlite():
        with op.batch_alter_table('data_source') as batch_op:
            batch_op.drop_column('text_delimiter')

        with op.batch_alter_table('attribute_privacy') as batch_op:
            batch_op.drop_column('data_type')
            batch_op.drop_column('is_global_law')

            batch_op.alter_column('attribute_id', nullable=False, server_default='')
            batch_op.alter_column('category_model', nullable=False, server_default='')
            batch_op.alter_column('category_technique', nullable=False, server_default='')
            batch_op.alter_column('hierarchical_structure_type', nullable=False, server_default='')
            batch_op.alter_column('hierarchy', nullable=False, server_default='')
            batch_op.alter_column('privacy_model', nullable=False, server_default='')
            batch_op.alter_column('privacy_model_parameters', nullable=False, server_default='')
            batch_op.alter_column('privacy_model_technique', nullable=False, server_default='')
            batch_op.alter_column('unlock_privacy_key', nullable=False, server_default='')

    else:
        op.drop_column('data_source', 'text_delimiter')
        op.alter_column('attribute_privacy', 'unlock_privacy_key',
                   existing_type=mysql.VARCHAR(length=400),
                   nullable=False)
        op.alter_column('attribute_privacy', 'privacy_model_technique',
                   existing_type=mysql.VARCHAR(length=100),
                   nullable=False)
        op.alter_column('attribute_privacy', 'privacy_model_parameters',
                   existing_type=mysql.TEXT(),
                   nullable=False)
        op.alter_column('attribute_privacy', 'privacy_model',
                   existing_type=mysql.TEXT(),
                   nullable=False)
        op.alter_column('attribute_privacy', 'hierarchy',
                   existing_type=mysql.TEXT(),
                   nullable=False)
        op.alter_column('attribute_privacy', 'hierarchical_structure_type',
                   existing_type=mysql.VARCHAR(length=100),
                   nullable=False)
        op.alter_column('attribute_privacy', 'category_technique',
                   existing_type=mysql.VARCHAR(length=100),
                   nullable=False)
        op.alter_column('attribute_privacy', 'category_model',
                   existing_type=mysql.TEXT(),
                   nullable=False)
        op.alter_column('attribute_privacy', 'attribute_id',
                   existing_type=mysql.INTEGER(display_width=11),
                   nullable=False)
        op.drop_column('attribute_privacy', 'is_global_law')
        op.drop_column('attribute_privacy', 'data_type')
    # ### end Alembic commands ###
