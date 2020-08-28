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
import os

from tinkoff_voicekit_client import ClientSTT


API_KEY = os.environ.get('API_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

parser = argparse.ArgumentParser(description='processes the .wav file, phone number, flag of the need to write '
                                             'to the database, recognition stage')
parser.add_argument('filepath', type=str, help='the path to the .wav file')
parser.add_argument('phone', type=str, help='the phone number')
parser.add_argument('-w', '--write_to_database', action='store_true', help='write the result to the database')
parser.add_argument('recognition_stage', type=str, help='recognition stage', choices=['stage_one', 'stage_two'])

args = parser.parse_args()


def voice_recognition() -> list:
    """ Отправляем файл на распознавание"""
    client = ClientSTT(API_KEY, SECRET_KEY)
    wav_file = args.filepath
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
    start_time = s2f(response[0]['start_time'])
    end_time = s2f(response[0]['end_time'])
    return start_time - end_time


def stage_one(transcript: str) -> bool:
    if 'автоответчик' in transcript:
        return False
    else:
        return True


def stage_two(transcript: str) -> bool:
    return False


def write_to_database():
    pass


print(args.filepath, args.phone, args.write_to_database, args.recognition_stage)

if __name__ == "__main__":
    response_from_server = voice_recognition()
    transcript_from_response = response_from_server[0]['alternatives'][0]['transcript']
    print(transcript_from_response)
    duration = calc_duration(response_from_server)
    print(duration)
    result = False
    if args.recognition_stage == 'stage_one':
        result = stage_one()
    elif args.recognition_stage == 'stage_two':
        result = stage_two()
