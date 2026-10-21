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
            "✨ <b>WELCOME TO V-PREMIUM STORE!</b> <tg-emoji emoji-id=\"5368324170671202286\">👑</tg-emoji>\n\n"
            "🔥 <b>Yahan Milte Hain Sabse Saste, 100% Genuine Aur Fully Trusted Premium Accounts!</b>\n\n"
            "⚡ <b>Instant Delivery | Full Warranty | VIP Support</b>\n\n"
            "👇 <b>Niche Diye Gaye Buttons Se Apna Option Select Karein:</b>"
        )
        bot.send_message(message.chat.id, txt, reply_markup=main_home_menu(), parse_mode="HTML")
    else:
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📢 Join Official Channel Now 🔥", url=CHANNEL_LINK),
            InlineKeyboardButton("✅ Check / Verify Subscription ✔️", callback_data="verify_sub")
        )
        warn = (
            "⚠️ <b>HOLD ON! ACCESS LOCKED!</b> 🔒\n\n"
            "📢 <b>Bot Ko Use Karne Ke Liye Pehle Hamara Official Channel Join Karna Zaroori Hai!</b>\n\n"
            "👇 <b>Niche Button Par Click Karke Channel Join Karein Aur Phir 'Check / Verify' Dabayein:</b>"
        )
        bot.send_message(message.chat.id, warn, reply_markup=m, parse_mode="HTML")

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
            txt = "🎉 <b>VERIFICATION SUCCESSFUL!</b> ✅\n\n✨ <b>Ab Aap Hamare Saare VIP Plans Explore Kar Sakte Hain.</b>\n\n👇 <b>Niche Se Option Select Karein:</b>"
            bot.send_message(cid, txt, reply_markup=main_home_menu(), parse_mode="HTML")
        else:
            bot.answer_callback_query(call.id, "❌ Bhai Pehle Channel Join Karein!", show_alert=True)
            
    elif call.data == "open_products":
        txt = (
            "🛍️ <b>V-PREMIUM STORE DASHBOARD</b>\n\n"
            "💎 <b>Sabhi Plans 100% Working Aur Guaranteed Hain!</b>\n\n"
            "👇 <b>Apna Pasandida OTT / AI Plan Select Karein:</b>\n\n"
            "<tg-emoji emoji-id=\"5318911503938634641\">🎬</tg-emoji> <b>Netflix</b> | "
            "<tg-emoji emoji-id=\"5346056560537779652\">📦</tg-emoji> <b>Prime</b> | "
            "<tg-emoji emoji-id=\"5346074681004801565\">🎵</tg-emoji> <b>Spotify</b>\n"
            "<tg-emoji emoji-id=\"5334681713316479679\">▶️</tg-emoji> <b>YouTube</b> | "
            "<tg-emoji emoji-id=\"5332394707655869572\">🌐</tg-emoji> <b>Hotstar</b>\n"
            "<tg-emoji emoji-id=\"6231196182907983273\">🍥</tg-emoji> <b>Crunchyroll</b> | "
            "<tg-emoji emoji-id=\"5951817721468424817\">🤖</tg-emoji> <b>Gemini</b>"
        )
        bot.edit_message_text(txt, cid, mid, reply_markup=products_menu(), parse_mode="HTML")

    elif call.data == "back_main":
        txt = "✨ <b>WELCOME BACK TO V-PREMIUM STORE!</b> <tg-emoji emoji-id=\"5368324170671202286\">👑</tg-emoji>\n\n🔥 <b>Sabse Saste Aur 100% Reliable Premium Accounts.</b>\n\n👇 <b>Niche Se Option Select Karein:</b>"
        bot.edit_message_text(txt, cid, mid, reply_markup=main_home_menu(), parse_mode="HTML")

    elif call.data == "menu_netflix":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📱 Mobile - ₹99", callback_data="buy_netflix_mob"),
            InlineKeyboardButton("📺 TV - ₹99", callback_data="buy_netflix_tv"),
            InlineKeyboardButton("💻 Laptop / PC - ₹99", callback_data="buy_netflix_pc"),
            InlineKeyboardButton("🔙 Back to Products", callback_data="open_products")
        )
        txt = '<tg-emoji emoji-id="5318911503938634641">🎬</tg-emoji> <b>NETFLIX PREMIUM (1M - 4K)</b>\n\n👇 <b>Apna Device Select Karein:</b>'
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "menu_prime":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📦 1 Month Plan - ₹70", callback_data="prime_dur_1"),
            InlineKeyboardButton("📦 6 Months Plan - ₹299", callback_data="prime_dur_6"),
            InlineKeyboardButton("🔙 Back to Products", callback_data="open_products")
        )
        txt = '<tg-emoji emoji-id="5346056560537779652">📦</tg-emoji> <b>AMAZON PRIME VIDEO</b>\n\n👇 <b>Apna Plan Duration Select Karein:</b>'
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "prime_dur_1":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_prime1_yes"),
            InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_prime1_no"),
            InlineKeyboardButton("🔙 Back to Prime Plans", callback_data="menu_prime")
        )
        txt = '<tg-emoji emoji-id="5346056560537779652">📦</tg-emoji> <b>AMAZON PRIME (1 MONTH) - ₹70</b>\n\n👇 <b>Apna Option Select Karein:</b>'
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "prime_dur_6":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_prime6_yes"),
            InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_prime6_no"),
            InlineKeyboardButton("🔙 Back to Prime Plans", callback_data="menu_prime")
        )
        txt = '<tg-emoji emoji-id="5346056560537779652">📦</tg-emoji> <b>AMAZON PRIME (6 MONTHS) - ₹299</b>\n\n👇 <b>Apna Option Select Karein:</b>'
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "menu_spotify":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_spotify_yes"),
            InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_spotify_no"),
            InlineKeyboardButton("🔙 Back to Products", callback_data="open_products")
        )
        txt = '<tg-emoji emoji-id="5346074681004801565">🎵</tg-emoji> <b>SPOTIFY PREMIUM (3M) - ₹60</b>\n\n👇 <b>Apna Option Select Karein:</b>'
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "menu_hotstar":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_hotstar_yes"),
            InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_hotstar_no"),
            InlineKeyboardButton("🔙 Back to Products", callback_data="open_products")
        )
        txt = '<tg-emoji emoji-id="5332394707655869572">🌐</tg-emoji> <b>JIOHOTSTAR PREMIUM (1M) - ₹50</b>\n\n👇 <b>Apna Option Select Karein:</b>'
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "menu_crunchyroll":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_crunchy_yes"),
            InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_crunchy_no"),
            InlineKeyboardButton("🔙 Back to Products", callback_data="open_products")
        )
        txt = '<tg-emoji emoji-id="6231196182907983273">🍥</tg-emoji> <b>CRUNCHYROLL (1M) - ₹50</b>\n\n👇 <b>Apna Option Select Karein:</b>'
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data.startswith("buy_"):
        p_name, p_amt = PLAN_DATA.get(call.data, ("VIP Plan", 30))
        sel = f"{p_name} - ₹{p_amt}"
        
        icon = "🛒"
        if "netflix" in call.data: icon = '<tg-emoji emoji-id="5318911503938634641">🎬</tg-emoji>'
        elif "prime" in call.data: icon = '<tg-emoji emoji-id="5346056560537779652">📦</tg-emoji>'
        elif "spotify" in call.data: icon = '<tg-emoji emoji-id="5346074681004801565">🎵</tg-emoji>'
        elif "hotstar" in call.data: icon = '<tg-emoji emoji-id="5332394707655869572">🌐</tg-emoji>'
        elif "crunchyroll" in call.data: icon = '<tg-emoji emoji-id="6231196182907983273">🍥</tg-emoji>'
        elif "youtube" in call.data: icon = '<tg-emoji emoji-id="5334681713316479679">▶️</tg-emoji>'
        elif "gemini" in call.data: icon = '<tg-emoji emoji-id="5951817721468424817">🤖</tg-emoji>'

        txt = f"{icon} <b>ORDER CONFIRMATION</b>\n\n📦 Plan: <b>{sel}</b>\n💰 Total Amount: <b>₹{p_amt}</b>\n\nPayment Ke Liye '✅ Pay Now' Par Click Karein:"
        
        m = InlineKeyboardMarkup(row_width=2)
        m.add(
            InlineKeyboardButton("✅ Pay Now 💸", callback_data=f"pay_{call.data}"),
            InlineKeyboardButton("❌ Cancel", callback_data="open_products")
        )
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data.startswith("pay_"):
        code = call.data.replace("pay_", "")
        p_name, amt = PLAN_DATA.get(code, ("VIP Plan", 30))
        sel = f"{p_name} - ₹{amt}"

        bot.delete_message(cid, mid)
        msg = bot.send_message(cid, "⏳ <b>Generating Direct UPI QR...</b>", parse_mode="HTML")

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
                    f"🛒 <b>YOUR SELECTED PLAN:</b>\n👉 {sel}\n\n"
                    f"📲 Upar QR Code Scan Karein\n"
                    f"<i>(Direct GPay/PhonePe/Paytm khulega)</i>\n\n"
                    f"⚠️ <b>Note:</b> Amount <b>₹{exact_amount}</b> hi rehne dein, warna auto-verify nahi hoga!\n\n"
                    f"📸 Payment hone ke baad niche '✅ I Paid' dabayein! 🚀"
                )

                m = InlineKeyboardMarkup(row_width=2)
                m.add(
                    InlineKeyboardButton("✅ I Paid", callback_data=f"chk_{order_id}_{code}"),
                    InlineKeyboardButton("❌ Cancel", callback_data="open_products")
                )

                bot.delete_message(cid, msg.message_id)
                bot.send_photo(cid, bio, caption=cap, reply_markup=m, parse_mode="HTML")
            else:
                bot.edit_message_text("⚠️ Payment gateway error. Admin ko contact karein.", cid, msg.message_id)
        except Exception as e:
            bot.edit_message_text("⚠️ Server error. Thodi der baad try karein.", cid, msg.message_id)

    elif call.data.startswith("chk_"):
        parts = call.data.split("_")
        order_id = parts[1]
        code = "_".join(parts[2:])
        p_name, amt = PLAN_DATA.get(code, ("VIP Plan", 30))

        headers = {'X-API-Key': TRUST_API_KEY}
        try:
            status_url = f'https://trustgateway.in/api/v1/orders/status/{order_id}'
            response = requests.get(status_url, headers=headers).json()

            if response.get('paid') == True:
                bot.edit_message_caption("🎉 <b>PAYMENT VERIFIED AUTOMATICALLY!</b> ✅\n\nWait for the next step...", chat_id=cid, message_id=mid, parse_mode="HTML")
                
                is_mail_plan = ("on mail ✅" in p_name.lower()) or ("youtube" in p_name.lower())
                
                if is_mail_plan:
                    txt = (
                        "🎉 <b>PAYMENT VERIFIED!</b> ✅\n\n"
                        "📧 <b>PLEASE SEND YOUR EMAIL / GMAIL ID FOR ACTIVATION</b>\n"
                        "<i>(Apni Mail ID niche type karke send karein)</i> 👇"
                    )
                    msg = bot.send_message(cid, txt, parse_mode="HTML")
                    bot.register_next_step_handler(msg, receive_user_gmail)
                    
                    bot.send_message(ADMIN_ID, f"✅ <b>Auto-Payment Success</b>\nUser: <code>{cid}</code>\nPlan: {p_name}\nStatus: Waiting for user's email...", parse_mode="HTML")
                else:
                    bot.send_message(cid, "🎉 <b>PAYMENT VERIFIED!</b> ✅\n\n⏳ Admin aapko jaldi hi ID & Password send karenge. Kripya wait karein!", parse_mode="HTML")
                    
                    cap = (
                        f"🔔 <b>NEW AUTO-PAYMENT VERIFIED!</b>\n\n"
                        f"📦 Plan: {p_name}\n"
                        f"👤 User ID: <code>{cid}</code>\n"
                        f"💰 Amount: ₹{amt}\n\n"
                        f"Action: Niche button click karke ID/Pass bhejein:"
                    )
                    m = InlineKeyboardMarkup()
                    m.add(InlineKeyboardButton("🔑 Send ID/Pass", callback_data=f"reply_pass_{cid}"))
                    bot.send_message(ADMIN_ID, cap, reply_markup=m, parse_mode="HTML")

            else:
                bot.answer_callback_query(call.id, "❌ Payment verify nahi hui. Agar abhi pay kiya hai toh 1 minute ruk kar dobara 'I Paid' dabayein.", show_alert=True)
                
        except Exception as e:
            bot.answer_callback_query(call.id, "⚠️ API Server error. Try again.", show_alert=True)

    elif call.data.startswith("reply_pass_"):
        t_uid = call.data.split("_")[2]
        msg = bot.send_message(cid, "🔑 Is user ke liye ID / Password type karke bhejo:")
        bot.register_next_step_handler(msg, send_id_to_user, t_uid)
        
    elif call.data.startswith("inv_sent_"):
        t_uid = call.data.split("_")[2]
        try:
            msg_user = "🎉 <b>Your invitation has been sent!</b> 💌\n\nPlease check your mail inbox or spam folder to accept it. Enjoy your Premium! ❤️🙏"
            bot.send_message(t_uid, msg_user, parse_mode="HTML")
            bot.edit_message_text(f"{call.message.text}\n\n✅ <b>Status: Invitation Sent (User Notified)</b>", cid, mid, parse_mode="HTML")
        except Exception:
            bot.send_message(cid, "❌ User tak message nahi gaya.")

    elif call.data.startswith("mail_prob_"):
        t_uid = call.data.split("_")[2]
        try:
            msg_user = f"⚠️ <b>Aapki Mail mein kuch problem hai, please admin se contact karein:</b> @{ADMIN_USERNAME}"
            bot.send_message(t_uid, msg_user, parse_mode="HTML")
            bot.edit_message_text(f"{call.message.text}\n\n⚠️ <b>Status: Problem Reported to User</b>", cid, mid, parse_mode="HTML")
        except Exception:
            bot.send_message(cid, "❌ User tak message nahi gaya.")

def receive_user_gmail(message):
    uid = message.from_user.id
    uname = message.from_user.username or "None"
    user_gmail = message.text

    alert = (
        f"📩 <b>RECEIVED MAIL ADDRESS!</b> ⚡\n\n"
        f"👤 <b>User:</b> @{uname} (<code>{uid}</code>)\n"
        f"📧 <b>Mail:</b> <code>{user_gmail}</code>\n\n"
        f"Action select karein:"
    )
    
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("✅ Invitation Sent", callback_data=f"inv_sent_{uid}"),
        InlineKeyboardButton("❌ Some Problem", callback_data=f"mail_prob_{uid}")
    )
    
    bot.send_message(ADMIN_ID, alert, reply_markup=m, parse_mode="HTML")
    bot.send_message(uid, "✅ <b>AAPKI MAIL RECEIVE HO GAYI HAI!</b> 🎉\n\n🚀 Activation process mein hai, thoda intezar karein.", parse_mode="HTML")

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
            
