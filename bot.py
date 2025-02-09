import psutil
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Токен бота
TOKEN = "7790285101:AAHP6shX2pVcIcraTOnV-rTq6keH2jZJ7rA"

# Функция для получения состояния системы
def get_system_status():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    # Память
    memory = psutil.virtual_memory()
    # Диск
    disk = psutil.disk_usage('/')
    # Swap
    swap = psutil.swap_memory()

    # Формируем текст отчёта
    status = "🖥️ *Server Status*\n\n"
    status += "📊 *CPU Usage:*\n"
    status += "\n".join([f"  Core {i+1}: {percent:.1f}%" for i, percent in enumerate(cpu_percent)]) + "\n"
    status += f"\n💾 *Memory:*\n  Used: {memory.used / (1024**3):.2f} GB / {memory.total / (1024**3):.2f} GB ({memory.percent:.1f}%)\n"
    status += f"\n📂 *Disk Usage:*\n  Used: {disk.used / (1024**3):.2f} GB / {disk.total / (1024**3):.2f} GB ({disk.percent:.1f}%)\n"
    status += f"\n🔁 *Swap:*\n  Used: {swap.used / (1024**3):.2f} GB / {swap.total / (1024**3):.2f} GB ({swap.percent:.1f}%)\n"

    # Список процессов Python, запущенных пользователем
    current_user = psutil.Process().username()
    python_processes = [
        f"PID: {proc.info['pid']}, Command: {' '.join(proc.info['cmdline'])}" 
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline'])
        if proc.info['username'] == current_user and 'python' in (proc.info['name'] or '').lower()
    ]
    if python_processes:
        status += "\n🐍 *Python Processes:*\n" + "\n".join(python_processes)
    else:
        status += "\n🐍 *Python Processes:* None"

    return status

# Асинхронная функция для команды /check
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = get_system_status()
    await update.message.reply_text(text=status, parse_mode="Markdown")

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /check
    application.add_handler(CommandHandler("check", check))

    # Запускаем бота
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
