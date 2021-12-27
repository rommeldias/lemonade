"""mpce

Revision ID: 6f7a506d4afb
Revises: a73c21a49894
Create Date: 2021-04-12 16:07:19.217622

"""
from alembic import op
import sqlalchemy as sa
from alembic import context
from alembic import op
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import table, column, text
import json



# revision identifiers, used by Alembic.
revision = '90ffa76be3a2'
down_revision = 'a85dce88d899'
branch_labels = None
depends_on = None


def _insert_operation_category_translation():
    tb = table(
        'operation_category_translation',
        column('id', Integer),
        column('locale', String),
        column('name', String))

    columns = ('id', 'locale', 'name')
    data = [
        (9001, 'en', 'Computer Vision'),
        (9001, 'pt', 'Visão Computacional'),
    ]
    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)


def _insert_operation_category():
    operation_category_table = table('operation_category',
                                     column("id", Integer),
                                     column('type', String),
                                     column("order", Integer),
                                     column("default_order", Integer)
                                     )
    columns = ['id', 'type', 'order', 'default_order']
    all_categories = [
        (9001, 'group', 0, 0),
    ]
    rows = [dict(list(zip(columns, cat))) for cat in all_categories]

    op.bulk_insert(operation_category_table, rows)

def _insert_operation():
    tb = table('operation',
               column("id", Integer),
               column("slug", String),
               column('enabled', Integer),
               column('type', String),
               column('icon', String),
               )
    columns = ['id', 'slug', 'enabled', 'type', 'icon']
    data = [
        (9001, 'read-image-folder', 1, 'TRANSFORMATION', 'fa-filter'),
        (9002, 'extract-faces', 1, 'TRANSFORMATION', 'fa-filter'),
        (9003, 'extract-face-features', 1, 'TRANSFORMATION', 'fa-filter'),
        (9004, 'chinese-whispers-clustering', 1, 'TRANSFORMATION', ''),
        (9005, 'image-view', 1, 'VISUALIZATION', ''),
    ]

    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

def _insert_operation_platform():
    tb = table(
        'operation_platform',
        column('operation_id', Integer),
        column('platform_id', Integer))

    columns = ('operation_id', 'platform_id')
    data = [
        (9001, 4), #Sklearn Platform
        (9002, 4), #Sklearn Platform
        (9003, 4),
        (9004, 4),
        (9005, 4),
    ]
    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

def _insert_operation_category_operation():
    tb = table(
        'operation_category_operation',
        column('operation_id', Integer),
        column('operation_category_id', Integer))

    columns = ('operation_id', 'operation_category_id')
    data = [
        (9001, 9001),
        (9002, 9001),
        (9003, 9001),
        (9004, 9001),
        (9005, 9001),
    ]

    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

def _insert_operation_translation():
    tb = table(
        'operation_translation',
        column('id', Integer),
        column('locale', String),
        column('name', String),
        column('description', String), )

    columns = ('id', 'locale', 'name', 'description')
    data = [
        (9001, 'en', 'Read Image Folder',
         'List all images inside the folder.'),
        (9001, 'pt', 'Ler Pasta de Imagem',
         'Lista todas as imagens contidas na pasta.'),
        (9002, 'en', 'Extract Faces',
         'Extract faces from images.'),
        (9002, 'pt', 'Extrair faces',
         'Extrair faces de imagens.'),
        (9003, 'en', 'Extract Face Features',
         'Extract face features from images.'),
        (9003, 'pt', 'Extrair características da face',
         'Extrair características da face em imagens.'),
        (9004, 'en', 'Chinese Whispers Clustering',
         'Uses Chinese Whispers algorithm for clustering.'),
        (9004, 'pt', 'Agrupamento Chinese Whispers',
         'Usa o algoritmo Chinese Whispers para agrupamento.'),
        (9005, 'en', 'Image View',
         'Present a image view.'),
        (9005, 'pt', 'Visualização de Imagens',
         'Apresentar imagens.'),
    ]

    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

def _insert_operation_form():
    operation_form_table = table(
        'operation_form',
        column('id', Integer),
        column('enabled', Integer),
        column('order', Integer),
        column('category', String), )

    columns = ('id', 'enabled', 'order', 'category')
    data = [
        (9001, 1, 1, 'execution'), #Form's ID = Operation ID
        (9002, 1, 1, 'execution'), #Form's ID = Operation ID
        (9003, 1, 1, 'execution'), #Form's ID = Operation ID
        (9004, 1, 1, 'execution'), #Form's ID = Operation ID
        (9005, 1, 1, 'execution'), #Form's ID = Operation ID
    ]

    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(operation_form_table, rows)

