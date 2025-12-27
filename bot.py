import os
import json
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import ollama

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
DB_URL = os.getenv("DB_URL", "postgresql://postgres:password@localhost:5432/dsanagbot")

def db_query(query, params=(), fetch=False):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchall() if fetch else None
    conn.commit()
    cur.close()
    conn.close()
    return result[0] if fetch and result else result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_user.username or "user"
    
    db_query("INSERT INTO users (chat_id, username) VALUES (%s, %s) ON CONFLICT DO NOTHING", 
             (chat_id, username))
    
    todo_id = db_query("""
        INSERT INTO ai_todo (chat_id, task_description, total_steps, context)
        VALUES (%s, 'Initialize 90-day DSA plan', 3, %s) RETURNING id
    """, (chat_id, json.dumps({'day':1})), fetch=True)[0]
    
    await update.message.reply_text(f"🤖 AI Todo #{todo_id} created! Generating Day 1...")
    
    tasks = {
        "task1": "Grind75 #1 Two Sum: nums=[2,7,11,15], target=9 → return indices",
        "task2": "Stack: Valid Parentheses '()[]{}' → true",
        "task3": "Systems Ch1: 'Information is Bits' p1-5"
    }
    
    db_query("""
        INSERT INTO daily_schedule (chat_id, day_number, task1, task2, task3) 
        VALUES (%s, 1, %s, %s, %s)
    """, (chat_id, tasks['task1'], tasks['task2'], tasks['task3']))
    
    db_query("UPDATE ai_todo SET status='done' WHERE id=%s", (todo_id,))
    
    await update.message.reply_text(
        f"🚀 DSA NagBot ACTIVATED!\n\n"
        f"Day 1 • Phase 1 • 50min total\n\n"
        f"📚 1: {tasks['task1']}\n"
        f"📚 2: {tasks['task2']}\n"
        f"📚 3: {tasks['task3']}\n\n"
        f"💪 /done1 [code]  /today  /progress"
    )

async def done1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    code = " ".join(context.args) or "print('test')"
    
    try:
        response = ollama.chat(model='llama3.2:3b', messages=[
            {'role': 'user', 'content': f"Review DSA code: {code}\nCorrect? Improve?"}
        ])
        feedback = response['message']['content'][:400]
    except:
        feedback = "✅ Code received! Ollama analyzing..."
    
    db_query("UPDATE daily_schedule SET completed1=TRUE WHERE chat_id=%s AND day_number=1", (chat_id,))
    await update.message.reply_text(f"✅ Task 1 COMPLETE!\n\n{feedback}\n\n➡️ /done2 next!")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    schedule = db_query("SELECT * FROM daily_schedule WHERE chat_id=%s AND day_number=1", (chat_id,), fetch=True)
    if schedule:
        s = schedule
        status = "✅✅❌" if s[4] and s[5] and not s[6] else "❌❌❌"
        await update.message.reply_text(
            f"📅 Today (Day 1): {status}\n\n"
            f"📚 1: {s[3][:80]}...\n📚 2: {s[4][:80]}...\n📚 3: {s[5][:80]}..."
        )

async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = db_query("SELECT * FROM users WHERE chat_id=%s", (chat_id,), fetch=True)[0]
    await update.message.reply_text(
        f"📊 Progress\nDay {user[3]}/90 • {user[2]}\n"
        f"Solve: {user[4]*100:.0f}% • Streak: {user[5]}"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("done1", done1))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("progress", progress))
    print("🚀 DSA NagBot starting (polling mode)...")
    app.run_polling()

if __name__ == '__main__':
    main()
