"""empty message

Revision ID: 68c1f1d2615e
Revises: 7ce76f8686e0
Create Date: 2025-04-22 17:16:24.224637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68c1f1d2615e'
down_revision = '7ce76f8686e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.Column('character_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], ),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('favoritos')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Favorite', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'favorite', ['Favorite'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('Favorite')

    op.create_table('favoritos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('planet_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('character_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['character.id'], name='favoritos_character_id_fkey'),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], name='favoritos_planet_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='favoritos_pkey')
    )
    op.drop_table('favorite')
    # ### end Alembic commands ###