def _insert_operation_form_translation():
    tb = table(
        'operation_form_translation',
        column('id', Integer),
        column('locale', String),
        column('name', String))

    columns = ('id', 'locale', 'name')
    data = [
        (9001, 'en', 'Execution'), #Form ID
        (9001, 'pt', 'Execução'), #Form ID
        (9002, 'en', 'Execution'), #Form ID
        (9002, 'pt', 'Execução'), #Form ID
        (9003, 'en', 'Execution'), #Form ID
        (9003, 'pt', 'Execução'), #Form ID
        (9004, 'en', 'Execution'), #Form ID
        (9004, 'pt', 'Execução'), #Form ID
        (9005, 'en', 'Execution'), #Form ID
        (9005, 'pt', 'Execução'), #Form ID
    ]
    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

def _insert_operation_operation_form():
    tb = table(
        'operation_operation_form',
        column('operation_id', Integer),
        column('operation_form_id', Integer))

    columns = ('operation_id', 'operation_form_id')
    data = [
        (9001, 41),   # Appearance
        (9001, 9001), #Own Execution Form
        (9001, 110), #Results
        (9002, 41),   # Appearance
        (9002, 9002), #Own Execution Form
        (9002, 110), #Results
        (9003, 41),   # Appearance
        (9003, 9003), #Own Execution Form
        (9003, 110), #Results
        (9004, 41),   # Appearance
        (9004, 9004), #Own Execution Form
        (9004, 110), #Results
        (9005, 41),   # Appearance
        (9005, 9005), #Own Execution Form
        (9005, 110), #Results
    ]

    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)


def _insert_operation_port():
    tb = table(
        'operation_port',
        column('id', Integer),
        column('type', String),
        column('tags', String),
        column('order', Integer),
        column('multiplicity', String),
        column('operation_id', Integer),
        column('slug', String),)

    columns = ('id', 'type', 'tags', 'order', 'multiplicity', 'operation_id', 'slug')
    data = [
        (9001, 'INPUT', '', 1, 'ONE', 9001, 'input data'),
        (9002, 'OUTPUT', '', 1, 'ONE', 9001, 'output data'),
        (9003, 'INPUT', '', 1, 'ONE', 9002, 'input data'),
        (9004, 'OUTPUT', '', 1, 'ONE', 9002, 'output data'),
        (9005, 'INPUT', '', 1, 'ONE', 9003, 'input data'),
        (9006, 'OUTPUT', '', 1, 'ONE', 9003, 'output data'),
        (9007, 'INPUT', '', 1, 'ONE', 9004, 'input data'),
        (9008, 'OUTPUT', '', 1, 'ONE', 9004, 'output data'),
        (9009, 'INPUT', '', 1, 'ONE', 9005, 'input data'),
        (9010, 'OUTPUT', '', 1, 'MANY', 9005, 'visualization'),
    ]

    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

def _insert_operation_port_translation():
    tb = table(
        'operation_port_translation',
        column('id', Integer),
        column('locale', String),
        column('name', String),
        column('description', String), )

    columns = ('id', 'locale', 'name', 'description')
    data = [
        (9001, "en", 'input data', 'Input data'),
        (9001, "pt", 'dados de entrada', 'Dados de entrada'),
        (9002, "en", 'output data', 'Output data'),
        (9002, "pt", 'dados de saída', 'Dados de saída'),
        (9003, "en", 'input data', 'Input data'),
        (9003, "pt", 'dados de entrada', 'Dados de entrada'),
        (9004, "en", 'output data', 'Output data'),
        (9004, "pt", 'dados de saída', 'Dados de saída'),
        (9005, "en", 'input data', 'Input data'),
        (9005, "pt", 'dados de entrada', 'Dados de entrada'),
        (9006, "en", 'output data', 'Output data'),
        (9006, "pt", 'dados de saída', 'Dados de saída'),
        (9007, "en", 'input data', 'Input data'),
        (9007, "pt", 'dados de entrada', 'Dados de entrada'),
        (9008, "en", 'output data', 'Output data'),
        (9008, "pt", 'dados de saída', 'Dados de saída'),
        (9009, "en", 'input data', 'Input data'),
        (9009, "pt", 'dados de entrada', 'Dados de entrada'),
        (9010, "en", 'visualization', 'Visualization'),
        (9010, "pt", 'visualização', 'Visualização'),
    ]

    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

