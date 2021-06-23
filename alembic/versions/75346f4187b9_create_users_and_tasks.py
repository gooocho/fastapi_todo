"""init

Revision ID: 75346f4187b9
Revises: 
Create Date: 2021-06-23 09:07:17.112840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "75346f4187b9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.VARCHAR(100), nullable=False),
        sa.Column("mail", sa.VARCHAR(256), nullable=False),
    )
    op.create_index("idx_users_mail", "users", ["mail"], None, True)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("title", sa.TEXT, nullable=False),
        sa.Column("description", sa.TEXT, nullable=False),
        sa.Column("priority", sa.Integer, nullable=False),
        sa.Column("status", sa.Integer, nullable=False),
    )

    op.create_table(
        "assignments",
        sa.Column("user_id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("task_id", sa.Integer, primary_key=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    op.create_index(
        "idx_assignments_task_id_user_id", "assignments", ["task_id", "user_id"]
    )


def downgrade():
    op.drop_index("idx_assignments_task_id_user_id", "assignments")
    op.drop_table("assignments")
    op.drop_table("tasks")
    op.drop_index("idx_users_mail", "users")
    op.drop_table("users")
