"""Change operating hours to opening and closing times

Revision ID: e2c6f410c6fd
Revises: 3591272fa59c

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = 'e2c6f410c6fd'
down_revision = '3591272fa59c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('court', schema=None) as batch_op:
        batch_op.add_column(sa.Column('opening_time', sa.Time(), nullable=False))
        batch_op.add_column(sa.Column('closing_time', sa.Time(), nullable=False))
        batch_op.drop_column('operating_hours')


def downgrade():
    with op.batch_alter_table('court', schema=None) as batch_op:
        batch_op.add_column(sa.Column('operating_hours', sa.VARCHAR(length=100), nullable=False))
        batch_op.drop_column('closing_time')
        batch_op.drop_column('opening_time')
