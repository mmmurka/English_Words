# 📚 *Bot for learning English words* - **LexiFly 🦉**

Welcome to the **Bot for learning English words** project! This bot will help you improve your English vocabulary through regular exercises and interactive learning.

## Table of Contents

- [🔍 Description](#🔍-description)
- [🚀 Installation](#🚀-installation)
- [🛠️ Usage](#🛠️-usage)
- [🌲 Project Structure](#🌲-project-structure)
- [⚙️ Technologies Used](#⚙️-technologies-used)
- [💁‍♂️ Authors](#💁‍♂️-authors)
- [🤝 Contribution](#🤝-contribution)
- [📄 License](#📄-license)


## 🔍 Description

The bot provides users with the opportunity to learn new words and phrases by level of knowledge or on specific topics. This is a great tool for those who want to improve their English language skills.




## 🚀 Installation

Follow these steps to run the bot on your device:

1. **Clone repositories:**
    ```bash
    git clone https://github.com/mmmurka/English_Words.git
    cd English_Words
    ```

2. **Token:**
   Register your bot's unique token:
   1. **Configuration file:** `/Telegram/config.py`  
   2. Insert your **token**:   
     
     ```python
     telegram_token = 'BOT_TOKEN'
    ```
   3. ***Save file***

3. **Running docker:**
    ```bash
    docker-compose up --build
    ```

## 🛠️ Usage

Basic bot commands:
- `/start` - Launch the bot and receive a welcome message.


## 🤝 Contribution

We welcome contributions from the community! If you want to make changes or add new functionality, please follow these steps:

1. Fork the repository.
2. Create new branch:
    ```bash
    git checkout -b feature/new-feature
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "New feature added"
    ```
4. Push changes to your branch:
    ```bash
    git push origin feature/new-feature
    ```
5. Create Pull Request on GitHub.
   
## 🌲 Project Structure

### Telegram
- **Callbacks**
    - `greeting.py` - Functions:
      - send_info_devs, send_bot_info, button_back: Display information about developers, bot and menu.
        themes, support, ukr_trans, eng_trans: Manage the selection of themes, translation language and word input.
        topic, topic, words: Processes the selection of topics/sections/words, displays pagination.
  
    - `paginator.py` - **Functionality:**
      - Displays definitions of words on topics with unsuccessful translation.
        Pagination has been implemented for the number of word lists and topics.
        Handling a click on the pagination button (“previous”, “next”, “trans”).  

        **Structure:**

        pagination_handler: Controls word pagination.
        theme_pagination_handler: Controls pagination of themes/sections. 

        **Key points:**

        Using create_paginator and create_theme_paginator to generate keyboard dynamically.
        trans_text function for translating words.
        Handling TelegramBadRequest exceptions.
    - `topics.py` - **Functionality:**
      - Getting topics by section *("topic_from_table").*  
        Search for topics by group *("theme_from_topic").*  
        Retrieving words and definitions for a topic *("words_from_theme").*  
        Defining a group by topic *("group_from_theme").*  

      - **Implementation:**  
        Async database queries using sqlalchemy.
        Regular expressions for parsing topic names.
        Formation of a word-definition list.
      - **Usage example:**  
  group_from_theme('topic_vocabulary', 'large mammals') -
get the group by topic "large mammals" in the table "topic_vocabulary".
- **Data**
    - ```database_module.py``` - Working with the database. An async engine is created, when the file is launched, tables are migrated
    - `database_words_migration.py` - Script for migrating data from json to database
    - `subloader.py` - Python module containing a function to asynchronously extract JSON data from a file.
    - `words_list.json` - word data
- **Handlers**
    - `bot_messages.py` - echo function for replying to messages
    - `questionaire.py` - state machine handlers for word translation
    - `user_commands` - the start command handler, when triggered, checks whether the user ID is in the database, if not, it adds it
- **Keyboards**
    - `builders.py` - Keyboard Creation:
        -  calc_kb(): Creates a keyboard layout for a calculator with buttons for numbers, operators, and other functions.
       - profile(text): Creates a keyboard layout based on the provided text. It can handle both single-button and multi-button layouts.
      - topic_kb(topics, table): Creates an inline keyboard with buttons representing topics for a specific table in the Telegram bot.
      - theme_kb(themes, table, group_subject): Creates an inline keyboard with buttons representing themes within a topic, handling situations where theme names might be long.
    - `fabrics.py` -
      -  **1. Callback Data Classes:**
         - *Pagination*: Defines a callback data structure (using aiogram.filters.callback_data.CallbackData) for handling pagination actions *("prev", "next")*, page number, database table (db_table), and database theme (db_theme).
         - ***ThemePagination***: Similar to Pagination, but includes an additional field theme_or_topic to differentiate between navigating themes and topics.  
      - **2. Pagination Functions:**
          - ***create_paginator(db_table, db_theme):***   Retrieves the group subject for the given table and theme.
            Creates an anonymous function paginator that generates the inline keyboard based on the page number.
            The keyboard includes buttons for previous/next page, "Назад" (back), and a language toggle button ("🇺🇦").
            The callback data for buttons is constructed using the **Pagination** class.
            Returns the *paginator* function.  

            ***create_theme_paginator(db_table, db_group_subject, theme_or_topic):***
            Fetches themes or topics (depending on theme_or_topic) based on the provided table and subject.
            Splits the themes/topics into a list of pages (10 items per page).  
            Creates an anonymous function *theme_paginator* that generates the inline keyboard based on the page number.
            The keyboard displays buttons for themes/topics (with shortened names for long ones) and includes previous/next page buttons, page info, and a "Назад" button.
            Callback data for buttons uses either ThemePagination or a string depending on the action.
            Returns the *theme_paginator* function.
      - **3. greeting() Function:**
        - Creates a static inline keyboard with buttons for navigating to "Теми" (Topics), "Розробники" (Developers), "Про бота" (About the bot), and "Перекладач" (Translator).
  
    - `inline.py` - Inline keyboard
    - `reply.py` - test file
- **Test**
    - `test_db.py` - **CAUTION:** when running tests the database is dropped
- **Translate**
    - `translateAPI.py` - async function for working with a translator
- **Utils**
    - `states.py` - state machine variables
- ***`config.py`*** - file for bot token and locker configuration
- **`main.py`** - main file including all routers and locking double bot activation
- `pytest.ini` - pytest configuration
  
    
    

## 📄 License

This project is licensed under the MIT License. Details can be found in the file [LICENSE](LICENSE).

## 💁‍♂️ Authors

**[mmmurka](https://github.com/mmmurka)**       |  🐈  
**[nemsh](https://github.com/ArtemNemshylov)**  |   🦧

## ⚙️ Technologies Used

- **Python**: The main programming language used.
- **Aiogram**: A framework for Telegram Bot API.
- **BeautifulSoup4** for web scraping
- **PosgreSQL**: A  database for storing user and bot data.
- **Google Translate API**: For providing translation and pronunciation features.
- **Docker**: For containerizing the application.

## 📧 Contacts

If you have questions or suggestions, you can contact us via telegram: ***@mmmurkaa***

---

Thanks for using our bot! Good luck in learning English! 🚀


