"""Created user model

Revision ID: c953f8daef12
Revises: 
Create Date: 2017-06-11 16:43:52.879360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c953f8daef12'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(64), unique=True),
        sa.Column( '_password', sa.Binary(128)),
        sa.Column('email_confirmed', sa.Boolean),
    )


def downgrade():
    op.drop_table('user')
