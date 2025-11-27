import os
import sqlite3
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, ChatMemberHandler, CommandHandler, ContextTypes
import asyncio

# Environment variables'dan al (Render.com için)
BOT_TOKEN = os.getenv('8445241488:AAFKvQUiX69Qu3E_Lx_ufr35sJPDHa4eW4w', 'BURAYA_TOKENINIZI_YAZIŞTIRIN')
GROUP_CHAT_ID = int(os.getenv('-1003339131587', -1003339131587))
PERSONAL_CHAT_ID = int(os.getenv('5563748743', 5563748743))

# Veritabanı oluştur
def init_db():
    conn = sqlite3.connect('uyeler.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS uyeler
                 (user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  first_name TEXT,
                  join_date TEXT,
                  notified INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# Yeni üye ekle
def add_member(user_id, username, first_name):
    conn = sqlite3.connect('uyeler.db')
    c = conn.cursor()
    join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c.execute("INSERT OR IGNORE INTO uyeler (user_id, username, first_name, join_date) VALUES (?, ?, ?, ?)",
                  (user_id, username, first_name, join_date))
        conn.commit()
        print(f"✅ Yeni üye eklendi: {first_name} (@{username}) - {join_date}")
    except Exception as e:
        print(f"❌ Hata: {e}")
    conn.close()

# Üye değişikliklerini takip et
async def track_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    
    if result.new_chat_member.status in ["member", "administrator"]:
        if result.old_chat_member.status in ["left", "kicked"]:
            user = result.new_chat_member.user
            user_id = user.id
            username = user.username or "kullanıcı_adı_yok"
            first_name = user.first_name or "İsimsiz"
            
            add_member(user_id, username, first_name)