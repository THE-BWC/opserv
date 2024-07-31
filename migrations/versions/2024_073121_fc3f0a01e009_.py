"""empty message

Revision ID: fc3f0a01e009
Revises: 7c8da069b7f1
Create Date: 2024-07-31 21:02:56.159618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc3f0a01e009'
down_revision = '7c8da069b7f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rank_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'ranks', ['rank_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('rank_id')

    # ### end Alembic commands ###