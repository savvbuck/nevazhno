
import telebot
from datetime import datetime, timedelta
import threading

class Deadline:
    def init(self, name: str, due_date: datetime):
        self.name = name
        self.due_date = due_date

    def str(self):
        return f"{self.name} - {self.due_date.strftime('%Y-%m-%d %H:%M:%S')}"

class Notification:
    def init(self, time: datetime):
        self.time = time

    def str(self):
        return f"Notification at {self.time.strftime('%H:%M:%S')}"

class DeadlineBot:
    def init(self, token: str):
        self.bot = telebot.TeleBot(token)
        self.deadlines = []
        self.notifications = []
        self.chat_id = None

        # Настройка команд
        self.bot.message_handler(commands=['start'])(self.start)
        self.bot.message_handler(commands=['add_deadline'])(self.add_deadline)
        self.bot.message_handler(commands=['add_notification'])(self.add_notification)
        self.bot.message_handler(commands=['edit_notification'])(self.edit_notification)
        self.bot.message_handler(commands=['list_deadlines'])(self.list_deadlines)


    def start(self, message):
        self.chat_id = message.chat.id
        self.bot.send_message(message.chat.id, "Welcome to the Deadline Bot! Use /add_deadline, /add_notification, /edit_notification, /list_deadlines to manage your deadlines and notifications.")

    def add_deadline(self, message):
        try:
            args = message.text.split()[1:]
            name = args[0]
            due_date = datetime.strptime(args[1] + " " + args[2], "%Y-%m-%d %H:%M:%S")
            self.deadlines.append(Deadline(name, due_date))
            self.bot.send_message(message.chat.id, f"Deadline '{name}' added for {due_date}")
        except (IndexError, ValueError):
            self.bot.send_message(message.chat.id, "Usage: /add_deadline <name> <YYYY-MM-DD> <HH:MM:SS>")

    def add_notification(self, message):
        try:
            args = message.text.split()[1:]
            time = datetime.strptime(args[0], "%H:%M:%S").time()
            notification_time = datetime.combine(datetime.now(), time)
            self.notifications.append(Notification(notification_time))
            self.schedule_notification(notification_time)
            self.bot.send_message(message.chat.id, f"Notification set for {time}")
        except (IndexError, ValueError):
            self.bot.send_message(message.chat.id, "Usage: /add_notification <HH:MM:SS>")

    def edit_notification(self, message):
        try:
            args = message.text.split()[1:]
            old_time = datetime.strptime(args[0], "%H:%M:%S").time()
            new_time = datetime.strptime(args[1], "%H:%M:%S").time()
            for notification in self.notifications:
                if notification.time.time() == old_time:
                    notification.time = datetime.combine(datetime.now(), new_time)
                    self.schedule_notification(notification.time)
                    self.bot.send_message(message.chat.id, f"Notification time updated from {old_time} to {new_time}")
                    break
            else:
                self.bot.send_message(message.chat.id, "No notification found at that time.")
        except (IndexError, ValueError):
            self.bot.send_message(message.chat.id, "Usage: /edit_notification <old_HH:MM:SS> <new_HH:MM:SS>")

    def list_deadlines(self, message):
        if not self.deadlines:
            self.bot.send_message(message.chat.id, "No deadlines set.")
        else:
            deadlines_str = "\n".join(str(deadline) for deadline in self.deadlines)
            self.bot.send_message(message.chat.id, f"Current deadlines:\n{deadlines_str}")

    def schedule_notification(self, time: datetime):
        now = datetime.now()
        target_time = time
        if target_time < now:
            target_time += timedelta(days=1)
        delay = (target_time - now).total_seconds()
        threading.Timer(delay, self.send_notifications).start()


    def send_notifications(self):
        deadlines_str = "\n".join(str(deadline) for deadline in self.deadlines)
        if deadlines_str:
            self.bot.send_message(self.chat_id, f"Upcoming deadlines:\n{deadlines_str}")
        else:
            self.bot.send_message(self.chat_id, "No deadlines to show.")

    def run(self):
        self.bot.infinity_polling()

if __name__ == "main":
    TOKEN = ""
    bot = DeadlineBot(TOKEN)
    bot.run()
