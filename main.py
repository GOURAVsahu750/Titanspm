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
    "TERI BUA KE CHUCHE🦜🦜",
    "TERI CHACHI KI CHUUT  🐍🐍",
    "TERI DADI KA BHOSDA 😋👈",
    "TERI NANI KA BUUR 🐎🐎",
    "TERI BHEN KE NUDES  🙀🙀",
    "TERI DIDI KI GAAND  🦎🦎",
    "TERI CHOTTI BHEN KI KAMAR  🐕🐕",
    "TERI BNDI KI GULABI   🐁🐁",
    "TERI BADI MUMMY KE DUDU🦙🦙",
    "TERI  MAA KI NAUGHTY AAWQZ  🦦🦦",
    "TERI MUMMY KE NIPPLE CHUSU😋👈",
    "TERI BHEN KI BHOSDI PE LAAAT MAARU",
    "TERI BHEN MULLI RAAND",
    "TERI MKB PE MUTHI MARU",
    "TERI CHACHI KO OYO LE JAU",
    "TERI MKC CUTE HAI",
    "TERI BHEN KA FIGURE HOT HAI",
    "TERI DADI KO CHUMA",
    "TERE BAAP KA NAAM SANKI",
    "BOLL SANKI ALWAYS KOKA",
    "BADMASH BANEGA TATTE",
    "KYA REE BIKHARI BETA",
    "TMCCC BADI MAJBUT",
    "HEY RNDI PUTAR",
    "TERI MA PUNJAB ME CHUDE",
    "TERI MA KHALISTANI",
    "TERI BUA BOLE SANKI KOKA",
    "KYA REE GAREEB SCRIPT DU?",
    "BIKHARI KA LADKA",
    "KILAS RNDI KE LADKE",
    "HAHAHA MAZA AAGYA CHUD KE",
    "LOL TERI MA RNDI",
    "TERI MA KA BALTKAAR KRDU",
    "HIZDA",
    "PUJA KR MERI",
    "KUTIYA KE LADKE",
    "SCRIPT KENG SANKI HAI",
    "TERI BUA KI KALI CHUT",
    "TMR BHOSDI WALI",
    "HARAMZADI HAI TERI MA",
    "TERI MAA KA KOTHA BAND",
    "TERI BHEN KI BHOSDI BETAAA ZII",
    "JHULA JHUL PAR BAAP KO MAT BHUL",
    "TERI BHEN KI KACHI WOW",
    " TMKCLOCK",
    "HAKLE RAAND",
    "CVR TOH KR MERE LADKE",
    "TERI MA PAID SERVICE WALI RAND",
    "GAWAR JHATU",
    "7 INCH KE LAUDE SE CHUD",
    "OYE CHOTTI LULI WALE",
    "BAUNE",
    "TERI BHEN KE SATH MMS VIRAL",
    "TERI BHEN MERI DIWANI",
    "TERI MA KO AMERICA ME CHODU",
    "TERI BHEN KO LY REE",
    "TERI MAA KE SATH XXX",
    "TERI MA KA BHOSDAAA BABU",
    "SCRIPT REFRESH KR",
    "GULAAM",
    "BALATKARI HU MAI",
    "JAA MAA CHUDA",
    "TYPE MAT KR REE RNDY",
    "TMKC KO THAPPAD",
    "HEHEHE RNDY KA",
    "DELAY KAM KR CHAMAR",
    "TERI MA KI CHIKHE NIKALU",
    "TMKC BLUE BLUE BLUE",
    "TMKC GULABI GULABI",
    "GANDMARE",
    "WAH TERI MA RNDY",
    "BETA SPEED LA",
    "FAAST KR RNDIKE",
    "BBC SE CHUD",
    "CMD DAAL CHAKKE",
    "TERI MA KI BUUR BUR",
    "FAUJI CUTTING WALE CHAKKE",
]

RAID_TEXTS = [to_small_caps(t) for t in RAID_TEXTS]

# ---------------------------
# NCEMO EMOJIS
# ---------------------------
NCEMO_EMOJIS = [
    "😋","😝","😜","🤪","😑","🤫","🤭","🥱","🤗","😡","😠","😤",
    "😮‍💨","🙄","😒","🥶","🥵","🤢","😎","🥸",
    "😹","💫","😼","😽","🙀","😿","😾",
    "🙈","🙉","🙊",
    "⭐","🌟","✨","⚡","💥","💨",
    "💛","💙","💜","🤎","🤍","💘","💝"
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
with open(SUDO_FILE, "w") as f: json.dump(list(SUDO_USERS), f)

def save_sudo():
    with open(SUDO_FILE, "w") as f: json.dump(list(SUDO_USERS), f)

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
            print(f"[WARN] Bot error in chat {chat_id}: {e}")
            await asyncio.sleep(2)

# ---------------------------
# COMMANDS
# ---------------------------
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💗 Welcome to Mafia Bot!\nUse /help to see all commands.")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        " Bot Help Menu\n\n"
        "⚡ GC Loops:\n"
        "/gcnc <text>\n/ncemo <text>\n/stopgcnc\n/stopall\n/delay <sec>\n/status\n\n"
        "🎯 Slide & Spam:\n"
        "/targetslide (reply)\n/stopslide (reply)\n/slidespam (reply)\n/stopslidespam (reply)\n\n"
        "⚡ Swipe Mode:\n"
        "/swipe <name>\n/stopswipe\n\n"
        "👑 SUDO Management:\n"
        "/addsudo (reply)\n/delsudo (reply)\n/listsudo\n\n"
        "🛠 Misc:\n/myid\n/ping"
    )

async def ping_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("🏓 Pinging...")
    end_time = time.time()
    latency = int((end_time - start_time) * 1000)
    await msg.edit_text(f"🏓 Pong! ✅ {latency} ms")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your ID: {update.effective_user.id}")

# ---------------------------
# BUILD APP & RUN
# ---------------------------
def build_app(token):
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping_cmd))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_replies))
    return app

async def run_all_bots():
    global apps, bots
    for token in TOKENS:
        if token.strip():
            app = build_app(token)
            apps.append(app)
            bots.append(app.bot)

    for app in apps:
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

    print("All bots running...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(run_all_bots())