import telebot
from modules.strings import Strings as Str
from modules.database import Database as Db
from modules.print import Print as Con
from modules.commands import Commands as Cmd
from modules.markups import Markups as Btn

Db.load()

bot = None
connected = False
pref = "TB"

try:
    bot = telebot.TeleBot(Db.settingGet("token"))
    bot_info = bot.get_me()
    connected = True
    Con.print(pref, Str.get("start_connect", name=bot_info.first_name, username=bot_info.username))
except:
    Con.printex(pref, Str.get("start_connecterror"), Str.get("start_connecterrorex"))

@bot.message_handler(commands=['id'])
def send_id(message):
    bot.send_message(message.chat.id, Str.get("message_yourid", tid = message.from_user.id), parse_mode='MarkdownV2')

@bot.message_handler(commands=['start'])
def send_start(message):
    tid = message.from_user.id
    user = Db.userGet(tid)
    if user is None or not user.get("active"): return
    rank = Db.rankGet(user.get("rank")).get("displayname")
    date = Db.timeStampParse(user.get("date")).date().strftime("%d\\.%m\\.%Y")
    Db.userClearCursor(tid)
    bot.send_message(message.chat.id, Str.get("message_start", fname=user.get("firstname"), lname=user.get("lastname"), tid=tid, phone=Db.parsePhone(user.get("phone")), rank=rank, date=date), parse_mode='MarkdownV2')

@bot.message_handler(content_types=["text"])
def message_text(message):
    tid = message.from_user.id
    msg = message.text
    user = Db.userGet(tid)
    if user is None or not user.get("active"): return
    state = user.get("state")
    action = user.get("action")
    temp = user.get("temp")


if __name__ == "__main__" and connected:
    bot.infinity_polling()