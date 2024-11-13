"""init

Revision ID: bc171f131d94
Revises: 
Create Date: 2024-11-13 11:02:11.503500

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc171f131d94'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'weather',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('time', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('wind_speed', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id', 'time'),
    )
    # ### end Alembic commands ###
    op.execute("SELECT create_hypertable('weather', 'time');")


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weather')
    # ### end Alembic commands ###