"""empty message

Revision ID: 297dc056ae36
Revises: 
Create Date: 2022-01-18 23:59:14.129308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '297dc056ae36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status_name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('status_name')
    )
    op.create_table('type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type_name', sa.String(length=6), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type_name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('imdb', sa.String(length=15), nullable=True),
    sa.Column('title', sa.String(length=250), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('year', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['type_id'], ['type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('imdb')
    )
    op.create_table('entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['status.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entry')
    op.drop_table('movie')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('type')
    op.drop_table('status')
    # ### end Alembic commands ###