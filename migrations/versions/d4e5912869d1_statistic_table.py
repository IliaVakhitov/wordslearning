"""Statistic table

Revision ID: d4e5912869d1
Revises: f273e939b2c7
Create Date: 2020-02-03 21:12:38.777858

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4e5912869d1'
down_revision = 'f273e939b2c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statistic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('game_type', sa.String(length=30), nullable=True),
    sa.Column('total_rounds', sa.Integer(), nullable=True),
    sa.Column('correct_answers', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('statistic')
    # ### end Alembic commands ###
