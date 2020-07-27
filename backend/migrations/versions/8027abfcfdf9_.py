"""empty message

Revision ID: 8027abfcfdf9
Revises: b3aa3c77f58d
Create Date: 2020-07-27 17:15:00.254439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8027abfcfdf9'
down_revision = 'b3aa3c77f58d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actor', sa.Column('birthdate', sa.Date(), nullable=False))
    op.drop_column('actor', 'age')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('actor', sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('actor', 'birthdate')
    # ### end Alembic commands ###
