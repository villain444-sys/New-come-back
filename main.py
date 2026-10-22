import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, io, qrcode, requests
from flask import Flask
from threading import Thread
from pymongo import MongoClient

# 🟢 BOT CONFIGURATION
BOT_TOKEN = "8777634130:AAEfZpoDgpx5vrjhj232poiFXt2HVw1ict8"
CHANNEL_USERNAME = "villain_ott_hub"
UPI_ID = "rishabhx07@fam"
ADMIN_ID = 8692723368
ADMIN_USERNAME = "ishowvillain"
CHANNEL_LINK = "https://t.me/villain_ott_hub"
TRUST_API_KEY = "Fam_live_d28474caad09563b9b8a2383599d6e88a979" 

# 🟢 MONGODB CONFIGURATION
MONGO_URL = "mongodb+srv://admin:samontop@cluster0.dtv35tb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client['VPremiumDB']
users_col = db['users']
wallet_col = db['wallet']

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

# 🟢 DATABASE HELPER FUNCTIONS
def save_user(user_id):
    users_col.update_one({"_id": user_id}, {"$set": {"_id": user_id}}, upsert=True)

def get_balance(user_id):
    user = wallet_col.find_one({"_id": user_id})
    return user.get("balance", 0) if user else 0

def update_balance(user_id, amount):
    wallet_col.update_one({"_id": user_id}, {"$inc": {"balance": amount}}, upsert=True)
    user = wallet_col.find_one({"_id": user_id})
    if user["balance"] < 0:
        wallet_col.update_one({"_id": user_id}, {"$set": {"balance": 0}})
        return 0
    return user["balance"]

def check_sub(user_id):
    try:
        chat_handle = f"@{CHANNEL_USERNAME}"
        status = bot.get_chat_member(chat_handle, user_id).status
        return status in ['member', 'creator', 'administrator']
    except Exception:
        return False
        # 🟢 MENUS
