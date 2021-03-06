"""empty message

Revision ID: eb5dbf1f8d28
Revises: 
Create Date: 2021-12-09 23:33:29.331263

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eb5dbf1f8d28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prsh')
    op.drop_table('app_time')
    op.drop_table('shops')
    op.drop_table('apps_from_json')
    op.drop_table('playtime')
    op.drop_table('swpr')
    op.drop_table('apps')
    op.drop_table('sweets')
    op.drop_table('inventory')
    op.drop_table('shsw')
    op.drop_table('prod')
    op.drop_table('providers')
    op.alter_column('accs', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('accs', 'timecreated',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('accs', 'timecreated',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('accs', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_table('providers',
    sa.Column('id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('inn', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='providers_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('prod',
    sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.CheckConstraint('price >= 0', name='prod_price_check'),
    sa.PrimaryKeyConstraint('id', name='prod_pkey')
    )
    op.create_table('shsw',
    sa.Column('id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('sh_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('sw_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['sh_id'], ['shops.id'], name='shsw_sh_id_fkey'),
    sa.ForeignKeyConstraint(['sw_id'], ['sweets.id'], name='shsw_sw_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='shsw_pkey')
    )
    op.create_table('inventory',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('appid', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('playtime_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('gifted', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['appid'], ['apps.id'], name='inventory_appid_fkey'),
    sa.ForeignKeyConstraint(['playtime_id'], ['playtime.id'], name='inventory_playtime_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['accs.id'], name='inventory_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='inventory_pkey')
    )
    op.create_table('sweets',
    sa.Column('id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('compos', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('about', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='sweets_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('apps',
    sa.Column('id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('dlc', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('parent', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['parent'], ['apps.id'], name='apps_parent_fkey'),
    sa.PrimaryKeyConstraint('id', name='apps_pkey')
    )
    op.create_table('swpr',
    sa.Column('id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('sw_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('pr_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['pr_id'], ['providers.id'], name='swpr_pr_id_fkey'),
    sa.ForeignKeyConstraint(['sw_id'], ['sweets.id'], name='swpr_sw_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='swpr_pkey')
    )
    op.create_table('playtime',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('forever', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('weeks2', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('windows', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('mac', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('linux', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='playtime_pkey')
    )
    op.create_table('apps_from_json',
    sa.Column('id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('author', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('dlc', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('parent', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='apps_from_json_pkey')
    )
    op.create_table('shops',
    sa.Column('id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('date', sa.VARCHAR(length=30), autoincrement=False, nullable=True),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='shops_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('app_time',
    sa.Column('appid', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('mac', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('linux', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('windows', sa.BIGINT(), autoincrement=False, nullable=True)
    )
    op.create_table('prsh',
    sa.Column('id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('sh_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('pr_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['pr_id'], ['providers.id'], name='prsh_pr_id_fkey'),
    sa.ForeignKeyConstraint(['sh_id'], ['shops.id'], name='prsh_sh_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='prsh_pkey')
    )
    # ### end Alembic commands ###
