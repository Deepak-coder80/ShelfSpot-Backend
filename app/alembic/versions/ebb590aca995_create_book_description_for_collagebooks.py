"""create book description and book id for collageBooks

Revision ID: ebb590aca995
Revises: 
Create Date: 2023-04-09 13:04:39.514302

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ebb590aca995'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('collageBooks',
                  sa.Column('book_description', sa.String(), nullable=True))
    op.add_column('collageBooks',sa.Column('book_id', sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column('collageBooks', 'book_description')
