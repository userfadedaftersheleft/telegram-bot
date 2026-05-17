import sqlite3
import random
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

TOKEN = "8967711024:AAGNd4F8G2mXue9nFojvgg47lHjhGyhmwQ8"

conn = sqlite3.connect("famtree.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    wallet INTEGER DEFAULT 1000,
    bank INTEGER DEFAULT 0,
    weapon TEXT DEFAULT 'Bite 🦷'
)
""")

conn.commit()

WEAPONS = {
    "Bite 🦷": 5000,
    "Punch 👊": 6000,
    "Kick 🦵": 7000,
    "Knife 🔪": 8000,
    "Bomber 💣": 10000
}

GIFS = [
    "https://media.tenor.com/3ZZm9Z9J3mAAAAAC/anime-fight.gif",
    "https://media.tenor.com/4tC6mK6s6lAAAAAC/anime-kill.gif",
    "https://media.tenor.com/mCiM7CmGGI4AAAAC/anime.gif"
]


def get_user(user):
    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user.id,)
    )

    data = cursor.fetchone()

    if not data:
        cursor.execute(
            "INSERT INTO users (user_id, name) VALUES (?, ?)",
            (user.id, user.first_name)
        )

        conn.commit()

        cursor.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user.id,)
        )

        data = cursor.fetchone()

    return data


async def start(update, context):
    get_user(update.effective_user)

    await update.message.reply_text(
        "FamTree style bot online 🎀"
    )


async def account(update, context):

    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    else:
        target = update.effective_user

    data = get_user(target)

    await update.message.reply_text(
        f"🎀 {target.first_name}'s Account\n\n💰 Wallet: ${data[2]}\n🏦 Bank: ${data[3]}\n🔫 Weapon: {data[4]}"
    )


async def daily(update, context):

    user = update.effective_user
    data = get_user(user)

    new_wallet = data[2] + 3000

    cursor.execute(
        "UPDATE users SET wallet=? WHERE user_id=?",
        (new_wallet, user.id)
    )

    conn.commit()

    await update.message.reply_text(
        "You earned $3000 🎀"
    )


async def kill(update, context):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to someone 🎀"
        )
        return

    user = update.effective_user
    target = update.message.reply_to_message.from_user

    weapon = random.choice(list(WEAPONS.keys()))
    gif = random.choice(GIFS)

    await update.message.reply_animation(
        animation=gif,
        caption=f"You killed {target.first_name} with {weapon} and earned $50000"
    )


async def rob(update, context):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to someone 🎀"
        )
        return

    user = update.effective_user
    target = update.message.reply_to_message.from_user

    amount = random.randint(1000, 100000)

    await update.message.reply_text(
        f"{user.first_name} robbed ${amount} from {target.first_name}"
    )


async def weapon(update, context):

    buttons = []

    for name, price in WEAPONS.items():

        buttons.append([
            InlineKeyboardButton(
                f"{name} - ${price}",
                callback_data=f"buy_{name}"
            )
        ])

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "Choose your weapon 🎀",
        reply_markup=keyboard
    )


async def button_handler(update, context):

    query = update.callback_query

    await query.answer()

    await query.message.reply_text(
        "Weapon purchased 🎀"
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler(["acc", "account"], account))
app.add_handler(CommandHandler("daily", daily))
app.add_handler(CommandHandler("kill", kill))
app.add_handler(CommandHandler("rob", rob))
app.add_handler(CommandHandler("weapon", weapon))

app.add_handler(
    CallbackQueryHandler(button_handler)
)

print("BOT STARTED")

app.run_polling()