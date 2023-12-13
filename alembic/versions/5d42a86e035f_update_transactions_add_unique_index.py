"""update-transactions-add-unique-index

Revision ID: 5d42a86e035f
Revises: ff486958c8d0
Create Date: 2023-12-13 17:59:30.764938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d42a86e035f'
down_revision: Union[str, None] = 'ff486958c8d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_xref_total_loan_amount', 'transactions', ['xref', 'total_loan_amount'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_xref_total_loan_amount', 'transactions', type_='unique')
    # ### end Alembic commands ###