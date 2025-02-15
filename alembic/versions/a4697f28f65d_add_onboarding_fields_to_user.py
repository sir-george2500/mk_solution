"""add onboarding fields to user

Revision ID: a4697f28f65d
Revises: 5b425b6bbe0c
Create Date: ...
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a4697f28f65d'
down_revision: Union[str, None] = '5b425b6bbe0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Add columns with server_default for existing records
    op.add_column('users', sa.Column('is_onboarded', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('users', sa.Column('is_approved', sa.Boolean(), server_default='false', nullable=False))

def downgrade() -> None:
    op.drop_column('users', 'is_approved')
    op.drop_column('users', 'is_onboarded')