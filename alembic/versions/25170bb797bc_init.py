"""init

Revision ID: 25170bb797bc
Revises: 
Create Date: 2025-07-11 15:55:01.004762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25170bb797bc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hero',
    sa.Column('name', sa.String(), nullable=False, comment='Имя героя'),
    sa.Column('intelligence', sa.Integer(), nullable=False, comment='Интеллект'),
    sa.Column('strength', sa.Integer(), nullable=False, comment='Сила'),
    sa.Column('speed', sa.Integer(), nullable=False, comment='Скорость'),
    sa.Column('durability', sa.Integer(), nullable=False, comment='Выносливость'),
    sa.Column('power', sa.Integer(), nullable=False, comment='Мощь'),
    sa.Column('combat', sa.Integer(), nullable=False, comment='Битва'),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    comment='Таблица с героями и их характеристиками'
    )
    op.create_index(op.f('ix_hero_name'), 'hero', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_hero_name'), table_name='hero')
    op.drop_table('hero')
    # ### end Alembic commands ###
