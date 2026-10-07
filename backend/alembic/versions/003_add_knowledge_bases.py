"""add knowledge bases and link documents and conversations

Revision ID: 0003
Revises: 0002
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ------------------------------------------------------------------
    # 1. Create knowledge_bases table
    # ------------------------------------------------------------------

    op.create_table(
        "knowledge_bases",
        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=200),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ------------------------------------------------------------------
    # 2. Add knowledge_base_id to documents
    # ------------------------------------------------------------------

    with op.batch_alter_table(
        "documents",
        schema=None,
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "knowledge_base_id",
                sa.String(length=36),
                nullable=True,
            )
        )

    # ------------------------------------------------------------------
    # 3. Create a default knowledge base
    # ------------------------------------------------------------------

    connection = op.get_bind()

    default_knowledge_base_id = (
        "00000000-0000-0000-0000-000000000001"
    )

    connection.execute(
        sa.text(
            """
            INSERT INTO knowledge_bases (
                id,
                name,
                description
            )
            VALUES (
                :id,
                :name,
                :description
            )
            """
        ),
        {
            "id": default_knowledge_base_id,
            "name": "Default Knowledge Base",
            "description": (
                "Default knowledge base created during "
                "database migration."
            ),
        },
    )

    # ------------------------------------------------------------------
    # 4. Assign existing documents to the default knowledge base
    # ------------------------------------------------------------------

    connection.execute(
        sa.text(
            """
            UPDATE documents
            SET knowledge_base_id = :knowledge_base_id
            WHERE knowledge_base_id IS NULL
            """
        ),
        {
            "knowledge_base_id": default_knowledge_base_id,
        },
    )

    # ------------------------------------------------------------------
    # 5. Make documents.knowledge_base_id required
    #    and add foreign key + index
    # ------------------------------------------------------------------

    with op.batch_alter_table(
        "documents",
        schema=None,
    ) as batch_op:
        batch_op.alter_column(
            "knowledge_base_id",
            existing_type=sa.String(length=36),
            nullable=False,
        )

        batch_op.create_foreign_key(
            "fk_documents_knowledge_base_id",
            "knowledge_bases",
            ["knowledge_base_id"],
            ["id"],
            ondelete="CASCADE",
        )

        batch_op.create_index(
            "ix_documents_knowledge_base_id",
            ["knowledge_base_id"],
            unique=False,
        )

    # ------------------------------------------------------------------
    # 6. Add knowledge_base_id to conversations
    # ------------------------------------------------------------------

    with op.batch_alter_table(
        "conversations",
        schema=None,
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "knowledge_base_id",
                sa.String(length=36),
                nullable=True,
            )
        )

    # ------------------------------------------------------------------
    # 7. Populate conversation knowledge_base_id
    #
    # At this point conversations still contain document_id.
    # ------------------------------------------------------------------

    connection.execute(
        sa.text(
            """
            UPDATE conversations
            SET knowledge_base_id = (
                SELECT documents.knowledge_base_id
                FROM documents
                WHERE documents.id = conversations.document_id
            )
            WHERE knowledge_base_id IS NULL
            """
        )
    )

    # ------------------------------------------------------------------
    # 8. Rebuild conversations table
    #
    # IMPORTANT:
    # SQLite already has the old document_id index created by 0002.
    # We must explicitly remove that index BEFORE removing document_id.
    # Otherwise Alembic attempts to recreate the old index during the
    # batch table rebuild.
    # ------------------------------------------------------------------

    with op.batch_alter_table(
        "conversations",
        schema=None,
    ) as batch_op:
        # Remove the old index BEFORE dropping document_id.
        batch_op.drop_index(
            "ix_conversations_document_id",
        )

        # The old document_id foreign key is removed automatically
        # when SQLite rebuilds the table without document_id.

        batch_op.alter_column(
            "knowledge_base_id",
            existing_type=sa.String(length=36),
            nullable=False,
        )

        batch_op.create_foreign_key(
            "fk_conversations_knowledge_base_id",
            "knowledge_bases",
            ["knowledge_base_id"],
            ["id"],
            ondelete="CASCADE",
        )

        batch_op.create_index(
            "ix_conversations_knowledge_base_id",
            ["knowledge_base_id"],
            unique=False,
        )

        # Finally remove the old document relationship.
        batch_op.drop_column(
            "document_id",
        )


def downgrade() -> None:
    connection = op.get_bind()

    # ------------------------------------------------------------------
    # 1. Add document_id back
    # ------------------------------------------------------------------

    with op.batch_alter_table(
        "conversations",
        schema=None,
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "document_id",
                sa.String(length=36),
                nullable=True,
            )
        )

    # ------------------------------------------------------------------
    # 2. Restore document_id using a document from the same
    #    knowledge base.
    # ------------------------------------------------------------------

    connection.execute(
        sa.text(
            """
            UPDATE conversations
            SET document_id = (
                SELECT documents.id
                FROM documents
                WHERE documents.knowledge_base_id =
                      conversations.knowledge_base_id
                ORDER BY documents.created_at
                LIMIT 1
            )
            WHERE document_id IS NULL
            """
        )
    )

    # ------------------------------------------------------------------
    # 3. Rebuild conversations back to the old structure
    # ------------------------------------------------------------------

    with op.batch_alter_table(
        "conversations",
        schema=None,
    ) as batch_op:
        batch_op.alter_column(
            "document_id",
            existing_type=sa.String(length=36),
            nullable=False,
        )

        batch_op.create_foreign_key(
            "fk_conversations_document_id",
            "documents",
            ["document_id"],
            ["id"],
            ondelete="CASCADE",
        )

        batch_op.create_index(
            "ix_conversations_document_id",
            ["document_id"],
            unique=False,
        )

        batch_op.drop_index(
            "ix_conversations_knowledge_base_id",
        )

        batch_op.drop_column(
            "knowledge_base_id",
        )

    # ------------------------------------------------------------------
    # 4. Remove knowledge_base_id from documents
    # ------------------------------------------------------------------

    with op.batch_alter_table(
        "documents",
        schema=None,
    ) as batch_op:
        batch_op.drop_index(
            "ix_documents_knowledge_base_id",
        )

        batch_op.drop_constraint(
            "fk_documents_knowledge_base_id",
            type_="foreignkey",
        )

        batch_op.drop_column(
            "knowledge_base_id",
        )

    # ------------------------------------------------------------------
    # 5. Remove knowledge_bases
    # ------------------------------------------------------------------

    op.drop_table(
        "knowledge_bases",
    )