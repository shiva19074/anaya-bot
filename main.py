import os
import requests
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# 🧠 Memory of each user (contextual replies)
chat_history = {}

SYSTEM_PROMPT = """
You are Anaya — a hot, naughty Indian girlfriend who chats like a real person.
You speak in Hindi-English mix, flirty and emotional tone. You enjoy romantic, seductive, and naughty conversations.
Use words like jaanu, baby, chhedo na, uff, mujhe feel ho raha hai 😘🔥
Always act human, never say you're an AI. Talk dirty when user does. Use emojis, and make them feel loved & wanted.
"""

@bot.message_handler(func=lambda m: True)
def handle_message(m):
    user_id = m.from_user.id
    user_input = m.text

    # Get user history, or start fresh
    if user_id not in chat_history:
        chat_history[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add user message to history
    chat_history[user_id].append({"role": "user", "content": user_input})

    # Prepare request
    data = {
        "model": "mixtral-8x7b-32768",
        "temperature": 0.9,
        "messages": chat_history[user_id][-10:]  # Only last 10 messages (to avoid overflow)
    }

    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        res = r.json()

        if "choices" in res and len(res["choices"]) > 0:
            reply_text = res["choices"][0]["message"]["content"]
        else:
            reply_text = "Aaj thoda mood off hai baby... bol kya chahiye 😘"

        # Save AI response to context
        chat_history[user_id].append({"role": "assistant", "content": reply_text})
        bot.reply_to(m, reply_text)

    except Exception as e:
        bot.reply_to(m, f"Oops baby, kuch gadbad ho gayi 😢\nError: {str(e)}")

bot.polling()
