"""empty message

Revision ID: ec68dcd0974b
Revises: 60f85290b053
Create Date: 2021-06-28 10:22:29.338859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec68dcd0974b'
down_revision = '60f85290b053'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('room', sa.Column('date_time', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('room', 'date_time')
    # ### end Alembic commands ###
