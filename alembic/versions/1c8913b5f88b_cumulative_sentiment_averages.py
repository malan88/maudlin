"""cumulative sentiment averages

Revision ID: 1c8913b5f88b
Revises: 25d0c0af9b71
Create Date: 2021-05-07 09:53:22.372258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c8913b5f88b'
down_revision = '25d0c0af9b71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agency', sa.Column('cum_sent', sa.Float(), nullable=False,
                                      default=0.0))
    op.add_column('agency', sa.Column('cum_neut', sa.Float(), nullable=False,
                                      default=0.0))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('agency', 'cum_neut')
    op.drop_column('agency', 'cum_sent')
    # ### end Alembic commands ###
