"""add foreign key to post table

Revision ID: 62ec66b11f52
Revises: 170342977120
Create Date: 2022-05-25 09:02:24.991385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62ec66b11f52'
down_revision = '170342977120'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
