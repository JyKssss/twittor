"""add phone to user

Revision ID: 5829203e3ace
Revises: 1ba7ec22e37e
Create Date: 2020-02-18 04:35:46.215431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5829203e3ace'
down_revision = '1ba7ec22e37e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('phone', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone')
    # ### end Alembic commands ###
