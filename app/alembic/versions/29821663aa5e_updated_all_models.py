"""updated all models
Revision ID: 29821663aa5e
Revises: dcee00bf40c8
Create Date: 2024-10-14 01:53:17.906578
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '29821663aa5e'
down_revision: Union[str, None] = 'dcee00bf40c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create a new table with the desired schema without the index for now
    op.create_table(
        'new_links',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('link_name', sa.String, server_default='unknown-link'),
        sa.Column('url', sa.String, nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.current_timestamp()),
        sa.Column('created_by_user_id', sa.BigInteger, nullable=False, server_default=sa.text('243332147379830785'))
    )

    # Copy data from the old table to the new table if needed
    op.execute('INSERT INTO new_links (id, link_name, url, created_at, created_by_user_id) SELECT id, link_name, url, created_at, created_by_user_id FROM links')

    # Drop the old table
    op.drop_table('links')

    # Rename the new table to the old table's name
    op.rename_table('new_links', 'links')

    # Create the index if it doesn't exist
    try:
        op.create_index('ix_links_url', 'links', ['url'], unique=True)
    except Exception as e:
        print(f"Index creation skipped: {e}")

def downgrade() -> None:
    # Drop the existing index if it exists
    try:
        op.drop_index(op.f('ix_links_url'), table_name='links')
    except Exception as e:
        print(f"Index not found: {e}")

    # Create the old table schema
    op.create_table(
        'old_links',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('link_name', sa.String, server_default='unknown-link'),
        sa.Column('url', sa.String, nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime, nullable=True),
        sa.Column('added_by_user_id', sa.BigInteger, nullable=True)
    )

    # Copy data back to the old table schema if needed
    op.execute('INSERT INTO old_links (id, link_name, url, created_at, added_by_user_id) SELECT id, link_name, url, created_at, created_by_user_id FROM links')

    # Drop the new table
    op.drop_table('links')

    # Rename the old table back to its original name
    op.rename_table('old_links', 'links')

    # Recreate the index if it doesn't exist
    try:
        op.create_index('ix_links_url', 'links', ['url'], unique=True)
    except Exception as e:
        print(f"Index creation skipped: {e}")
