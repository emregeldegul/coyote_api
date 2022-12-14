"""create user table

Revision ID: 9925c79b6be2
Revises: 
Create Date: 2022-09-23 22:09:53.712041

"""
import sqlalchemy as sa
from alembic import op

from app.models.base import DateTime

# revision identifiers, used by Alembic.
revision = "9925c79b6be2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date_created", DateTime(), nullable=True),
        sa.Column("date_modified", DateTime(), nullable=True),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("email_verification", sa.Boolean(), nullable=False),
        sa.Column("email_verification_date", sa.DateTime(), nullable=True),
        sa.Column("email_verification_code", sa.String(length=50), nullable=False),
        sa.Column("email_verification_code_exp_date", sa.DateTime(), nullable=False),
        sa.Column("password_hash", sa.String(length=120), nullable=False),
        sa.Column("status", sa.Enum("active", "passive", "deleted", name="status"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    # ### end Alembic commands ###
