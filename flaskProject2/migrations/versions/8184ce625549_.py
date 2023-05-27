"""empty message

Revision ID: 8184ce625549
Revises: c73fdcd4215d
Create Date: 2023-05-27 22:12:28.482426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8184ce625549'
down_revision = 'c73fdcd4215d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['zhanghao'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
