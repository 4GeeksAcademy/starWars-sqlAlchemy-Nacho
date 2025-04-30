"""empty message

Revision ID: affdfc4adf4c
Revises: 6e12b885086d
Create Date: 2025-04-30 07:31:46.232813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'affdfc4adf4c'
down_revision = '6e12b885086d'
branch_labels = None
depends_on = None


def upgrade():
    # Crear nuevas tablas de favoritos
    op.create_table('user_favorite_planets',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('planet_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['planet_id'], ['planet.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'])
    )
    op.create_table('user_favorite_characters',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('character_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['character_id'], ['character.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'])
    )
    op.create_table('user_favorite_vehicles',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('vehicle_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.ForeignKeyConstraint(['vehicle_id'], ['vehicle.id'])
    )

    # Eliminar claves foráneas y columnas que dependen de 'favorite'
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_constraint('character_vehicle_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('character_favorite_id_fkey', type_='foreignkey')
        batch_op.drop_column('favorite_id')
        batch_op.drop_column('vehicle_id')

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('population', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('climate', sa.String(length=200), nullable=False))
        batch_op.drop_constraint('planet_favorite_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('planet_vehicle_id_fkey', type_='foreignkey')
        batch_op.drop_column('climated')
        batch_op.drop_column('poblation')
        batch_op.drop_column('vehicle_id')
        batch_op.drop_column('favorite_id')

    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.drop_constraint('vehicle_favorite_id_fkey', type_='foreignkey')
        batch_op.drop_column('favorite_id')

    # Ahora sí, eliminar la tabla 'favorite' después de eliminar dependencias
    op.drop_table('favorite')


def downgrade():
    # Restaurar tabla 'favorite'
    op.create_table('favorite',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='favorite_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='favorite_pkey')
    )

    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vehicle_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('favorite_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('character_favorite_id_fkey', 'favorite', ['favorite_id'], ['id'])
        batch_op.create_foreign_key('character_vehicle_id_fkey', 'vehicle', ['vehicle_id'], ['id'])

    with op.batch_alter_table('planet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('vehicle_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('poblation', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('climated', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('planet_vehicle_id_fkey', 'vehicle', ['vehicle_id'], ['id'])
        batch_op.create_foreign_key('planet_favorite_id_fkey', 'favorite', ['favorite_id'], ['id'])
        batch_op.drop_column('climate')
        batch_op.drop_column('population')

    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.add_column(sa.Column('favorite_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('vehicle_favorite_id_fkey', 'favorite', ['favorite_id'], ['id'])

    # Eliminar nuevas tablas de favoritos
    op.drop_table('user_favorite_vehicles')
    op.drop_table('user_favorite_characters')
    op.drop_table('user_favorite_planets')
