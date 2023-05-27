"""empty message

Revision ID: e03cc0eb21ed
Revises: 
Create Date: 2023-05-27 21:32:09.431861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e03cc0eb21ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document',
    sa.Column('dnum', sa.String(length=255, collation='utf8mb4_0900_ai_ci'), nullable=False),
    sa.Column('time', sa.String(length=255), nullable=True),
    sa.Column('date', sa.String(length=255), nullable=True),
    sa.Column('fnum', sa.String(length=255), nullable=True),
    sa.Column('weight', sa.String(length=255), nullable=True),
    sa.Column('unum', sa.String(length=255), nullable=True),
    sa.Column('energy', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('dnum')
    )
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_document_dnum'), ['dnum'], unique=False)
        batch_op.create_index(batch_op.f('ix_document_unum'), ['unum'], unique=False)

    op.create_table('food',
    sa.Column('fnum', sa.Integer(), nullable=False),
    sa.Column('type1', sa.String(length=255, collation='utf8mb4_0900_ai_ci'), nullable=True),
    sa.Column('type2', sa.String(length=255, collation='utf8mb4_0900_ai_ci'), nullable=True),
    sa.Column('fname', sa.String(length=255, collation='utf8mb4_0900_ai_ci'), nullable=True),
    sa.Column('link', sa.String(length=255, collation='utf8mb4_0900_ai_ci'), nullable=True),
    sa.Column('img', sa.String(length=255, collation='utf8mb4_0900_ai_ci'), nullable=True),
    sa.Column('energy', sa.String(length=255, collation='utf8mb4_0900_ai_ci'), nullable=True),
    sa.PrimaryKeyConstraint('fnum'),
    sa.UniqueConstraint('fnum')
    )
    with op.batch_alter_table('food', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_food_type1'), ['type1'], unique=False)
        batch_op.create_index(batch_op.f('ix_food_type2'), ['type2'], unique=False)

    op.create_table('user',
    sa.Column('number', sa.String(length=255, collation='utf8mb4_0900_ai_ci'), nullable=False),
    sa.Column('zhanghao', sa.String(length=255), nullable=True),
    sa.Column('gender', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('number'),
    sa.UniqueConstraint('number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    with op.batch_alter_table('food', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_food_type2'))
        batch_op.drop_index(batch_op.f('ix_food_type1'))

    op.drop_table('food')
    with op.batch_alter_table('document', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_document_unum'))
        batch_op.drop_index(batch_op.f('ix_document_dnum'))

    op.drop_table('document')
    # ### end Alembic commands ###
