"""updated links table - link_name server default
Revision ID: dcee00bf40c8
Revises: b3e3e611f0d4
Create Date: 2024-10-13 17:56:41.619235
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'dcee00bf40c8'
down_revision: Union[str, None] = 'b3e3e611f0d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a new table with the desired schema
    op.create_table(
        'new_links',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('link_name', sa.String, nullable=False, server_default='unknown-link'),
        sa.Column('url', sa.String, nullable=False, unique=True, index=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('created_by_user_id', sa.BigInteger(), nullable=False, server_default=sa.text('243332147379830785'))
    )

    # Drop the old table
    op.drop_table('links')

    # Rename the new table to the old table's name
    op.rename_table('new_links', 'links')


def downgrade() -> None:
    # Revert the changes by creating the old table schema
    op.create_table(
        'old_links',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('weight', sa.Integer, nullable=False, default=5),
        sa.Column('link_name', sa.String, default='unknown-link'),
        sa.Column('url', sa.String, nullable=False, unique=True, index=True),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('added_by_user_id', sa.BigInteger, nullable=True)
    )

    # Drop the new table
    op.drop_table('links')

    # Rename the old table back to its original name
    op.rename_table('old_links', 'links')
