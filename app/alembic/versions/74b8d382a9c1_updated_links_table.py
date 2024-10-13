"""updated links table
Revision ID: 74b8d382a9c1
Revises: 0e48b06a92a5
Create Date: 2024-10-12 22:41:50.641202
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '74b8d382a9c1'
down_revision: Union[str, None] = '0e48b06a92a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a new table with the desired schema
    op.create_table(
        'new_links',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('weight', sa.Integer, nullable=False, default=5),
        sa.Column('link_name', sa.String, default='unknown-link'),
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
