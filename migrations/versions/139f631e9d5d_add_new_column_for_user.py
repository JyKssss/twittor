"""add new column for user

Revision ID: 139f631e9d5d
Revises: 252d1d499eb7
Create Date: 2020-02-21 20:02:48.515709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '139f631e9d5d'
down_revision = '252d1d499eb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'create_time')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
