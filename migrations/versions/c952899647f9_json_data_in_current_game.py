"""Json data in current game

Revision ID: c952899647f9
Revises: 53da096e30fe
Create Date: 2020-01-13 11:43:27.500549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c952899647f9'
down_revision = '53da096e30fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('current_game', sa.Column('game_data', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('current_game', 'game_data')
    # ### end Alembic commands ###