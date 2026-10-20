import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, io, qrcode, requests
from flask import Flask
from threading import Thread

# BOT CONFIGURATION
BOT_TOKEN = "8777634130:AAEfZpoDgpx5vrjhj232poiFXt2HVw1ict8"
CHANNEL_USERNAME = "villain_ott_hub"
UPI_ID = "rishabhx07@fam"
ADMIN_ID = 8692723368
ADMIN_USERNAME = "ishowvillain"
CHANNEL_LINK = "https://t.me/villain_ott_hub"
USERS_FILE = "users.txt"
TRUST_API_KEY = "Fam_live_d28474caad09563b9b8a2383599d6e88a979" 

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

    # 🟢 AUTOMATIC PAYMENT GATEWAY LOGIC (DIRECT UPI QR)
    elif call.data.startswith("pay_"):
        code = call.data.replace("pay_", "")
        p_name, amt = PLAN_DATA.get(code, ("VIP Plan", 30))
        sel = f"{p_name} - ₹{amt}"

        bot.delete_message(cid, mid)
        msg = bot.send_message(cid, "⏳ *Generating Direct UPI QR...*", parse_mode="Markdown")

        headers = {
            'Content-Type': 'application/json',
            'X-API-Key': TRUST_API_KEY
        }
        payload = {
            "amount": str(amt),
            "note": f"Plan: {code}, User: {cid}"
        }

        try:
            api_res = requests.post('https://trustgateway.in/api/v1/orders/create', json=payload, headers=headers).json()
            
            if api_res.get('success'):
                order_id = api_res['data']['order_id']
                exact_amount = api_res['data']['amount']
                
                upi_url = f"upi://pay?pa={UPI_ID}&pn=V-Premium&am={exact_amount}&cu=INR"
                
                qr = qrcode.make(upi_url)
                bio = io.BytesIO()
                bio.name = 'qr.png'
                qr.save(bio, 'PNG')
                bio.seek(0)

                cap = (
                    f"🛒 *YOUR SELECTED PLAN:*\n👉 {sel}\n\n"
                    f"📲 Upar QR Code Scan Karein\n"
                    f"*(Direct GPay/PhonePe/Paytm khulega)*\n\n"
                    f"⚠️ *Note:* Amount *₹{exact_amount}* hi rehne dein, warna auto-verify nahi hoga!\n\n"
                    f"📸 Payment hone ke baad niche '✅ I Paid' dabayein! 🚀"
                )

                m = InlineKeyboardMarkup(row_width=2)
                m.add(
                    InlineKeyboardButton("✅ I Paid", callback_data=f"chk_{order_id}_{code}"),
                    InlineKeyboardButton("❌ Cancel", callback_data="open_products")
                )

                bot.delete_message(cid, msg.message_id)
                bot.send_photo(cid, bio, caption=cap, reply_markup=m, parse_mode="Markdown")
            else:
                bot.edit_message_text("⚠️ Payment gateway error. Admin ko contact karein.", cid, msg.message_id)
        except Exception as e:
            bot.edit_message_text("⚠️ Server error. Thodi der baad try karein.", cid, msg.message_id)

    # 🟢 AUTOMATIC PAYMENT VERIFICATION & REDIRECTION
    elif call.data.startswith("chk_"):
        parts = call.data.split("_")
        order_id = parts[1]
        code = "_".join(parts[2:]) # Restore plan code
        p_name, amt = PLAN_DATA.get(code, ("VIP Plan", 30))

        headers = {'X-API-Key': TRUST_API_KEY}
        try:
            status_url = f'https://trustgateway.in/api/v1/orders/status/{order_id}'
            response = requests.get(status_url, headers=headers).json()

            if response.get('paid') == True:
                # Payment 100% verified automatically
                bot.edit_message_caption("🎉 *PAYMENT VERIFIED AUTOMATICALLY!* ✅\n\nWait for the next step...", chat_id=cid, message_id=mid, parse_mode="Markdown")
                
                # Check agar plan "Mail" wala hai ya "ID/Pass" wala
                is_mail_plan = ("on mail ✅" in p_name.lower()) or ("youtube" in p_name.lower())
                
                if is_mail_plan:
                    # User se Mail maango
                    txt = (
                        "🎉 *PAYMENT VERIFIED!* ✅\n\n"
                        "📧 *PLEASE SEND YOUR EMAIL / GMAIL ID FOR ACTIVATION*\n"
                        "*(Apni Mail ID niche type karke send karein)* 👇"
                    )
                    msg = bot.send_message(cid, txt, parse_mode="Markdown")
                    bot.register_next_step_handler(msg, receive_user_gmail)
                    
                    # Admin ko info do
                    bot.send_message(ADMIN_ID, f"✅ *Auto-Payment Success*\nUser: `{cid}`\nPlan: {p_name}\nStatus: Waiting for user's email...", parse_mode="Markdown")
                else:
                    # Admin ko "Send ID/Pass" ka option do
                    bot.send_message(cid, "🎉 *PAYMENT VERIFIED!* ✅\n\n⏳ Admin aapko jaldi hi ID & Password send karenge. Kripya wait karein!", parse_mode="Markdown")
                    
                    cap = (
                        f"🔔 *NEW AUTO-PAYMENT VERIFIED!*\n\n"
                        f"📦 Plan: {p_name}\n"
                        f"👤 User ID: `{cid}`\n"
                        f"💰 Amount: ₹{amt}\n\n"
                        f"Action: Niche button click karke ID/Pass bhejein:"
                    )
                    m = InlineKeyboardMarkup()
                    m.add(InlineKeyboardButton("🔑 Send ID/Pass", callback_data=f"reply_pass_{cid}"))
                    bot.send_message(ADMIN_ID, cap, reply_markup=m, parse_mode="Markdown")

            else:
                bot.answer_callback_query(call.id, "❌ Payment verify nahi hui. Agar abhi pay kiya hai toh 1 minute ruk kar dobara 'I Paid' dabayein.", show_alert=True)
                
        except Exception as e:
            bot.answer_callback_query(call.id, "⚠️ API Server error. Try again.", show_alert=True)

    # 🟢 ADMIN POST-PAYMENT ACTIONS
    elif call.data.startswith("reply_pass_"):
        t_uid = call.data.split("_")[2]
        msg = bot.send_message(cid, "🔑 Is user ke liye ID / Password type karke bhejo:")
        bot.register_next_step_handler(msg, send_id_to_user, t_uid)
        
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
        
