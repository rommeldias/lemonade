""" Add OpenID configuration  

Revision ID: c79673214a30
Revises: 1fbc565aa957
Create Date: 2021-05-06 16:32:13.484353

"""
import datetime

import bcrypt
from alembic import context
from alembic import op
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import table, column
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = 'c79673214a30'
down_revision = '1fbc565aa957'
branch_labels = None
depends_on = None

def _insert_configuration_translation():
    tb = table(
        'configuration_translation',
        column('id', Integer),
        column('locale', String),
        column('description', String),
        column('category', String),
    )
    columns = [c.name for c in tb.columns]
    data = [
        (10, 'pt', 'Configuração para OpenID (JSON, requer reinício)', 'Autenticação'),
        (10, 'en', 'OpenID configuration (JSON, requires restart)', 'Authentication'),
        (11, 'pt', 'OpenID+JWT: chave pública (usada para validar o token, requer reinício) ', 'Autenticação'),
        (11, 'en', 'OpenID+JWT public key (used to validate the token, requires restart)', 'Authentication'),
    ]
    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)


def _insert_configuration():
    tb = table(
        'configuration',
        column('id', Integer),
        column('name', String),
        column('value', String),
        column('enabled', Integer),
        column('internal', Integer),
        column('editor', String),
    )
    columns = [c.name for c in tb.columns]
    data = [
        (10, 'OPENID_CONFIG', '{}', 1, 0, 'TEXTAREA'),
        (11, 'OPENID_JWT_PUB_KEY', '{}', 1, 0, 'TEXTAREA'),
    ]
    rows = [dict(list(zip(columns, row))) for row in data]
    op.bulk_insert(tb, rows)

def _add_authentication_type():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'authentication_type',
               existing_type=mysql.ENUM('LDAP', 'INTERNAL', 'AD', 'OPENID', collation='utf8_unicode_ci'),
               nullable=True)
    # ### end Alembic commands ###


def _remove_authentication_type():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'authentication_type',
               existing_type=mysql.ENUM('LDAP', 'INTERNAL', 'AD', collation='utf8_unicode_ci'),
               nullable=False)

all_commands = [
    (_insert_configuration, 'DELETE FROM configuration WHERE id IN (10, 11) '),
    (_insert_configuration_translation, 'DELETE FROM configuration_translation WHERE id IN (10, 11)'),
    (_add_authentication_type, _remove_authentication_type)
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
