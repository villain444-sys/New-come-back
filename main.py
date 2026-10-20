import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, io, qrcode
from flask import Flask
from threading import Thread

# BOT CONFIGURATION
BOT_TOKEN = "8777634130:AAEfZpoDgpx5vrjhj232poiFXt2HVw1ict8"  # Token reset kiya ho toh naya yahan daalein
CHANNEL_USERNAME = "villain_ott_hub"
UPI_ID = "rishabhx07@fam"
ADMIN_ID = 8692723368
ADMIN_USERNAME = "ishowvillain"
CHANNEL_LINK = "https://t.me/villain_ott_hub"
USERS_FILE = "users.txt"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "🚀 V-Premium Bot is Alive & Running Successfully!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run_flask).start()

PLAN_DATA = {
    "buy_netflix_mob": ("Netflix 1M (📱 Mobile)", 99),
    "buy_netflix_tv": ("Netflix 1M (📺 TV)", 99),
    "buy_netflix_pc": ("Netflix 1M (💻 Laptop/PC)", 99),
    "buy_prime1_yes": ("Amazon Prime 1M (On Mail ✅)", 70),
    "buy_prime1_no": ("Amazon Prime 1M (On Mail ❌)", 70),
    "buy_prime6_yes": ("Amazon Prime 6M (On Mail ✅)", 299),
    "buy_prime6_no": ("Amazon Prime 6M (On Mail ❌)", 299),
    "buy_spotify_yes": ("Spotify 3M (On Mail ✅)", 60),
    "buy_spotify_no": ("Spotify 3M (On Mail ❌)", 60),
    "buy_hotstar_yes": ("JioHotstar 1M (On Mail ✅)", 50),
    "buy_hotstar_no": ("JioHotstar 1M (On Mail ❌)", 50),
    "buy_crunchy_yes": ("Crunchyroll 1M (On Mail ✅)", 50),
    "buy_crunchy_no": ("Crunchyroll 1M (On Mail ❌)", 50),
    "buy_youtube": ("YouTube Premium (1 Month)", 30),
    "buy_gemini": ("Gemini Advanced (18 Months)", 80)
}

def generate_dynamic_qr(upi_id, amount, name="V-Premium"):
    upi_url = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    bio = io.BytesIO()
    bio.name = 'qr.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    return bio

def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")

def check_sub(user_id):
    try:
        chat_handle = f"@{CHANNEL_USERNAME}"
        status = bot.get_chat_member(chat_handle, user_id).status
        return status in ['member', 'creator', 'administrator']
    except Exception as e:
        print(f"Check Sub Error: {e}")
        return False

def main_home_menu():
    m = InlineKeyboardMarkup(row_width=1)
    m.add(
        InlineKeyboardButton("🛍️ Explore Products & Plans 🛍️", callback_data="open_products"),
        InlineKeyboardButton("💬 Customer Support / Help 🛠️", url=f"https://t.me/{ADMIN_USERNAME}"),
        InlineKeyboardButton("⭐ Client Vouches & Proofs 🔥", url=CHANNEL_LINK)
    )
    return m

def products_menu():
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("🎬 Netflix - ₹99", callback_data="menu_netflix"),
        InlineKeyboardButton("📦 Amazon Prime", callback_data="menu_prime"),
        InlineKeyboardButton("🎵 Spotify (3M) - ₹60", callback_data="menu_spotify"),
        InlineKeyboardButton("▶️ YouTube Prem - ₹30", callback_data="buy_youtube"),
        InlineKeyboardButton("🌐 JioHotstar - ₹50", callback_data="menu_hotstar"),
        InlineKeyboardButton("🍥 Crunchyroll - ₹50", callback_data="menu_crunchyroll")
    )
    m.add(InlineKeyboardButton("🤖 Gemini (18M) - ₹80", callback_data="buy_gemini"))
    m.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_main"))
    return m

@bot.message_handler(commands=['start'])
def send_welcome(message):
    uid = message.from_user.id
    save_user(uid)
    if check_sub(uid):
        txt = (
            "✨ *WELCOME TO V-PREMIUM STORE!* 🎉\n\n"
            "🔥 *Yahan Milte Hain Sabse Saste, 100% Genuine Aur Fully Trusted Premium Accounts!*\n\n"
            "⚡ *Instant Delivery | Full Warranty | VIP Support*\n\n"
            "👇 *Niche Diye Gaye Buttons Se Apna Option Select Karein:*"
        )
        bot.send_message(message.chat.id, txt, reply_markup=main_home_menu(), parse_mode="Markdown")
    else:
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📢 Join Official Channel Now 🔥", url=CHANNEL_LINK),
            InlineKeyboardButton("✅ Check / Verify Subscription ✔️", callback_data="verify_sub")
        )
        warn = (
            "⚠️ *HOLD ON! ACCESS LOCKED!* 🔒\n\n"
            "📢 *Bot Ko Use Karne Ke Liye Pehle Hamara Official Channel Join Karna Zaroori Hai!*\n\n"
            "👇 *Niche Button Par Click Karke Channel Join Karein Aur Phir 'Check / Verify' Dabayein:*"
        )
        bot.send_message(message.chat.id, warn, reply_markup=m, parse_mode="Markdown")

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Aap Yeh Command Use Nahi Kar Sakte!")
        return
    msg = bot.send_message(message.chat.id, "📢 Sabhi Users Ko Bhejne Ke Liye Message Ya Photo Type Karein:")
    bot.register_next_step_handler(msg, send_broadcast_to_all)

