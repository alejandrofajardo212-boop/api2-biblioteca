"""0002_multa_pagada

Revision ID: 07069c59e6b5
Revises: 406f4e44beee
Create Date: 2026-11-02 17:12:36.425849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07069c59e6b5'
down_revision: Union[str, None] = '406f4e44beee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("prestamos", sa.Column("multa_pagada", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.execute("UPDATE prestamos SET multa_pagada = true WHERE multa = 0")


def downgrade() -> None:
    op.drop_column("prestamos", "multa_pagada")