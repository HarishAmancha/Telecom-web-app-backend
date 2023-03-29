"""change_id_column_length

Revision ID: 162cd2894b44
Revises: b3fc08b3b65a
Create Date: 2023-03-29 22:08:57.114177

"""
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision = "162cd2894b44"
down_revision = "b3fc08b3b65a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user_model",
        "id",
        existing_type=mysql.VARCHAR(length=16),
        type_=sa.String(length=36),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user_model",
        "id",
        existing_type=sa.String(length=36),
        type_=mysql.VARCHAR(length=16),
        existing_nullable=False,
    )
    # ### end Alembic commands ###