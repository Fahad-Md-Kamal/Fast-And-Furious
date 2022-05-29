"""Create users table

Revision ID: 170342977120
Revises: 20874e8f0332
Create Date: 2022-05-25 08:49:31.725581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '170342977120'
down_revision = '20874e8f0332'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
        )

def downgrade():
    op.drop_table('users')
