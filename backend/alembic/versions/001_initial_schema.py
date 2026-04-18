"""Initial schema — create hcp, interaction, sample, follow_up tables.

Revision ID: 001_initial
Revises: (none)
Create Date: 2026-04-17
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- HCP table ---
    op.create_table(
        'hcp',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('specialty', sa.String(), nullable=False),
        sa.Column('institution', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    # --- Interaction table ---
    op.create_table(
        'interaction',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('hcp_id', sa.Integer(), nullable=False),
        sa.Column('interaction_type', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('time', sa.Time(), nullable=True),
        sa.Column('attendees', sa.Text(), nullable=True),
        sa.Column('topics_discussed', sa.Text(), nullable=True),
        sa.Column('materials_shared', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('sentiment', sa.String(), nullable=True),
        sa.Column('outcome', sa.Text(), nullable=True),
        sa.Column('follow_up_notes', sa.Text(), nullable=True),
        sa.Column('follow_up_date', sa.Date(), nullable=True),
        sa.Column('ai_suggested_followups', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('source', sa.String(), nullable=False, server_default='form'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['hcp_id'], ['hcp.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )

    # --- Sample table ---
    op.create_table(
        'sample',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('interaction_id', sa.Integer(), nullable=False),
        sa.Column('product_name', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['interaction_id'], ['interaction.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )

    # --- FollowUp table ---
    op.create_table(
        'follow_up',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('interaction_id', sa.Integer(), nullable=False),
        sa.Column('hcp_id', sa.Integer(), nullable=False),
        sa.Column('follow_up_date', sa.Date(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['interaction_id'], ['interaction.id'], ),
        sa.ForeignKeyConstraint(['hcp_id'], ['hcp.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('follow_up')
    op.drop_table('sample')
    op.drop_table('interaction')
    op.drop_table('hcp')
