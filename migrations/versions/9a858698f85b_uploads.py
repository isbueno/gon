"""Uploads

Revision ID: 9a858698f85b
Revises: 1682db18cde3
Create Date: 2023-11-07 09:44:06.820829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a858698f85b'
down_revision = '1682db18cde3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('uploads',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=50), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('uploads')
    # ### end Alembic commands ###
