""" Здесь хранятся наши функции-сервисы """

import argparse
import logging

import psycopg2
import psycopg2.extras
from tinkoff_voicekit_client import ClientSTT

import config

logger = logging.getLogger('voicekit_logger')


def create_parser():
    """ Парсим аргументы командной строки"""
    parser = argparse.ArgumentParser(description="processes the .wav file, phone number, flag of the need to write "
                                                 "to the database, recognition stage")
    parser.add_argument("filepath", type=str, help="the path to the .wav file")
    parser.add_argument("phone", type=str, help="the phone number")
    parser.add_argument("-w", "--write_to_database", action="store_true", help="write the result to the database")
    parser.add_argument("recognition_stage", type=str, help="recognition stage", choices=["stage_one", "stage_two"])

    args = parser.parse_args()
    return args


def voice_recognition(filepath: str) -> list:
    """ Отправляем файл на распознавание"""
    client = ClientSTT(config.API_KEY, config.SECRET_KEY)
    wav_file = filepath
    audio_config = {
        "encoding": "LINEAR16",
        "sample_rate_hertz": 8000,
        "num_channels": 1
    }
    response = client.recognize(wav_file, audio_config)
    return response


def s2f(x):
    """ Преобразуем строковый ответ с 's' в тип float """
    return float(x.strip('s'))


def calc_duration(response: list) -> float:
    """ Считаем длительность аудио """
    start_time = s2f(response[0]["start_time"])
    end_time = s2f(response[0]["end_time"])
    return end_time - start_time


def find_words_in_string(transcript: str, words: list) -> bool:
    """
    Функция возвращает True, если в строке transcript было найдено любое слово из списка words.
    Если слов в строке нет, возвращает False.
    :param transcript: строка, в которой производится поиск
    :param words: список из слов, которые мы ищем в строке
    """
    if any(word in transcript for word in words):
        return True
    else:
        return False


def stage_one(transcript: str) -> bool:
    """ Первый этап """
    words = ["автоответчик", "сигнала"]
    if find_words_in_string(transcript, words):
        return False
    else:
        return True


def stage_two(transcript: str) -> bool:
    """ Второй этап """
    affirmative = ["говорите", "да", "конечно", "хорошо", "слушаю"]
    negative = ["нет", "неудобно", "не", "хватит"]
    if find_words_in_string(transcript, affirmative):
        return True
    elif find_words_in_string(transcript, negative):
        return False


def write_to_log_info(current_time, operation_id, result, phone, duration, transcript):
    """
    Пишет результат распознавания в лог-файл
    :param current_time: текущее время
    :param operation_id: уникальный id
    :param result: результат действия
    :param phone: номер телефона
    :param duration: длительность аудио
    :param transcript: результат распознавания
    """
    logger.info("%s, %s, %s, %s, %s, %s", current_time, operation_id, result, phone, duration, transcript)


def write_to_database(current_time, operation_id, result, phone, duration, transcript):
    """
    Пишет результат распознавания в базу данных
    :param current_time: текущее время
    :param operation_id: уникальный id
    :param result: результат действия
    :param phone: номер телефона
    :param duration: длительность аудио
    :param transcript: результат распознавания
    """

    query = """
            INSERT INTO voice_call(datetime, operation_id, result, phone, duration, transcript)
            VALUES(%s, %s, %s, %s, %s, %s)
            """

    conn = None
    try:
        psycopg2.extras.register_uuid()
        conn = psycopg2.connect(user=config.PG_USER,
                                password=config.PG_PASSWORD,
                                host=config.PG_HOST,
                                port=config.PG_PORT,
                                database="voicekit_db")
        cur = conn.cursor()
        cur.execute(query, (current_time, operation_id, result, phone, duration, transcript))
        conn.commit()
        cur.close()

    except psycopg2.OperationalError:
        logger.exception("Не удалось подключиться к базе данных. Проверьте работу сервера и настроек PostgreSQL")
    except Exception as e:
        logger.exception("Ошибка во время записи в базу данных. ")
    finally:
        conn.close()
