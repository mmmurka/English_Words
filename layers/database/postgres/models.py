from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import sqlalchemy.orm

Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    username = Column(String, nullable=True)
    # Relationship with UserWord
    words = relationship("UserWord", back_populates="user")


class UserWord(Base):
    __tablename__ = 'user_words'

    id = Column(BigInteger, primary_key=True)
    word = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)

    # Foreign key to User
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="words")


class DynamicTable(Base):
    __abstract__ = True  # abstractstest class

    id = Column(BigInteger, primary_key=True)
    group_subject = Column(String, index=True)
    subject = Column(String, index=True)
    word = Column(String)
    definition = Column(String)
