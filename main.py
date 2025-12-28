import asyncio, json, os, random, time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging

def to_small_caps(text):
    normal = "abcdefghijklmnopqrstuvwxyz"
    small  = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"
    trans = str.maketrans(normal, small)
    return text.lower().translate(trans)

# ---------------------------
# CONFIG
# ---------------------------

TOKENS = [
    "8134557553:AAEDk0eu1HKdKYydtgW5Ico7lAjm5s7yNQM",
    "8597912574:AAHz4o5lKG2J6MvfHIOvfD5SqmX1pAmsjNg",
]

OWNER_ID = 8453291493
SUDO_FILE = "susdo.json"

# ---------------------------
# RAID TEXTS
# ---------------------------

RAID_TEXTS = [
    "CHUDAI ARC STARTED🐷🐷",
    "KYA REE RNDI  🐗🐗",
    "BAAP KO BHEJ🐸🐸",
    "KUTIYA RAAND 🙈🙈",
    "TMR HAINA  🐥🐥",
]

RAID_TEXTS = [to_small_caps(t) for t in RAID_TEXTS]

# ---------------------------
# NCEMO EMOJIS
# ---------------------------

NCEMO_EMOJIS = [
    "😋","😝","😜","🤪","😑","🤫","🤭","🥱","🤗","😡"
]

# ---------------------------
# GLOBAL STATE
# ---------------------------

if os.path.exists(SUDO_FILE):
    try:
        with open(SUDO_FILE, "r") as f:
            _loaded = json.load(f)
        SUDO_USERS = set(int(x) for x in _loaded)
    except Exception:
        SUDO_USERS = {OWNER_ID}
else:
    SUDO_USERS = {OWNER_ID}
    with open(SUDO_FILE, "w") as f:
        json.dump(list(SUDO_USERS), f)

def save_sudo():
    with open(SUDO_FILE, "w") as f:
        json.dump(list(SUDO_USERS), f)

group_tasks = {}
slide_targets = set()
slidespam_targets = set()
swipe_mode = {}
apps, bots = [], []
delay = 1

logging.basicConfig(level=logging.INFO)

# ---------------------------
# DECORATORS
# ---------------------------

def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid not in SUDO_USERS:
            return await update.message.reply_text("❌ You are not SUDO.")
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid != OWNER_ID:
            return await update.message.reply_text("❌ Only Owner can do this.")
        return await func(update, context)
    return wrapper

# ---------------------------
# LOOP FUNCTION
# ---------------------------

async def bot_loop(bot, chat_id, base, mode):
    i = 0
    while True:
        try:
            if mode == "raid":
                text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}"
            else:
                text = f"{base} {NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]}"
            await bot.set_chat_title(chat_id, text)
            i += 1
            await asyncio.sleep(delay)
        except Exception as e:
            print(f"[WARN] Bot error: {e}")
            await asyncio.sleep(2)

# ---------------------------
# COMMANDS
# ---------------------------

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💗 Welcome to Mafia Bot!")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /gcnc /ncemo /stopall")

@only_sudo
async def gcnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    group_tasks.setdefault(chat_id, {})
    for bot in bots:
        if bot.id not in group_tasks[chat_id]:
            task = asyncio.create_task(bot_loop(bot, chat_id, base, "raid"))
            group_tasks[chat_id][bot.id] = task
    await update.message.reply_text("GC RAID STARTED")

@only_sudo
async def stopall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for chat_id in group_tasks:
        for task in group_tasks[chat_id].values():
            task.cancel()
    group_tasks.clear()
    await update.message.reply_text("ALL STOPPED")

# ---------------------------
# BUILD APP
# ---------------------------

def build_app(token):
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("gcnc", gcnc))
    app.add_handler(CommandHandler("stopall", stopall))
    return app

async def run_all_bots():
    for token in TOKENS:
        app = build_app(token)
        apps.append(app)
        bots.append(app.bot)

    for app in apps:
        await app.initialize()
        await app.start()
        await app.bot.initialize()

    print("✅ ALL BOTS RUNNING")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(run_all_bots())
