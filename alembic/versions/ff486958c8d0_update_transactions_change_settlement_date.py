"""update-transactions-change-settlement_date

Revision ID: ff486958c8d0
Revises: 5f4c42edbc4f
Create Date: 2023-12-13 17:31:34.302096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ff486958c8d0'
down_revision: Union[str, None] = '5f4c42edbc4f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE transactions ALTER COLUMN settlement_date TYPE DATE USING settlement_date::DATE")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'settlement_date', type_=sa.String(length=255))
    # ### end Alembic commands ###