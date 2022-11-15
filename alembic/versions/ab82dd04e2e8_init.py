"""init

Revision ID: ab82dd04e2e8
Revises: 
Create Date: 2022-11-15 15:32:29.859810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab82dd04e2e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user_accounts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False)
                    )


def downgrade() -> None:
    op.drop_table('user_accounts')
