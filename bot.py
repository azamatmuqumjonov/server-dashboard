import psutil
import subprocess
import time
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Токен бота
TOKEN = '7790285101:AAHP6shX2pVcIcraTOnV-rTq6keH2jZJ7rA'
CHAT_ID = '5999342037'

# Функция для отправки сообщения в Telegram
def send_message(message):
    bot = Bot(TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

# Функция для получения состояния системы
def get_system_status():
    # Получение информации о CPU, памяти и дисковом пространстве
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Формируем отчет
    status = f"""
    CPU: {cpu}%
    Memory: {memory.percent}% (Used: {memory.used / (1024 ** 3):.2f} GB / Total: {memory.total / (1024 ** 3):.2f} GB)
    Disk: {disk.percent}% (Used: {disk.used / (1024 ** 3):.2f} GB / Total: {disk.total / (1024 ** 3):.2f} GB)
    """
    return status

# Функция для проверки состояния процессов
def check_processes():
    # Здесь можно указать имена ваших ботов или других процессов
    processes_to_check = ['bot_name1', 'bot_name2']
    not_running = []
    
    # Получаем список всех запущенных процессов
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] in processes_to_check:
            processes_to_check.remove(proc.info['name'])
    
    # Если какие-то процессы не найдены, добавляем их в список неработающих
    if processes_to_check:
        not_running = processes_to_check
    
    return not_running

# Основная функция, которая будет отправлять сообщения в Telegram
def monitor(update, context):
    # Получаем состояние системы
    status = get_system_status()
    # Проверяем процессы
    not_running = check_processes()
    
    if not_running:
        status += "\n\nWarning: The following processes are not running:\n" + "\n".join(not_running)
    
    # Отправляем статус в Telegram
    send_message(status)

# Команда для запуска мониторинга вручную
def start(update, context):
    message = "Monitoring server status..."
    send_message(message)

# Настройка и запуск бота
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Команды
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("monitor", monitor))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
