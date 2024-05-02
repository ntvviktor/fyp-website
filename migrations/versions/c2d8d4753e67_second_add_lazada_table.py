"""second/add_lazada_table

Revision ID: c2d8d4753e67
Revises: 0f7023fad6ac
Create Date: 2024-04-30 22:15:25.719370

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c2d8d4753e67'
down_revision = '0f7023fad6ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lazada_books', schema=None) as batch_op:
        batch_op.alter_column('url',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lazada_books', schema=None) as batch_op:
        batch_op.alter_column('url',
               existing_type=sa.Text(),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###