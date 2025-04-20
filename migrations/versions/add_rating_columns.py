"""Add rating columns to materials table

Revision ID: add_rating_columns
Revises: initial_migration
Create Date: 2024-04-20 05:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_rating_columns'
down_revision = 'initial_migration'
branch_labels = None
depends_on = None


def upgrade():
    # Add rating_sum and rating_count columns to materials table
    op.add_column('materials', sa.Column('rating_sum', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('materials', sa.Column('rating_count', sa.Integer(), nullable=True, server_default='0'))


def downgrade():
    # Remove rating_sum and rating_count columns from materials table
    op.drop_column('materials', 'rating_sum')
    op.drop_column('materials', 'rating_count') 