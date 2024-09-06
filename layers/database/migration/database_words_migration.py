import json
from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL_SYNC = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(DATABASE_URL_SYNC, echo=True)
Base = declarative_base()

# Создаем сессию для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


# Функция нормализации строки
def normalize_string(s):
    return ' '.join(s.split()).strip()


if __name__ == '__main__':
    with open('../data/words_list.json', 'r') as outfile:
        words_list = json.load(outfile)
        for group, dicti in words_list.items():
            class_name = f"Word_{normalize_string(group).capitalize().replace(' ', '_')}"
            table_name = normalize_string(group).lower().replace(' ', '_')

            # Динамическое создание класса
            word_class = type(class_name, (Base,), {
                "__tablename__": table_name,
                "id": Column(BigInteger, primary_key=True),
                "group_subject": Column(String, index=True),
                "subject": Column(String, index=True),
                "word": Column(String),
                "definition": Column(String)
            })

            # Динамическое создание таблицы
            Base.metadata.create_all(bind=engine, tables=[word_class.__table__])

            # Заполнение таблицы данными
            for group_subject, group_dicti in dicti.items():
                normalized_group_subject = normalize_string(group_subject)
                for subject, word_definition in group_dicti.items():
                    normalized_subject = normalize_string(subject)
                    for word, definition in word_definition.items():
                        normalized_word = normalize_string(word)
                        normalized_definition = normalize_string(definition)
                        new_word = word_class(group_subject=normalized_group_subject,
                                              subject=normalized_subject,
                                              word=normalized_word,
                                              definition=normalized_definition)
                        db.add(new_word)

        db.commit()
