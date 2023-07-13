"""

Revision ID: 2c0994f3037a
Revises: 8ff7686ccd6f
Create Date: 2023-07-13 14:41:52.550144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c0994f3037a'
down_revision = '8ff7686ccd6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ACCOUNT',
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('value', sa.Numeric(precision=8, scale=2), nullable=False),
    sa.Column('account_date', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('freight_id', sa.BigInteger(), nullable=False),
    sa.Column('identifier', sa.String(length=36), nullable=False),
    sa.Column('synced_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, cycle=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['freight_id'], ['FREIGHT.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('ACCOUNT', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ACCOUNT_freight_id'), ['freight_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_ACCOUNT_identifier'), ['identifier'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ACCOUNT', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_ACCOUNT_identifier'))
        batch_op.drop_index(batch_op.f('ix_ACCOUNT_freight_id'))

    op.drop_table('ACCOUNT')
    # ### end Alembic commands ###
