# voicekit_test
 
## Устанока

- Создайте виртуальное окружение и выполните 
```pip install requirements.txt```
- Откройте ```config.py```, пропишите необходимые ключи API-KEY и SECRET-KEY, логин и пароль пользователя базы данных (по умолчанию они берутся из переменных окружения)
- Для создания необходимых базы данных и таблиц, запустите скрипт ```init_database.py```

## Использование
```
main.py [-h] [-w] filepath phone {stage_one,stage_two}

позиционные аргументы:
  filepath                     путь к .wav файлу
  phone                        телефонный номер
  {stage_one,stage_two}        один из двух возможных этапов

опциональные аргументы:
  -w, --write_to_database      записать результат в базу данных
  -h, --help                   помощь
```
## Пример
```
python main.py /path/to/file.wav 79210123456 stage_two -w
```