def send_broadcast_to_all(message):
    if not os.path.exists(USERS_FILE):
        bot.send_message(message.chat.id, "❌ Koi User Nahi Mila!")
        return
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    s, fl = 0, 0
    bot.send_message(message.chat.id, f"🚀 Broadcast Shuru... Total Users: {len(users)}")
    for uid in users:
        try:
            if message.photo:
                bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption or "")
            else:
                bot.send_message(uid, message.text)
            s += 1
        except Exception:
            fl += 1
    bot.send_message(message.chat.id, f"✅ BROADCAST COMPLETE!\n🟢 Success: {s}\n🔴 Failed: {fl}")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    uid = call.from_user.id
    save_user(uid)
    
    if call.data == "verify_sub":
        if check_sub(uid):
            bot.delete_message(cid, mid)
            txt = "🎉 *VERIFICATION SUCCESSFUL!* ✅\n\n✨ *Ab Aap Hamare Saare VIP Plans Explore Kar Sakte Hain.*\n\n👇 *Niche Se Option Select Karein:*"
            bot.send_message(cid, txt, reply_markup=main_home_menu(), parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ Bhai Pehle Channel Join Karein!", show_alert=True)
            
    elif call.data == "open_products":
        txt = "🛍️ *V-PREMIUM STORE DASHBOARD* ⚡\n\n💎 *Sabhi Plans 100% Working Aur Guaranteed Hain!*\n\n👇 *Apna Pasandida OTT / AI Plan Select Karein:*"
        bot.edit_message_text(txt, cid, mid, reply_markup=products_menu(), parse_mode="Markdown")

    elif call.data == "back_main":
        txt = "✨ *WELCOME BACK TO V-PREMIUM STORE!* 🎉\n\n🔥 *Sabse Saste Aur 100% Reliable Premium Accounts.*\n\n👇 *Niche Se Option Select Karein:*"
        bot.edit_message_text(txt, cid, mid, reply_markup=main_home_menu(), parse_mode="Markdown")

    elif call.data == "menu_netflix":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📱 Mobile - ₹99", callback_data="buy_netflix_mob"),
            InlineKeyboardButton("📺 TV - ₹99", callback_data="buy_netflix_tv"),
            InlineKeyboardButton("💻 Laptop / PC - ₹99", callback_data="buy_netflix_pc"),
            InlineKeyboardButton("🔙 Back to Products", callback_data="open_products")
        )
        bot.edit_message_text("🎬 *NETFLIX PREMIUM (1M - 4K)* 🔥\n\n👇 *Apna Device Select Karein:*", cid, mid, reply_markup=m, parse_mode="Markdown")

    elif call.data == "menu_prime":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📦 1 Month Plan - ₹70", callback_data="prime_dur_1"),
            InlineKeyboardButton("📦 6 Months Plan - ₹299", callback_data="prime_dur_6"),
            InlineKeyboardButton("🔙 Back to Products", callback_data="open_products")
        )
        bot.edit_message_text("📦 *AMAZON PRIME VIDEO* 🎬\n\n👇 *Apna Plan Duration Select Karein:*", cid, mid, reply_markup=m, parse_mode="Markdown")

    elif call.data == "prime_dur_1":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_prime1_yes"),
            InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_prime1_no"),
            InlineKeyboardButton("🔙 Back to Prime Plans", callback_data="menu_prime")
        )
        bot.edit_message_text("📦 *AMAZON PRIME (1 MONTH) - ₹70* ⚡\n\n👇 *Apna Option Select Karein:*", cid, mid, reply_markup=m, parse_mode="Markdown")

    elif call.data == "prime_dur_6":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_prime6_yes"),
            InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_prime6_no"),
            InlineKeyboardButton("🔙 Back to Prime Plans", callback_data="menu_prime")
        )
        bot.edit_message_text("📦 *AMAZON PRIME (6 MONTHS) - ₹299* ⚡\n\n👇 *Apna Option Select Karein:*", cid, mid, reply_markup=m, parse_mode="Markdown")

    elif call.data == "menu_spotify":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_spotify_yes"),
            InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_spotify_no"),
            InlineKeyboardButton("🔙 Back to Products", callback_data="open_products")
        )
        bot.edit_message_text("🎵 *SPOTIFY PREMIUM (3M) - ₹60* 🎧\n\n👇 *Apna Option Select Karein:*", cid, mid, reply_markup=m, parse_mode="Markdown")

    elif call.data == "menu_hotstar":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_hotstar_yes"),
            InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_hotstar_no"),
            InlineKeyboardButton("🔙 Back to Products", callback_data="open_products")
        )
        bot.edit_message_text("🌐 *JIOHOTSTAR PREMIUM (1M) - ₹50* 🔥\n\n👇 *Apna Option Select Karein:*", cid, mid, reply_markup=m, parse_mode="Markdown")

    elif call.data == "menu_crunchyroll":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_crunchy_yes"),
            InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_crunchy_no"),
            InlineKeyboardButton("🔙 Back to Products", callback_data="open_products")
        )
        bot.edit_message_text("🍥 *CRUNCHYROLL (1M) - ₹50* ⚔️\n\n👇 *Apna Option Select Karein:*", cid, mid, reply_markup=m, parse_mode="Markdown")

    elif call.data.startswith("buy_"):
        p_name, p_amt = PLAN_DATA.get(call.data, ("VIP Plan", 30))
        sel = f"{p_name} - ₹{p_amt}"
        txt = f"🛒 *ORDER CONFIRMATION* ⚡\n\n📦 Plan: {sel}\n💰 Total Amount: ₹{p_amt}\n\nPayment Ke Liye '✅ Pay Now' Par Click Karein:"
        m = InlineKeyboardMarkup(row_width=2)
        m.add(
            InlineKeyboardButton("✅ Pay Now 💸", callback_data=f"pay_{call.data}"),
            InlineKeyboardButton("❌ Cancel", callback_data="open_products")
        )
        bot.edit_message_text(txt, cid, mid, reply_markup=m)

    elif call.data.startswith("pay_"):
        code = call.data.replace("pay_", "")
        p_name, amt = PLAN_DATA.get(code, ("VIP Plan", 30))
        sel = f"{p_name} - ₹{amt}"
        cap = (
            f"🛒 YOUR SELECTED PLAN:\n👉 {sel}\n\n"
            f"📲 Upar QR Code Scan Karke ₹{amt} Payment Karein\n\n"
            f"🏦 UPI ID: {UPI_ID}\n\n"
            f"📸 IMPORTANT STEP:\n"
            f"Payment hone ke turant baad screenshot (photo ya file) yahan send karein! 🚀✅"
        )
        try:
            qr = generate_dynamic_qr(UPI_ID, amt)
            bot.delete_message(cid, mid)
            msg = bot.send_photo(cid, qr, caption=cap)
            bot.register_next_step_handler(msg, process_screenshot, sel)
        except Exception:
            bot.delete_message(cid, mid)
            msg = bot.send_message(cid, cap)
            bot.register_next_step_handler(msg, process_screenshot, sel)

    elif call.data.startswith("accept_mail_"):
        t_uid = call.data.split("_")[2]
        try:
            txt = (
                "🎉 *PAYMENT VERIFIED!* ✅\n\n"
                "📧 *PLEASE SEND YOUR EMAIL / GMAIL ID FOR ACTIVATION*\n"
                "*(Apni Mail ID niche type karke send karein)* 👇"
            )
            msg = bot.send_message(t_uid, txt, parse_mode="Markdown")
            bot.register_next_step_handler(msg, receive_user_gmail)
            bot.edit_message_caption(chat_id=cid, message_id=mid, caption=call.message.caption + "\n\n✅ *Status: Accepted (Waiting for user's mail)*")
        except Exception as e:
            bot.send_message(cid, f"❌ User tak message nahi gaya: {e}")

    elif call.data.startswith("reply_pass_"):
        t_uid = call.data.split("_")[2]
        msg = bot.send_message(cid, "🔑 Is user ke liye ID / Password type karke bhejo:")
        bot.register_next_step_handler(msg, send_id_to_user, t_uid)
        
    elif call.data.startswith("reject_"):
        t_uid = call.data.split("_")[1]
        try:
            bot.send_message(t_uid, "❌ *PAYMENT VERIFICATION FAILED!*\n\nAapka payment screenshot verify nahi ho paya. Kripya sahi screenshot dobara bhejein ya admin se contact karein.", parse_mode="Markdown")
            bot.edit_message_caption(chat_id=cid, message_id=mid, caption=call.message.caption + "\n\n❌ *Status: Rejected*")
        except Exception:
            bot.send_message(cid, "❌ User tak message deliver nahi hua.")

    elif call.data.startswith("inv_sent_"):
        t_uid = call.data.split("_")[2]
        try:
            msg_user = "🎉 *Your invitation has been sent!* 💌\n\nPlease check your mail inbox or spam folder to accept it. Enjoy your Premium! ❤️🙏"
            bot.send_message(t_uid, msg_user, parse_mode="Markdown")
            bot.edit_message_text(f"{call.message.text}\n\n✅ *Status: Invitation Sent (User Notified)*", cid, mid)
        except Exception:
            bot.send_message(cid, "❌ User tak message nahi gaya.")

    elif call.data.startswith("mail_prob_"):
        t_uid = call.data.split("_")[2]
        try:
            msg_user = f"⚠️ *Aapki Mail mein kuch problem hai, please admin se contact karein:* @{ADMIN_USERNAME}"
            bot.send_message(t_uid, msg_user)
            bot.edit_message_text(f"{call.message.text}\n\n⚠️ *Status: Problem Reported to User*", cid, mid)
        except Exception:
            bot.send_message(cid, "❌ User tak message nahi gaya.")

