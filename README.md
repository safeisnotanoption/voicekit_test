# voicekit_test

Скрипт, который отправляет .wav-файлы на `https://github.com/TinkoffCreditSystems/voicekit_client_python`, распознает автоответчик и положительное/негативное настроение, а затем вносит результаты в базу данных.

---

## Установка

- Клонировать репозиторий, используя команду `https://github.com/fvcproductions/SOMEREPO`
- Создать виртуальное окружение и выполнить 
```pip install requirements.txt```
- Открыть ```config.py```, прописать необходимые ключи для voicekit_client_python (API-KEY и SECRET-KEY), логин и пароль пользователя базы данных (по умолчанию они берутся из переменных окружения)
- При первом запуске: чтобы создать необходимые базу данных и таблицы, запустить скрипт ```init_database.py```

---

## Использование

```
main.py [-h] [-w] filepath phone {stage_one,stage_two}

позиционные аргументы:
  filepath                     путь к .wav файлу
  phone                        телефонный номер
  {stage_one,stage_two}        один из двух возможных этапов

опциональные аргументы:
  -w, --write_to_database      записать результат в базу данных
  -h, --help                   показать помощь
```

---

## Пример
```
python main.py /path/to/file.wav 79210123456 stage_two -w
```

---

## Примечания
- Используемая версия PostgreSQL 12.4
- SQL-запрос второго задания находится в файле ```second_task.sql```
