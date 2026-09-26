"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-09-26
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=True),
        sa.Column("email", sa.String(255), nullable=True, index=True),
        sa.Column("phone", sa.String(50), nullable=True, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("role", sa.String(50), server_default="SALES_AGENT"),
        sa.Column("hashed_password", sa.String(255), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "leads",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("customers.id"), nullable=False, index=True),
        sa.Column("status", sa.String(50), server_default="NEW", index=True),
        sa.Column("intent", sa.String(50), nullable=True),
        sa.Column("property_type", sa.String(50), nullable=True),
        sa.Column("location_text", sa.Text(), nullable=True),
        sa.Column("bedrooms", sa.Integer(), nullable=True),
        sa.Column("budget_min", sa.Numeric(18, 2), nullable=True),
        sa.Column("budget_max", sa.Numeric(18, 2), nullable=True),
        sa.Column("currency", sa.String(10), server_default="NGN"),
        sa.Column("timeframe", sa.String(50), nullable=True),
        sa.Column("qualification_level", sa.String(20), nullable=True, index=True),
        sa.Column("qualification_score", sa.Integer(), nullable=True),
        sa.Column("urgency", sa.String(20), nullable=True, index=True),
        sa.Column("qualification_version", sa.String(50), nullable=True),
        sa.Column("assigned_to", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "conversations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("customers.id"), nullable=False, index=True),
        sa.Column("lead_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("leads.id"), nullable=True, index=True),
        sa.Column("status", sa.String(50), server_default="ACTIVE"),
        sa.Column("channel", sa.String(50), server_default="web"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("conversations.id"), nullable=False, index=True),
        sa.Column("sender_type", sa.String(30), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("external_message_id", sa.String(255), nullable=True, unique=True, index=True),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "lead_activities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("lead_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("leads.id"), nullable=False, index=True),
        sa.Column("actor_type", sa.String(30), nullable=False),
        sa.Column("actor_id", sa.String(100), nullable=True),
        sa.Column("activity_type", sa.String(50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("payload", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "follow_ups",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("lead_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("leads.id"), nullable=False, index=True),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("status", sa.String(30), server_default="PENDING", index=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("assigned_to", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("lead_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("leads.id"), nullable=False, index=True),
        sa.Column("channel", sa.String(50), nullable=False),
        sa.Column("recipient", sa.String(255), nullable=True),
        sa.Column("status", sa.String(30), server_default="PENDING"),
        sa.Column("payload", postgresql.JSONB(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("notifications")
    op.drop_table("follow_ups")
    op.drop_table("lead_activities")
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("leads")
    op.drop_table("users")
    op.drop_table("customers")