def _insert_operation_port_interface_operation_port():
    tb = table(
        'operation_port_interface_operation_port',
        column('operation_port_id', Integer),
        column('operation_port_interface_id', Integer), )

    columns = ('operation_port_id', 'operation_port_interface_id')
    data = [
        (9001, 1),
        (9002, 1),
        (9003, 1),
        (9004, 1),
        (9005, 1),
        (9006, 1),
        (9007, 1),
        (9008, 1),
        (9009, 1),
        (9010, 19), #vis
    ]
    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

def _insert_operation_form_field():
    tb = table(
        'operation_form_field',
        column('id', Integer),
        column('name', String),
        column('type', String),
        column('required', Integer),
        column('order', Integer),
        column('default', Text),
        column('suggested_widget', String),
        column('values_url', String),
        column('values', String),
        column('scope', String),
        column('form_id', Integer),
        column('enable_conditions', String),
        column('editable', Integer),
    )

    columns = ('id', 'name', 'type', 'required', 'order', 'default',
               'suggested_widget', 'values_url', 'values', 'scope', 'form_id',
               'enable_conditions', 'editable')

    data = [
        #Flatten - data_format
        (9001, 'folder_column', 'TEXT', 1, 1, 'folder_column', 'text', None, None, 'EXECUTION', 9001, None, 1),
        (9002, 'image_column', 'TEXT', 1, 2, 'image_column', 'text', None, None, 'EXECUTION', 9001, None, 1),
        (9003, 'image_prefix', 'TEXT', 1, 1, 'image_prefix', 'text', None, None, 'EXECUTION', 9002, None, 1),
        (9004, 'image_column', 'TEXT', 1, 2, 'image_column', 'text', None, None, 'EXECUTION', 9002, None, 1),
        (9005, 'feature_column', 'TEXT', 1, 2, 'feature_column', 'text', None, None, 'EXECUTION', 9003, None, 1),
        (9006, 'image_column', 'TEXT', 1, 2, 'image_column', 'text', None, None, 'EXECUTION', 9003, None, 1),
        (9007, 'face_column', 'TEXT', 1, 1, 'face_column', 'text', None, None, 'EXECUTION', 9002, None, 1),
        (9008, 'face_location_column', 'TEXT', 1, 2, 'face_location_column', 'text', None, None, 'EXECUTION', 9002, None, 1),
        (9009, 'descriptors', 'TEXT', 1, 1, 'descriptors', 'text', None, None, 'EXECUTION', 9004, None, 1),
        (9010, 'prediction', 'TEXT', 0, 2, 'prediction', 'text', None, None, 'EXECUTION', 9004, None, 1),
        (9011, 'threshold', 'DECIMAL', 0, 3, 0.5, 'decimal', None, None, 'EXECUTION', 9004, None, 1),
        (9012, 'image_column', 'TEXT', 1, 1, 'image_column', 'text', None, None, 'EXECUTION', 9005, None, 1),
        (9013, 'label_column', 'TEXT', 1, 1, 'label_column', 'text', None, None, 'EXECUTION', 9005, None, 1),
        (9014, 'grid_coordinates', 'TEXT', 0, 20, None,'grid-coordinates', None, None, 'EXECUTION', 9005, None, 1),
        (9015, 'normalize', 'INTEGER', 1, 3, 0, 'checkbox', None, None, 'EXECUTION', 9002, None, 1),

    ]
    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

