""" new visualizations 2020  

Revision ID: 437ffc36a821
Revises: d73f1a3bccf3
Create Date: 2020-07-16 19:48:01.228630

"""
from alembic import op
from sqlalchemy import String, Integer
from sqlalchemy.sql import table, column, text
from caipirinha.migration_utils import get_enable_disable_fk_command

# revision identifiers, used by Alembic.
revision = '437ffc36a821'
down_revision = 'd73f1a3bccf3'
branch_labels = None
depends_on = None


def insert_visualization_type():
    tb = table(
        'visualization_type',
        column('id', Integer),
        column('name', String),
        column('help', String),
        column('icon', String))

    all_ops = [
        (130, 'indicator', 'Gauge', 'fa-chart'),                              
        (131, 'markdown', 'Markdown text', 'fa-chart'),                       
        (132, 'word-cloud', 'Word cloud', 'fa-chart'),                        
        (133, 'heatmap', 'Heatmap', 'fa-chart'),                              
        (134, 'bubble-chart', 'Bubble chart', 'fa-chart'),                    
        (135, 'force-direct', 'Network graphs', 'fa-chart'),                  
        (136, 'iframe', 'HTML iframe', 'fa-chart'),                           
        (137, 'treemap', 'Treemap', 'fa-chart'),
    ]
    rows = [dict(zip([c.name for c in tb.columns], operation)) for operation in
            all_ops]

    op.bulk_insert(tb, rows)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    try:
        op.execute(text('BEGIN'))
        insert_visualization_type()
        op.execute(text('COMMIT'))
    except:
        op.execute(text('ROLLBACK'))
        raise


# noinspection PyBroadException
def downgrade():
    try:
        op.execute(text('BEGIN'))
        op.execute(text(get_enable_disable_fk_command(False)))
        op.execute(
            text("DELETE FROM visualization WHERE type_id IN (123, 124)"))
        op.execute(
            text("DELETE FROM visualization_type WHERE id IN (123, 124)"))
        op.execute(text(get_enable_disable_fk_command(True)))
        op.execute(text('COMMIT'))
    except:
        op.execute(text('ROLLBACK'))
        raise
