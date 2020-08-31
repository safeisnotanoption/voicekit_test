import datetime
import logging.config
import os
from uuid import uuid4

import config
import services

logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('voicekit_logger')


def main():
    # Считываем аргументы командной строки
    args = services.create_parser()
    # Пропускаем .wav файл через распознавание голоса
    response = services.voice_recognition(args.filepath)
    transcript = response[0]["alternatives"][0]["transcript"]
    duration = services.calc_duration(response)
    # Ищем результат
    result = False
    if args.recognition_stage == "stage_one":
        result = services.stage_one(transcript)
    elif args.recognition_stage == "stage_two":
        result = services.stage_two(transcript)
    # Получаем текущую дату (чтобы вписать одинаковую дату и в лог, и в базу данных) и уникальный id операции
    current_time = datetime.datetime.now()
    operation_id = uuid4()
    # Пишем данные в лог и (при необходимости) в базу данных
    services.write_to_log_info(current_time, operation_id, result, args.phone, duration, transcript)
    if args.write_to_database:
        services.write_to_database(current_time, operation_id, result, args.phone, duration, transcript)
    # Удаляем .wav файл
    try:
        os.remove(args.filepath)
    except FileNotFoundError:
        logger.exception("Ошибка во время удаления файла")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception(f"Ошибка во время выполнения основной программы. Входные данные:\n{services.create_parser()}")
