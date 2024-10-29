"""dictionary models and updated user

Revision ID: 661d5f0a1c87
Revises: e534112edbaa
Create Date: 2024-10-29 21:04:14.689312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '661d5f0a1c87'
down_revision: Union[str, None] = 'e534112edbaa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Створення таблиці dictionary
    op.create_table(
        'dictionary',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('level', sa.Enum('A1', 'A2', 'B1', 'B2', 'C1', 'C2', name="dictionary_level"), nullable=True),
        sa.Column('word_count', sa.Integer, nullable=True),
        sa.Column('is_open', sa.Boolean, nullable=False),
        sa.Column('user_id', sa.BigInteger, sa.ForeignKey('users.id'), nullable=False)
    )
    op.drop_table('user_words')
    # Створення таблиці word
    op.create_table(
        'word',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('word', sa.String, nullable=False),
        sa.Column('definition', sa.Text, nullable=True),
        sa.Column('level', sa.Enum('A1', 'A2', 'B1', 'B2', 'C1', 'C2', name="word_level"), nullable=True),
        sa.Column('transcription', sa.String, nullable=True)
    )

    # Створення асоціативної таблиці dictionary_word для зв’язку між dictionary і word
    op.create_table(
        'dictionary_word',
        sa.Column('dictionary_id', sa.Integer, sa.ForeignKey('dictionary.id'), primary_key=True),
        sa.Column('word_id', sa.Integer, sa.ForeignKey('word.id'), primary_key=True)
    )

def downgrade() -> None:
    # Видалення таблиць у зворотному порядку
    op.drop_table('dictionary_word')
    op.drop_table('word')
    op.drop_table('dictionary')
