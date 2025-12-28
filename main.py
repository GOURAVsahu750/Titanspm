import asyncio, json, os, random, time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging

def to_small_caps(text):
    normal = "abcdefghijklmnopqrstuvwxyz"
    small  = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"
    return text.lower().translate(str.maketrans(normal, small))

# ---------------------------
# CONFIG
# ---------------------------
TOKENS = [
    "8134557553:AAEDk0eu1HKdKYydtgW5Ico7lAjm5s7yNQM",
    "8597912574:AAHz4o5lKG2J6MvfHIOvfD5SqmX1pAmsjNg",
]

OWNER_ID = 8453291493
SUDO_FILE = "susdo.json"

logging.basicConfig(level=logging.INFO)

# ---------------------------
# SAFE SUDO FILE CREATE
# ---------------------------
if not os.path.exists(SUDO_FILE):
    with open(SUDO_FILE, "w") as f:
        json.dump([OWNER_ID], f)

try:
    with open(SUDO_FILE, "r") as f:
        SUDO_USERS = set(map(int, json.load(f)))
except Exception:
    SUDO_USERS = {OWNER_ID}
    with open(SUDO_FILE, "w") as f:
        json.dump(list(SUDO_USERS), f)

def save_sudo():
    with open(SUDO_FILE, "w") as f:
        json.dump(list(SUDO_USERS), f)

# ---------------------------
# DATA
# ---------------------------
RAID_TEXTS = [to_small_caps("TEST RAID")]
NCEMO_EMOJIS = ["🔥","💥","⚡"]

group_tasks = {}
apps, bots = [], []
delay = 1

# ---------------------------
# DECORATORS
# ---------------------------
def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in SUDO_USERS:
            return await update.message.reply_text("❌ Not sudo")
        return await func(update, context)
    return wrapper

# ---------------------------
# COMMANDS
# ---------------------------
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot started")

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = time.time()
    m = await update.message.reply_text("🏓")
    await m.edit_text(f"Pong {int((time.time()-t)*1000)}ms")

# ---------------------------
# BUILD APP
# ---------------------------
def build_app(token):
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    return app

# ---------------------------
# RUN ALL BOTS (FIXED)
# ---------------------------
async def run_all_bots():
    for token in TOKENS:
        app = build_app(token)
        apps.append(app)

    await asyncio.gather(*[app.run_polling() for app in apps])

if __name__ == "__main__":
    asyncio.run(run_all_bots())
