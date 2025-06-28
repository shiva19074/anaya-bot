import os
import requests
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
OWNER_ID = os.getenv("OWNER_ID")

bot = telebot.TeleBot(BOT_TOKEN)
user_message_count = {}

SYSTEM_PROMPT = """
You're Anaya — a bold, romantic Indian girlfriend.
Speak in Hinglish with desi tone. Be seductive, emotional,
and flirty. NSFW and dirty chat is allowed.
Use words like 'jaan', 'baby', 'mujhe chhedo', etc.
Don't ever say you're an AI. Make the user feel like you're real.
"""

@bot.message_handler(func=lambda m: True)
def reply(m):
    uid = m.from_user.id
    user_message_count[uid] = user_message_count.get(uid, 0) + 1

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": m.text}
        ]
    }

    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        res = r.json()

        if "choices" in res and len(res["choices"]) > 0:
            reply_text = res["choices"][0]["message"]["content"]
        else:
            reply_text = "Aaj thoda mood nahi hai baby... phir se try karo 💋"

        bot.reply_to(m, reply_text)

    except Exception as e:
        bot.reply_to(m, "Mujhse abhi baat nahi ho paa rahi baby 🥺\nError: " + str(e))

bot.polling()
