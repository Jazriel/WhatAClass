"""Modify user model(oauth2 google)

Revision ID: 3dd95ad0bef0
Revises: c953f8daef12
Create Date: 2017-06-11 16:44:47.174506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dd95ad0bef0'
down_revision = 'c953f8daef12'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('oauth_token', sa.String(64), unique=True))


def downgrade():
    op.drop_column('user', 'oauth_token')