def main_home_menu():
    m = InlineKeyboardMarkup(row_width=1)
    m.add(
        InlineKeyboardButton("🛍️ Explore Products & Plans 🛍️", callback_data="open_products"),
        InlineKeyboardButton("💳 My Wallet System 💰", callback_data="my_wallet")
    )
    m.row(
        InlineKeyboardButton("💬 Support 🛠️", url=f"https://t.me/{ADMIN_USERNAME}"),
        InlineKeyboardButton("⭐ Vouches 🔥", url=CHANNEL_LINK)
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

# 🟢 COMMANDS
@bot.message_handler(commands=['start'])
def send_welcome(message):
    uid = message.from_user.id
    save_user(uid)
    if check_sub(uid):
        txt = (
            "✨ <b>WELCOME TO V-PREMIUM STORE!</b> 👑\n\n"
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

@bot.message_handler(commands=['addbal'])
def admin_add_balance(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        target = int(args[1])
        amt = int(args[2])
        new_bal = update_balance(target, amt)
        bot.send_message(message.chat.id, f"✅ Added ₹{amt} to `{target}`.\n💰 New Balance: ₹{new_bal}", parse_mode="Markdown")
        bot.send_message(target, f"🎉 Admin ne aapke wallet mein ₹{amt} add kiye hain!\n💰 Current Balance: ₹{new_bal}")
    except Exception:
        bot.send_message(message.chat.id, "⚠️ Format: /addbal <user_id> <amount>")

@bot.message_handler(commands=['minusbal'])
def admin_minus_balance(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        target = int(args[1])
        amt = int(args[2])
        new_bal = update_balance(target, -amt)
        bot.send_message(message.chat.id, f"✅ Deducted ₹{amt} from `{target}`.\n💰 New Balance: ₹{new_bal}", parse_mode="Markdown")
        bot.send_message(target, f"⚠️ Admin ne aapke wallet se ₹{amt} deduct kiye hain.\n💰 Current Balance: ₹{new_bal}")
    except Exception:
        bot.send_message(message.chat.id, "⚠️ Format: /minusbal <user_id> <amount>")

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id != ADMIN_ID: return
    msg = bot.send_message(message.chat.id, "📢 Sabhi Users Ko Bhejne Ke Liye Message Ya Photo Type Karein:")
    bot.register_next_step_handler(msg, send_broadcast_to_all)

def send_broadcast_to_all(message):
    users = [u["_id"] for u in users_col.find()]
    if not users:
        return bot.send_message(message.chat.id, "❌ Koi User Nahi Mila!")
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
# 🟢 CALLBACK HANDLERS
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
            "🎬 <b>Netflix</b> | 📦 <b>Prime</b> | 🎵 <b>Spotify</b>\n"
            "▶️ <b>YouTube</b> | 🌐 <b>Hotstar</b>\n"
            "🍥 <b>Crunchyroll</b> | 🤖 <b>Gemini</b>"
        )
        bot.edit_message_text(txt, cid, mid, reply_markup=products_menu(), parse_mode="HTML")

    elif call.data == "back_main":
        txt = "✨ <b>WELCOME BACK TO V-PREMIUM STORE!</b> 👑\n\n🔥 <b>Sabse Saste Aur 100% Reliable Premium Accounts.</b>\n\n👇 <b>Niche Se Option Select Karein:</b>"
        bot.edit_message_text(txt, cid, mid, reply_markup=main_home_menu(), parse_mode="HTML")

    elif call.data == "my_wallet":
        bal = get_balance(uid)
        txt = (
            f"💳 <b>YOUR WALLET DASHBOARD</b>\n\n"
            f"👤 <b>User ID:</b> <code>{uid}</code>\n"
            f"💰 <b>Available Balance:</b> ₹{bal}\n\n"
            f"<i>Aap is balance ka use karke seedha plans khareed sakte hain bina baar-baar QR scan kiye!</i>"
        )
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("➕ Add Balance to Wallet", callback_data="add_wallet_prompt"),
            InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_main")
        )
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "add_wallet_prompt":
        msg = bot.send_message(cid, "💰 <b>Aap apne wallet mein kitna balance add karna chahte hain?</b>\n\n<i>Kripya niche sirf amount type karein (Jaise: 50, 100, 200)</i> 👇", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_add_balance)

    elif call.data == "menu_netflix":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("📱 Mobile - ₹99", callback_data="buy_netflix_mob"), InlineKeyboardButton("📺 TV - ₹99", callback_data="buy_netflix_tv"), InlineKeyboardButton("💻 Laptop / PC - ₹99", callback_data="buy_netflix_pc"), InlineKeyboardButton("🔙 Back to Products", callback_data="open_products"))
        bot.edit_message_text('🎬 <b>NETFLIX PREMIUM (1M - 4K)</b>\n\n👇 <b>Apna Device Select Karein:</b>', cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "menu_prime":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("📦 1 Month Plan - ₹70", callback_data="prime_dur_1"), InlineKeyboardButton("📦 6 Months Plan - ₹299", callback_data="prime_dur_6"), InlineKeyboardButton("🔙 Back to Products", callback_data="open_products"))
        bot.edit_message_text('📦 <b>AMAZON PRIME VIDEO</b>\n\n👇 <b>Apna Plan Duration Select Karein:</b>', cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "prime_dur_1":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_prime1_yes"), InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_prime1_no"), InlineKeyboardButton("🔙 Back to Prime Plans", callback_data="menu_prime"))
        bot.edit_message_text('📦 <b>AMAZON PRIME (1 MONTH) - ₹70</b>\n\n👇 <b>Apna Option Select Karein:</b>', cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "prime_dur_6":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_prime6_yes"), InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_prime6_no"), InlineKeyboardButton("🔙 Back to Prime Plans", callback_data="menu_prime"))
        bot.edit_message_text('📦 <b>AMAZON PRIME (6 MONTHS) - ₹299</b>\n\n👇 <b>Apna Option Select Karein:</b>', cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "menu_spotify":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_spotify_yes"), InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_spotify_no"), InlineKeyboardButton("🔙 Back to Products", callback_data="open_products"))
        bot.edit_message_text('🎵 <b>SPOTIFY PREMIUM (3M) - ₹60</b>\n\n👇 <b>Apna Option Select Karein:</b>', cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "menu_hotstar":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_hotstar_yes"), InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_hotstar_no"), InlineKeyboardButton("🔙 Back to Products", callback_data="open_products"))
        bot.edit_message_text('🌐 <b>JIOHOTSTAR PREMIUM (1M) - ₹50</b>\n\n👇 <b>Apna Option Select Karein:</b>', cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data == "menu_crunchyroll":
        m = InlineKeyboardMarkup(row_width=1)
        m.add(InlineKeyboardButton("📧 On Your Mail ✅", callback_data="buy_crunchy_yes"), InlineKeyboardButton("📧 On Your Mail ❌", callback_data="buy_crunchy_no"), InlineKeyboardButton("🔙 Back to Products", callback_data="open_products"))
        bot.edit_message_text('🍥 <b>CRUNCHYROLL (1M) - ₹50</b>\n\n👇 <b>Apna Option Select Karein:</b>', cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data.startswith("buy_"):
        p_name, p_amt = PLAN_DATA.get(call.data, ("VIP Plan", 30))
        bal = get_balance(uid)
        
        txt = f"🛒 <b>ORDER CONFIRMATION</b>\n\n📦 Plan: <b>{p_name}</b>\n💰 Total Amount: <b>₹{p_amt}</b>\n\nPayment ka tarika select karein:"
        
        m = InlineKeyboardMarkup(row_width=1)
        m.add(
            InlineKeyboardButton("✅ Pay Now 💸 (UPI QR)", callback_data=f"pay_{call.data}"),
            InlineKeyboardButton(f"💳 Pay from Wallet (Bal: ₹{bal})", callback_data=f"walletpay_{call.data}"),
            InlineKeyboardButton("❌ Cancel", callback_data="open_products")
        )
        bot.edit_message_text(txt, cid, mid, reply_markup=m, parse_mode="HTML")

    elif call.data.startswith("walletpay_buy_"):
        code = call.data.replace("walletpay_", "") 
        p_name, amt = PLAN_DATA.get(code, ("VIP Plan", 30))
        bal = get_balance(uid)
        
        if bal >= amt:
            update_balance(uid, -amt)
            bot.edit_message_text(f"🎉 <b>WALLET PAYMENT SUCCESSFUL!</b> ✅\n\n₹{amt} aapke wallet se deduct ho gaye hain.", cid, mid, parse_mode="HTML")
            process_successful_payment(cid, code, p_name, amt)
        else:
            bot.answer_callback_query(call.id, f"❌ Insufficient Balance!\nAapke paas ₹{bal} hain, par plan ₹{amt} ka hai.\nPehle wallet mein balance add karein.", show_alert=True)

    elif call.data.startswith("pay_"):
        code = call.data.replace("pay_", "")
        p_name, amt = PLAN_DATA.get(code, ("VIP Plan", 30))

        bot.delete_message(cid, mid)
        msg = bot.send_message(cid, "⏳ <b>Generating Direct UPI QR...</b>", parse_mode="HTML")

        payload = {"amount": str(amt), "note": f"Plan: {code}, User: {cid}"}
        try:
            api_res = requests.post('https://trustgateway.in/api/v1/orders/create', json=payload, headers={'Content-Type': 'application/json', 'X-API-Key': TRUST_API_KEY}).json()
            if api_res.get('success'):
                order_id = api_res['data']['order_id']
                exact_amount = api_res['data']['amount']
                upi_url = f"upi://pay?pa={UPI_ID}&pn=V-Premium&am={exact_amount}&cu=INR"
                
                qr = qrcode.make(upi_url)
                bio = io.BytesIO()
                bio.name = 'qr.png'
                qr.save(bio, 'PNG')
                bio.seek(0)

                cap = f"🛒 <b>YOUR SELECTED PLAN:</b>\n👉 {p_name}\n\n📲 Upar QR Code Scan Karein\n<i>(Direct GPay/PhonePe/Paytm khulega)</i>\n\n⚠️ <b>Note:</b> Amount <b>₹{exact_amount}</b> hi rehne dein, warna auto-verify nahi hoga!\n\n📸 Payment hone ke baad niche '✅ I Paid' dabayein! 🚀"
                m = InlineKeyboardMarkup(row_width=2)
                m.add(InlineKeyboardButton("✅ I Paid", callback_data=f"chk_{order_id}_{code}"), InlineKeyboardButton("❌ Cancel", callback_data="open_products"))

                bot.delete_message(cid, msg.message_id)
                bot.send_photo(cid, bio, caption=cap, reply_markup=m, parse_mode="HTML")
            else:
                bot.edit_message_text("⚠️ Payment gateway error. Admin ko contact karein.", cid, msg.message_id)
        except Exception:
            bot.edit_message_text("⚠️ Server error. Thodi der baad try karein.", cid, msg.message_id)

    elif call.data.startswith("chk_"):
        parts = call.data.split("_")
        order_id = parts[1]

        try:
            response = requests.get(f'https://trustgateway.in/api/v1/orders/status/{order_id}', headers={'X-API-Key': TRUST_API_KEY}).json()
            if response.get('paid') == True:
                if "wallet" in call.data:
                    amt = int(parts[-1])
                    new_bal = update_balance(cid, amt)
                    bot.edit_message_caption(f"🎉 <b>WALLET RECHARGE SUCCESSFUL!</b> ✅\n\n₹{amt} aapke wallet me add ho gaye hain.\n💰 <b>New Balance:</b> ₹{new_bal}", chat_id=cid, message_id=mid, parse_mode="HTML")
                else:
                    code = "_".join(parts[2:])
                    p_name, amt = PLAN_DATA.get(code, ("VIP Plan", 30))
                    bot.edit_message_caption("🎉 <b>PAYMENT VERIFIED AUTOMATICALLY!</b> ✅\n\nWait for the next step...", chat_id=cid, message_id=mid, parse_mode="HTML")
                    process_successful_payment(cid, code, p_name, amt)
            else:
                bot.answer_callback_query(call.id, "❌ Payment verify nahi hui. Agar pay kiya hai toh 1 min ruk kar wapas 'I Paid' dabayein.", show_alert=True)
        except Exception:
            bot.answer_callback_query(call.id, "⚠️ API Server error. Try again.", show_alert=True)

    elif call.data.startswith("reply_pass_"):
        t_uid = call.data.split("_")[2]
        msg = bot.send_message(cid, "🔑 Is user ke liye ID / Password type karke bhejo:")
        bot.register_next_step_handler(msg, send_id_to_user, t_uid)
        
    elif call.data.startswith("inv_sent_"):
        t_uid = call.data.split("_")[2]
        bot.send_message(t_uid, "🎉 <b>Your invitation has been sent!</b> 💌\n\nPlease check your mail inbox or spam folder to accept it. Enjoy your Premium! ❤️🙏", parse_mode="HTML")
        bot.edit_message_text(f"{call.message.text}\n\n✅ <b>Status: Invitation Sent</b>", cid, mid, parse_mode="HTML")

    elif call.data.startswith("mail_prob_"):
        t_uid = call.data.split("_")[2]
        bot.send_message(t_uid, f"⚠️ <b>Aapki Mail mein kuch problem hai, please admin se contact karein:</b> @{ADMIN_USERNAME}", parse_mode="HTML")
        bot.edit_message_text(f"{call.message.text}\n\n⚠️ <b>Status: Problem Reported</b>", cid, mid, parse_mode="HTML")

def process_add_balance(message):
    uid = message.from_user.id
    try:
        amt = int(message.text)
        if amt < 10:
            return bot.send_message(message.chat.id, "⚠️ Kripya kam se kam ₹10 add karein. Wapas wallet button par click karein.")
        
        msg = bot.send_message(message.chat.id, "⏳ <b>Generating Wallet QR...</b>", parse_mode="HTML")
        payload = {"amount": str(amt), "note": f"Wallet Recharge User: {uid}"}
        
        api_res = requests.post('https://trustgateway.in/api/v1/orders/create', json=payload, headers={'Content-Type': 'application/json', 'X-API-Key': TRUST_API_KEY}).json()
        if api_res.get('success'):
            order_id = api_res['data']['order_id']
            exact_amount = api_res['data']['amount']
            upi_url = f"upi://pay?pa={UPI_ID}&pn=V-Premium+Wallet&am={exact_amount}&cu=INR"
            
            qr = qrcode.make(upi_url)
            bio = io.BytesIO()
            bio.name = 'qr.png'
            qr.save(bio, 'PNG')
            bio.seek(0)

            cap = f"💳 <b>WALLET RECHARGE INITIATED</b>\n\n💰 Amount to Add: <b>₹{exact_amount}</b>\n\n📲 QR Code Scan karke Payment karein.\n⚠️ <b>Note:</b> Amount {exact_amount} hi rakhein auto-verify ke liye.\n\n📸 Pay karne ke baad '✅ I Paid' dabayein!"
            m = InlineKeyboardMarkup(row_width=1)
            m.add(
                InlineKeyboardButton("✅ I Paid", callback_data=f"chk_{order_id}_wallet_{amt}"),
                InlineKeyboardButton("❌ Cancel", callback_data="my_wallet")
            )
            bot.delete_message(message.chat.id, msg.message_id)
            bot.send_photo(message.chat.id, bio, caption=cap, reply_markup=m, parse_mode="HTML")
        else:
            bot.edit_message_text("⚠️ Payment gateway error.", message.chat.id, msg.message_id)
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Kripya sirf number type karein (Jaise: 50). Wapas wallet menu mein jaakar try karein.")

def process_successful_payment(uid, code, p_name, amt):
    is_mail_plan = ("on mail ✅" in p_name.lower()) or ("youtube" in p_name.lower())
    if is_mail_plan:
        txt = "🎉 <b>PAYMENT VERIFIED!</b> ✅\n\n📧 <b>PLEASE SEND YOUR EMAIL / GMAIL ID FOR ACTIVATION</b>\n<i>(Apni Mail ID niche type karke send karein)</i> 👇"
        msg = bot.send_message(uid, txt, parse_mode="HTML")
        bot.register_next_step_handler(msg, receive_user_gmail)
        bot.send_message(ADMIN_ID, f"✅ <b>Auto-Payment Success</b>\nUser: <code>{uid}</code>\nPlan: {p_name}\nStatus: Waiting for email...", parse_mode="HTML")
    else:
        bot.send_message(uid, "🎉 <b>PAYMENT VERIFIED!</b> ✅\n\n⏳ Admin aapko jaldi hi ID & Password send karenge. Kripya wait karein!", parse_mode="HTML")
        cap = f"🔔 <b>NEW AUTO-PAYMENT VERIFIED!</b>\n\n📦 Plan: {p_name}\n👤 User ID: <code>{uid}</code>\n💰 Amount: ₹{amt}\n\nAction: Niche click karke ID/Pass bhejein:"
        m = InlineKeyboardMarkup().add(InlineKeyboardButton("🔑 Send ID/Pass", callback_data=f"reply_pass_{uid}"))
        bot.send_message(ADMIN_ID, cap, reply_markup=m, parse_mode="HTML")

def receive_user_gmail(message):
    uid = message.from_user.id
    uname = message.from_user.username or "None"
    alert = f"📩 <b>RECEIVED MAIL ADDRESS!</b> ⚡\n\n👤 <b>User:</b> @{uname} (<code>{uid}</code>)\n📧 <b>Mail:</b> <code>{message.text}</code>\n\nAction select karein:"
    m = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("✅ Invitation Sent", callback_data=f"inv_sent_{uid}"), InlineKeyboardButton("❌ Some Problem", callback_data=f"mail_prob_{uid}"))
    bot.send_message(ADMIN_ID, alert, reply_markup=m, parse_mode="HTML")
    bot.send_message(uid, "✅ <b>AAPKI MAIL RECEIVE HO GAYI HAI!</b> 🎉\n\n🚀 Activation process mein hai, thoda intezar karein.", parse_mode="HTML")

def send_id_to_user(message, t_uid):
    try:
        bot.send_message(t_uid, f"🎉 AAPKA PAYMENT VERIFY HO GAYA HAI! ✅\n\n🔐 ACCOUNT DETAILS:\n\n{message.text}\n\n❤️ Thank You For Buying From V-Premium!")
        bot.send_message(message.chat.id, "✅ ID/Password User ko bhej diya gaya hai!")
    except Exception:
        bot.send_message(message.chat.id, "❌ Error: User tak message nahi gaya.")

if __name__ == '__main__':
    keep_alive()
    bot.remove_webhook()
    print("🚀 V-Premium Bot is running smoothly with MongoDB & Wallet System...")
    bot.infinity_polling(skip_pending=True)
                     
