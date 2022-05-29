"""add last few colums to posts table

Revision ID: 9a473d518741
Revises: 62ec66b11f52
Create Date: 2022-05-25 09:07:40.636934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a473d518741'
down_revision = '62ec66b11f52'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column( 'published', sa.Boolean(), nullable=False, sever_default='TRUE'))
    op.add_column('posts', sa.Column( 'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
