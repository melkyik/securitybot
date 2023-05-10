import os
import pickle
from datetime import datetime
from telegram import Bot
import time
import json
WORK_DIR = '/var/scripts/securitybot/' #нужно указать чтобы запускалось из crone
# Чтение конфигурационного файла
with open(WORK_DIR+'config.json') as config_file:
    config_data = json.load(config_file)

token = config_data['TOKEN']
group_id = config_data['GROUP_ID']


# Путь к папке, которую нужно сканировать
FOLDER_PATH = '/var/ftproot/10116901/SnapShot'

# Путь к файлу для сохранения списка отправленных файлов
SENT_FILES_FILE = WORK_DIR+'sent_files.pkl'

def send_photo_to_group(file_path, creation_date):
    bot = Bot(token=token)
    caption = f'Ктото приходил : {creation_date.strftime("%Y-%m-%d %H:%M:%S")}'
    bot.send_photo(chat_id=group_id, photo=open(file_path, 'rb'), caption=caption)

def load_sent_files():
    if not os.path.exists(SENT_FILES_FILE):
        return set()
    with open(SENT_FILES_FILE, 'rb') as file:
        try:
            return pickle.load(file)
        except:
            return set()

def save_sent_files(sent_files):
    with open(SENT_FILES_FILE, 'wb') as file:
        pickle.dump(sent_files, file)

def scan_folder(folder_path, sent_files):
    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and (file_path not in sent_files):
          #  print(file_path)
            if file_name.lower().endswith('.jpg'):
                creation_date = datetime.fromtimestamp(os.path.getctime(file_path))
                send_photo_to_group(file_path, creation_date)
                sent_files.add(file_path)
                time.sleep(3)
        elif os.path.isdir(file_path):
            scan_folder(file_path, sent_files)

def main():
    sent_files = load_sent_files()
    scan_folder(FOLDER_PATH, sent_files)
    save_sent_files(sent_files)

if __name__ == '__main__':
    main()