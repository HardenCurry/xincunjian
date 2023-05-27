"""empty message

Revision ID: c73fdcd4215d
Revises: e03cc0eb21ed
Create Date: 2023-05-27 21:40:19.976285

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c73fdcd4215d'
down_revision = 'e03cc0eb21ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('number',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=255),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('zhanghao',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('gender',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('phone',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
        batch_op.drop_index('number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index('number', ['number'], unique=False)
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('phone',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('gender',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('zhanghao',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('number',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=255),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###
