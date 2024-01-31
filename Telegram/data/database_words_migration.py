import json
import time

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

db_config = {
    "user": "artemartem",
    "password": "325159799",
    "host": "localhost",
    "database": "englishwords",
}

engine = create_engine(
    f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}",
    echo=True
)
Base = declarative_base()

with open('/Users/artemartem/Documents/GitHub/English_Words/Parcer/words_list.json',
          'r') as outfile:
    words_list = json.load(outfile)
    for group, dicti in words_list.items():
        class_name = f"Word_{group}"
        table_name = group.lower()

        # Динамическое создание класса

        word_class = type(class_name, (Base,), {
            "__tablename__": table_name,
            "id": Column(Integer, primary_key=True, index=True),
            "group_subject": Column(String, index=True),
            "subject": Column(String, index=True),
            "word": Column(String, index=True),
            "definition": Column(String)
        })
        # Динамическое создание таблицы
        word_class.__table__.create(bind=engine, checkfirst=True)

        # Создаем сессию для взаимодействия с базой данных
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Проходим по данным и добавляем их в базу данных
        for group_subject, group_dicti in dicti.items():
            for subject, word_definition in group_dicti.items():
                for word, definition in word_definition.items():
                    new_word = word_class(group_subject=group_subject, subject=subject, word=word,
                                          definition=definition)
                    db.add(new_word)

        # Сохраняем изменения в базе данных
        db.commit()
