"""Add start_time and end_time to Game model

Revision ID: 3591272fa59c
Revises: 1bf62d95c87c

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3591272fa59c'
down_revision = '1bf62d95c87c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_time', sa.Time(), nullable=False))
        batch_op.add_column(sa.Column('end_time', sa.Time(), nullable=False))
        batch_op.drop_column('time')


def downgrade():
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.TIME(), nullable=False))
        batch_op.drop_column('end_time')
        batch_op.drop_column('start_time')
        
