"""Initial migration.

Revision ID: 7c4814832e06
Revises: 
Create Date: 2023-03-27 22:09:10.079884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c4814832e06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TRUCK_DRIVER',
    sa.Column('id', sa.Integer(), sa.Identity(always=False, start=1, cycle=True), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password_digest', sa.String(length=512), nullable=True),
    sa.Column('last_sign_in_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('TRUCK_DRIVER')
    # ### end Alembic commands ###
