"""Definitions table

Revision ID: 42a72af6db52
Revises: d4e5912869d1
Create Date: 2020-02-22 18:07:53.818736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42a72af6db52'
down_revision = 'd4e5912869d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('definitions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.Integer(), nullable=True),
    sa.Column('definition', sa.String(length=550), nullable=True),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('definitions')
    # ### end Alembic commands ###
