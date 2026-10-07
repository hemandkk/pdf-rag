"""Make document embedding metadata nullable.

Revision ID: 0004
Revises: 0003
Create Date: 2026-10-06
"""

from alembic import op
import sqlalchemy as sa


revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table(
        "documents",
        schema=None,
    ) as batch_op:
        batch_op.alter_column(
            "embedding_provider",
            existing_type=sa.String(length=100),
            nullable=True,
        )

        batch_op.alter_column(
            "embedding_model",
            existing_type=sa.String(length=200),
            nullable=True,
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "documents",
        schema=None,
    ) as batch_op:
        batch_op.alter_column(
            "embedding_provider",
            existing_type=sa.String(length=100),
            nullable=False,
        )

        batch_op.alter_column(
            "embedding_model",
            existing_type=sa.String(length=200),
            nullable=False,
        )