"""Add phone number

Revision ID: 7890d7a771de
Revises: a02b521a6d6e
Create Date: 2023-05-27 05:40:32.642938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7890d7a771de'
down_revision = 'a02b521a6d6e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###