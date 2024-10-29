from sqlalchemy import Column, String, ForeignKey, Text, Table, Integer, Enum, Boolean
from sqlalchemy.orm import relationship
import sqlalchemy.orm

Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=True)
    dictionaries = relationship("Dictionary", back_populates="user")


dictionary_word = Table(
    'dictionary_word', Base.metadata,
    Column('dictionary_id', Integer, ForeignKey('dictionary.id'), primary_key=True),
    Column('word_id', Integer, ForeignKey('word.id'), primary_key=True)
)

class Word(Base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    definition = Column(Text, nullable=True)
    level = Column(Enum('A1', 'A2', 'B1', 'B2', 'C1', 'C2'), nullable=True)
    transcription = Column(String, nullable=True)
    dictionaries = relationship("Dictionary", secondary=dictionary_word, back_populates="words")

class Dictionary(Base):
    __tablename__ = 'dictionary'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    level = Column(Enum('A1', 'A2', 'B1', 'B2', 'C1', 'C2'), nullable=True)
    word_count = Column(Integer, nullable=True)
    is_open = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="dictionaries")
    words = relationship("Word", secondary=dictionary_word, back_populates="dictionaries")


class DynamicTable(Base):
    __abstract__ = True  # abstractstest class

    id = Column(Integer, primary_key=True)
    group_subject = Column(String, index=True)
    subject = Column(String, index=True)
    word = Column(String)
    definition = Column(String)
