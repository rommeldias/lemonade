"""new attributes for privacy

Revision ID: c996f5e0b931
Revises: 9dccb02d8201
Create Date: 2017-07-04 10:46:02.417305

"""
from alembic import op
import sqlalchemy as sa
from limonero.migration_utils import is_sqlite


# revision identifiers, used by Alembic.
revision = 'c996f5e0b931'
down_revision = '9dccb02d8201'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    if is_sqlite():
        with op.batch_alter_table('attribute_privacy') as batch_op:
            batch_op.add_column(sa.Column('attribute_name', sa.String(length=200), nullable=False, server_default=''))
    else:
        op.add_column('attribute_privacy', sa.Column('attribute_name', sa.String(length=200), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    if is_sqlite():
        with op.batch_alter_table('attribute_privacy') as batch_op:
            batch_op.drop_column('attribute_name')
    else:
        op.drop_column('attribute_privacy', 'attribute_name')
    # ### end Alembic commands ###