def process_screenshot(message, selected_plan):
    uid = message.from_user.id
    uname = message.from_user.username or "None"
    
    file_id = None
    is_doc = False
    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.document:
        file_id = message.document.file_id
        is_doc = True
    else:
        msg = bot.send_message(message.chat.id, "⚠️ Text mat bhejo! Payment ka Screenshot bhejo (Photo ya File).")
        bot.register_next_step_handler(msg, process_screenshot, selected_plan)
        return

    is_mail_plan = ("on mail ✅" in selected_plan.lower()) or ("youtube" in selected_plan.lower())
    
    cap = (
        f"🔔 NEW PAYMENT SCREENSHOT!\n\n"
        f"📦 Plan: {selected_plan}\n"
        f"👤 User: @{uname} (ID: {uid})\n\n"
        f"Action select karein:"
    )
    
    m = InlineKeyboardMarkup(row_width=2)
    if is_mail_plan:
        m.add(
            InlineKeyboardButton("✅ Accept", callback_data=f"accept_mail_{uid}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{uid}")
        )
    else:
        m.add(
            InlineKeyboardButton("🔑 Send ID/Pass", callback_data=f"reply_pass_{uid}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{uid}")
        )
    
    try:
        if is_doc:
            bot.send_document(ADMIN_ID, file_id, caption=cap, reply_markup=m)
        else:
            bot.send_photo(ADMIN_ID, file_id, caption=cap, reply_markup=m)
            
        bot.send_message(message.chat.id, "✅ SCREENSHOT RECEIVED!\n\n⏳ Admin verification kar raha hai, kripya thoda wait karein!")
    except Exception as e:
        print(f"Error forwarding screenshot to Admin ({ADMIN_ID}): {e}")
        bot.send_message(message.chat.id, "❌ Screenshot bhejne mein problem aayi. Make sure karein Admin ne bot ko pehle /start kiya ho!")

