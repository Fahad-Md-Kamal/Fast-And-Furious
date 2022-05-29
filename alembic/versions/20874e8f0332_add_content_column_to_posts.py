"""Add content column to posts

Revision ID: 20874e8f0332
Revises: 00c884b23006
Create Date: 2022-05-25 08:49:04.859971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20874e8f0332'
down_revision = '00c884b23006'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column( 'posts', sa.Column('content', sa.String(), nullable=False))

def downgrade():
    op.drop_column('posts', 'content')
