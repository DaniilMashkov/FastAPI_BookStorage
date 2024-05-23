"""Add file_hash field and file_path to books

Revision ID: f8d548b83cf0
Revises: 8b053cd1dd70
Create Date: 2024-05-23 08:56:05.372025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8d548b83cf0'
down_revision: Union[str, None] = '8b053cd1dd70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("books") as batch_op:
        batch_op.add_column(sa.Column('file_path', sa.String, unique=True))
        batch_op.add_column(sa.Column('file_hash', sa.String, unique=True))
        # Добавление именованного ограничения
        batch_op.create_unique_constraint("uq_file_path", ["file_path"])
        batch_op.create_unique_constraint("uq_file_hash", ["file_hash"])



def downgrade():
    with op.batch_alter_table("books") as batch_op:
        batch_op.drop_column('file_path')
        batch_op.drop_column('file_hash')