def receive_user_gmail(message):
    uid = message.from_user.id
    uname = message.from_user.username or "None"
    user_gmail = message.text

    alert = (
        f"📩 *RECEIVED MAIL ADDRESS!* ⚡\n\n"
        f"👤 *User:* @{uname} (`{uid}`)\n"
        f"📧 *Mail:* `{user_gmail}`\n\n"
        f"Action select karein:"
    )
    
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("✅ Invitation Sent", callback_data=f"inv_sent_{uid}"),
        InlineKeyboardButton("❌ Some Problem", callback_data=f"mail_prob_{uid}")
    )
    
    bot.send_message(ADMIN_ID, alert, reply_markup=m, parse_mode="Markdown")
    bot.send_message(uid, "✅ *AAPKI MAIL RECEIVE HO GAYI HAI!* 🎉\n\n🚀 Activation process mein hai, thoda intezar karein.")

def send_id_to_user(message, t_uid):
    try:
        txt = (
            f"🎉 AAPKA PAYMENT VERIFY HO GAYA HAI! ✅\n\n"
            f"🔐 ACCOUNT DETAILS:\n\n{message.text}\n\n"
            f"❤️ Thank You For Buying From V-Premium!"
        )
        bot.send_message(t_uid, txt)
        bot.send_message(message.chat.id, "✅ ID/Password User ko bhej diya gaya hai!")
    except Exception:
        bot.send_message(message.chat.id, "❌ Error: User tak message nahi gaya.")

if __name__ == '__main__':
    keep_alive()
    bot.remove_webhook()
    print("🚀 V-Premium Bot is running smoothly...")
    bot.infinity_polling(skip_pending=True)
