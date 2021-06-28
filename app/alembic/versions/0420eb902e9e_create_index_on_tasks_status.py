"""create index on tasks(status)

Revision ID: 0420eb902e9e
Revises: 75346f4187b9
Create Date: 2021-06-27 13:48:51.646233

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0420eb902e9e'
down_revision = '75346f4187b9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index('idx_tasks_status', 'tasks', ['status'])


def downgrade():
    op.drop_index('idx_tasks_status', 'tasks')
