"""Здесь описан способ скачивания файлов на компьютер"""

import instaloader
import os
import re
import logging


# Настройка логирования
logging.basicConfig(
    filename='logfile.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Создание папки для сохранения файлов
download_folder = 'download'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Создаем Instaloader
Loader = instaloader.Instaloader()

# Переменные с логином и паролем (Это плохой пример, не делать так в своих проектах)
USERNAME = '***'
PASSWORD = '***'

# Вход в Instagram
try:
    Loader.login(USERNAME, PASSWORD)
    logging.info('Успешный вход в Instagram.')
except Exception as e:
    logging.error(f'Ошибка при входе в Instagram: {e}')
    raise


def extract_shortcode(url):
    """
    Извлекает shortcode из URL поста или рилса.
    :paramter url: Строка с URL
    :return: Shortcode или None, если не удалось извлечь
    """
    patterns = [r'/p/([^/]+)', r'/reel/([^/]+)']
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


# Функция для загрузки контента по ссылке
def download_content_from_url(url):
    # Получение shortcode из URL
    shortcode = extract_shortcode(url)
    if not shortcode:
        logging.error(f"Не удалось извлечь shortcode из URL: {url}")
        return
    # Проверяем где мы находимся.
    try:
        if os.getcwd != os.path.abspath(download_folder):
            os.chdir(os.path.abspath(download_folder))
            logging.info(f"Рабочая директория изменена на {os.getcwd()}")
        else:
            logging.info(f"Уже находимся в {os.getcwd()}")
        # Загрузка поста по shortcode
        post = instaloader.Post.from_shortcode(Loader.context, shortcode)
        post_dir = shortcode
        Loader.download_post(post, target=post_dir)
        logging.info(f"Скачан контент: {url}")
    except Exception as e:
        logging.error(f"Ошибка при скачивании контента: {e}")

# Список URL для загрузки
urls = [
    '***',  # Замените на реальные ссылки
    '***',  # Замените на реальные ссылки
]

# Скачивание контента
for url in urls:
    download_content_from_url(url)

logging.info(f"Загрузка завершена. Все файлы сохранены в папке {download_folder}")
