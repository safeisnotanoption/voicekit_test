"""
1. На вход из консоли принимает файл путь к .wav файлу, номер телефона, флаг необходимости записи в базу
данных, этап распознавания(возможно два этапа);
2. Отправляет файл на распознавание;
3. Обрабатывает результат:
Если первый этап, то:
3.1 1.если в аудио записи распознан автоответчик возвращает 0. Если человек, возвращает 1;
Если второй этап, то:
3.2 1. если в ответе есть отрицательные слова (“нет”, “неудобно” и т.п.), то возвращает 0. Если положительные
(“говорите”, “да конечно” и т.п.) то возвращает 1.
4. Пишет результат распознавания в лог-файл в формате: дата, время, уникальный id, результат действия
(АО или человек для 1 этапа и положительно или отрицательно для 2го этапа), номер телефона, длительность аудио,
результат распознавания;
5. Если выставлен соответствующий флаг, то пишет результат в базу данных в том же формате что и в лог-файл.
СУБД Postgres.
6. Удаляет .wav файл;
7. Обрабатывает возникающие ошибки и логирует их в отдельный файл.
"""

import argparse
import datetime
import logging.config
import os
from uuid import uuid4

import config
import services


# Создаем логгер
logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('voicekit_logger')


if __name__ == "__main__":
    args = services.create_parser()
    response = services.voice_recognition(args.filepath)
    transcript = response[0]["alternatives"][0]["transcript"]
    duration = services.calc_duration(response)

    result = False
    if args.recognition_stage == "stage_one":
        result = services.stage_one(transcript)
    elif args.recognition_stage == "stage_two":
        result = services.stage_two(transcript)

    current_time = datetime.datetime.now()
    operation_id = uuid4()

    services.write_to_log_info(current_time, operation_id, result, args.phone, duration, transcript)
    # logger.info("%s, %s, %s, %s, %s, %s", current_time, operation_id, result, args.phone, duration, transcript)
    if args.write_to_database:
        services.write_to_database(current_time, operation_id, result, args.phone, duration, transcript)

    # Удаляем .wav файл
    os.remove(args.filepath)
