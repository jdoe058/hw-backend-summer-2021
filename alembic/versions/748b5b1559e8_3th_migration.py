"""3th migration

Revision ID: 748b5b1559e8
Revises: fcfea0c840c5
Create Date: 2021-09-05 16:59:12.931308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '748b5b1559e8'
down_revision = 'fcfea0c840c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'theme_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'theme_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
