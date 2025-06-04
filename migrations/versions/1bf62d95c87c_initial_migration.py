"""initial migration

Revision ID: 1bf62d95c87c
Revises: 

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '1bf62d95c87c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('court',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=200), nullable=False),
    sa.Column('operating_hours', sa.String(length=100), nullable=False),
    sa.Column('wheelchair_rental', sa.Boolean(), nullable=True),
    sa.Column('wheelchair_ramp', sa.Boolean(), nullable=True),
    sa.Column('elevator', sa.Boolean(), nullable=True),
    sa.Column('adjustable_basket', sa.Boolean(), nullable=True),
    sa.Column('image_path', sa.String(length=200), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('court_id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('max_players', sa.Integer(), nullable=False),
    sa.Column('difficulty', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['court_id'], ['court.id'], ),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game_participant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('joined_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('game_participant')
    op.drop_table('game')
    op.drop_table('court')
    op.drop_table('user')
