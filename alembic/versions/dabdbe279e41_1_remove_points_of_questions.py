"""1 remove points of questions

Revision ID: dabdbe279e41
Revises: d2e325c6c630
Create Date: 2021-09-17 12:46:35.036700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dabdbe279e41'
down_revision = 'd2e325c6c630'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('answers_players_answer_id_fkey', 'answers_players', type_='foreignkey')
    op.drop_column('answers_players', 'answer_id')
    op.drop_column('questions', 'points')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('points', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('answers_players', sa.Column('answer_id', sa.BIGINT(), autoincrement=False, nullable=False))
    op.create_foreign_key('answers_players_answer_id_fkey', 'answers_players', 'answers', ['answer_id'], ['id'])
    # ### end Alembic commands ###