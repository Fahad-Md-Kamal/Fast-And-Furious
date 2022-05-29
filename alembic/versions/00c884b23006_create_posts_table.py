"""Create posts table

Revision ID: 00c884b23006
Revises: 
Create Date: 2022-05-25 08:26:33.885624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00c884b23006'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        )


def downgrade():
    op.drop_table('posts')