def _insert_operation_form_field_translation():
    tb = table(
        'operation_form_field_translation',
        column('id', Integer),
        column('locale', String),
        column('label', String),
        column('help', String), )

    columns = ('id', 'locale', 'label', 'help')
    data = [
        (9001, 'en', 'Folder Column', 'Folder Column.'),
        (9002, 'en', 'Image Column (new attribute)', 'Image Column (new attribute).'),
        (9003, 'en', 'New Image Prefix', 'New Image Prefix.'),
        (9004, 'en', 'Image Column', 'Image Column.'),
        (9001, 'pt', 'Coluna da Pasta', 'Coluna da Pasta.'),
        (9002, 'pt', 'Coluna da Imagem (novo)', 'Coluna da Imagem (novo).'),
        (9003, 'pt', 'Prefixo da imagem', 'Prefixo da imagem.'),
        (9004, 'pt', 'Coluna da Imagem', 'Coluna da Imagem.'),
        (9005, 'en', 'Feature Column (new attribute)', 'Feature Column (new attribute).'),
        (9006, 'en', 'Image Column', 'Image Column.'),
        (9005, 'pt', 'Coluna da Caracteristica (novo)', 'Coluna da Caracteristica (novo).'),
        (9006, 'pt', 'Coluna da Imagem', 'Coluna da Imagem.'),
        (9007, 'en', 'Face Column (new attribute)', 'Face Column (new attribute).'),
        (9008, 'en', 'Face Location Column (new attribute)', 'Face Location Column (new attribute).'),
        (9007, 'pt', 'Coluna da Face (novo)', 'Coluna da Face (novo).'),
        (9008, 'pt', 'Coluna da Coordenada da Face (novo)', 'Coluna da Coordenada da Face (novo).'),
        (9009, 'en', 'Descriptors', 'Descriptors'),
        (9010, 'en', 'Prediction (new attribute)', 'Prediction (new attribute).'),
        (9011, 'en', 'threshold', 'threshold.'),
        (9009, 'pt', 'Atributo(s) previsor(es)', 'Atributo(s) previsor(es).'),
        (9010, 'pt', 'Atributo com a predição (novo)', 'Atributo com a predição (novo).'),
        (9011, 'pt', 'limiar', 'limiar.'),
        (9012, 'en', 'Image Column', 'Image Column.'),
        (9012, 'pt', 'Coluna de Imagens', 'Coluna de Imagens.'),
        (9013, 'en', 'Label Column', 'Label Column.'),
        (9013, 'pt', 'Coluna de Rótulos', 'Coluna de Rótulos.'),
        [9014, 'en', 'Grid coordinates', 'If generating dashboards, where to include the visualization. Grid has 12 columns and unlimited number of rows.'],
        [9014, 'pt', 'Coordenadas da grade', 'Se a visualização é usada em um dashboard, em qual coordenada da grade ela deve ser incluída. A grade tem 12 colunas e um número ilimitado de linhas.'],
        [9015, 'en', 'Normalize', 'Normalize.'],
        [9015, 'pt', 'Normalizar', 'Normalizar.'],
    ]

    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

#melhorar lógica de rollback
all_commands = [
    (_insert_operation_category,
     'DELETE FROM operation_category WHERE id IN (4003)'),
    (_insert_operation_category_translation,
     'DELETE FROM operation_category_translation WHERE id IN (4003)'),
    (_insert_operation, 'DELETE FROM operation WHERE id >= 9001'),
    (_insert_operation_platform,
     'DELETE FROM operation_platform WHERE operation_id >= 9001'),
    (_insert_operation_category_operation,
     'DELETE FROM operation_category_operation WHERE operation_id >= 9001'),
    (_insert_operation_form, 'DELETE FROM operation_form WHERE id >= 9001'),
    (_insert_operation_form_translation,
     'DELETE FROM operation_form_translation WHERE id >= 9001'),
    (_insert_operation_operation_form,
     'DELETE FROM operation_operation_form WHERE operation_id >= 9001'),
    (_insert_operation_translation,
     'DELETE FROM operation_translation WHERE id >= 9001'),
    (_insert_operation_port, 'DELETE FROM operation_port WHERE id >= 9001'),
    (_insert_operation_port_translation,
     'DELETE FROM operation_port_translation WHERE id >= 9001'),
    (_insert_operation_port_interface_operation_port,
     'DELETE FROM operation_port_interface_operation_port WHERE operation_port_id >= 9001'),
    (_insert_operation_form_field,
     'DELETE FROM operation_form_field WHERE id >= 4373'),
    (_insert_operation_form_field_translation,
     'DELETE FROM operation_form_field_translation WHERE id >= 4373')
]

def upgrade():
    ctx = context.get_context()
    session = sessionmaker(bind=ctx.bind)()
    connection = session.connection()

    try:
        for cmd in all_commands:
            if isinstance(cmd[0], str):
                connection.execute(cmd[0])
            elif isinstance(cmd[0], list):
                for row in cmd[0]:
                    connection.execute(row)
            else:
                cmd[0]()
    except:
        session.rollback()
        raise
    session.commit()


def downgrade():
    ctx = context.get_context()
    session = sessionmaker(bind=ctx.bind)()
    connection = session.connection()

    try:
        for cmd in reversed(all_commands):
            if isinstance(cmd[1], str):
                connection.execute(cmd[1])
            elif isinstance(cmd[1], list):
                for row in cmd[1]:
                    connection.execute(row)
            else:
                cmd[1]()
    except:
        session.rollback()
        raise
    session.commit()