import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, time, threading
from flask import Flask
from pymongo import MongoClient
from famgateway import FamGateway  # 👈 Naya VIP API Gateway

# 🟢 BOT & CONFIGURATION
BOT_TOKEN = "8777634130:AAEfZpoDgpx5vrjhj232poiFXt2HVw1ict8"
CHANNEL_USERNAME = "villain_ott_hub"
ADMIN_ID = 8692723368
ADMIN_USERNAME = "ishowvillain"
CHANNEL_LINK = "https://t.me/villain_ott_hub"

# 🟢 FAMGATEWAY API SETUP
API_KEY = "fam_f2e1023f31c14bc327cba4c0b086892d6ade3023"
fg = FamGateway(api_key=API_KEY)

# 🟢 MONGODB CONFIGURATION
MONGO_URL = "mongodb+srv://admin:samontop@cluster0.dtv35tb.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client['VPremiumDB']
users_col = db['users']
wallet_col = db['wallet']
# used_utrs_col ki ab zaroorat nahi kyunki API dynamic QR handle karegi

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "🚀 V-Premium Bot is Alive & Running Automatically!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    threading.Thread(target=run_flask).start()

PLAN_DATA = {
    "buy_netflix_mob": ("Netflix 1M (📱 Mobile)", 120),
    "buy_netflix_tv": ("Netflix 1M (📺 TV)", 120),
    "buy_netflix_pc": ("Netflix 1M (💻 Laptop/PC)", 120),
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
    "buy_gemini": ("Gemini Advanced (18 Months)", 80),
    "buy_chatgpt": ("ChatGPT GO (1 Month)", 150),
    "buy_tgprem_6m": ("Telegram Premium (6 Months)", 1200),
    "buy_tgprem_1y": ("Telegram Premium (1 Year)", 1700)
}

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
        InlineKeyboardButton("🎬 Netflix 4K - ₹120", callback_data="menu_netflix"),
        InlineKeyboardButton("📦 Amazon Prime", callback_data="menu_prime"),
        InlineKeyboardButton("🎵 Spotify (3M) - ₹60", callback_data="menu_spotify"),
        InlineKeyboardButton("▶️ YouTube Prem - ₹30", callback_data="buy_youtube"),
        InlineKeyboardButton("🌐 JioHotstar - ₹50", callback_data="menu_hotstar"),
        InlineKeyboardButton("🍥 Crunchyroll - ₹50", callback_data="menu_crunchyroll")
    )
    m.add(InlineKeyboardButton("🤖 Gemini (18M) - ₹80", callback_data="buy_gemini"))
    m.add(InlineKeyboardButton("🧠 ChatGPT GO - ₹150", callback_data="buy_chatgpt"))
    m.add(InlineKeyboardButton("💎 Telegram Premium (Gift)", callback_data="menu_tgprem"))
    m.add(InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_main"))
    return m

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
        bot.send_message(message.chat.id, "⚠️ <b>Channel Join Karein Pehle!</b>", reply_markup=m, parse_mode="HTML")

@bot.message_handler(commands=['addbal'])
def admin_add_balance(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        args = message.text.split()
        target, amt = int(args[1]), int(args[2])
        new_bal = update_balance(target, amt)
        bot.send_message(message.chat.id, f"✅ Added ₹{amt} to `{target}`. New Bal: ₹{new_bal}")
        bot.send_message(target, f"🎉 Admin ne wallet mein ₹{amt} add kiye! Current Bal: ₹{new_bal}")
    except:
        bot.send_message(message.chat.id, "⚠️ Format: /addbal <user_id> <amount>")

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id != ADMIN_ID: return
    msg = bot.send_message(message.chat.id, "📢 Message bhejien broadcast ke liye:")
    bot.register_next_step_handler(msg, lambda m: bot.send_message(message.chat.id, "✅ Broadcast started..."))
        # 🟢 BACKGROUND POLLING THREAD (Auto Verification)
def poll_order_status(order_id, chat_id, message_id, code, amt):
    start_time = time.time()
    while time.time() - start_time < 600:  # 10 Minutes loop
        time.sleep(4)  # Check every 4 seconds
        try:
            status = fg.get_status(order_id)
            if status.is_paid:
                try: bot.delete_message(chat_id, message_id) # Delete QR
                except: pass
                
                if code == "wallet":
                    new_bal = update_balance(chat_id, amt)
                    bot.send_message(chat_id, f"🎉 <b>WALLET RECHARGE SUCCESS!</b> ✅\n💰 New Balance: ₹{new_bal}", parse_mode="HTML")
                else:
                    p_name, _ = PLAN_DATA.get(code, ("VIP Plan", amt))
                    process_successful_payment(chat_id, code, p_name, amt)
                return
                
            elif status.is_expired:
                try: bot.edit_message_caption("⌛ <b>QR Code Expired!</b>\n\n10 minute pure ho gaye hain. Kripya back jaakar naya QR generate karein.", chat_id=chat_id, message_id=message_id, parse_mode="HTML")
                except: pass
                return
        except:
            pass

# 🟢 ALL CALLBACK LOGIC
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    cid, mid, uid = call.message.chat.id, call.message.message_id, call.from_user.id
    save_user(uid)
    
    # Basic Navigations
    if call.data == "open_products":
        bot.edit_message_text("🛍️ <b>V-PREMIUM STORE DASHBOARD</b>\n👇 Apna Plan Select Karein:", cid, mid, reply_markup=products_menu(), parse_mode="HTML")
    elif call.data == "back_main":
        bot.edit_message_text("✨ <b>WELCOME BACK TO V-PREMIUM STORE!</b>", cid, mid, reply_markup=main_home_menu(), parse_mode="HTML")
    elif call.data == "my_wallet":
        bal = get_balance(uid)
        m = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("➕ Add Balance to Wallet", callback_data="add_wallet_prompt"), InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_main"))
        bot.edit_message_text(f"💳 <b>YOUR WALLET</b>\n\n💰 Balance: ₹{bal}", cid, mid, reply_markup=m, parse_mode="HTML")
    
    # Sub-menus
    elif call.data == "menu_netflix":
        m = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("📱 Mobile - ₹120", callback_data="buy_netflix_mob"), InlineKeyboardButton("🔙 Back", callback_data="open_products"))
        bot.edit_message_text("🎬 <b>NETFLIX PREMIUM</b>", cid, mid, reply_markup=m, parse_mode="HTML")
    elif call.data == "menu_prime":
        m = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("📦 1 Month - ₹70", callback_data="buy_prime1_yes"), InlineKeyboardButton("🔙 Back", callback_data="open_products"))
        bot.edit_message_text("📦 <b>AMAZON PRIME</b>", cid, mid, reply_markup=m, parse_mode="HTML")
    
    # Order Confirmation
    elif call.data.startswith("buy_"):
        p_name, p_amt = PLAN_DATA.get(call.data, ("VIP Plan", 30))
        bal = get_balance(uid)
        txt = f"🛒 <b>ORDER CONFIRMATION</b>\n\n📦 Plan: <b>{p_name}</b>\n💰 Total Amount: <b>₹{p_amt}</b>\n\nPayment mode select karein:"
        m = InlineKeyboardMarkup(row_width=1).add(
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
            bot.edit_message_text(f"🎉 <b>WALLET PAYMENT SUCCESS!</b> ✅\n₹{amt} deducted.", cid, mid, parse_mode="HTML")
            process_successful_payment(cid, code, p_name, amt)
        else:
            bot.answer_callback_query(call.id, f"❌ Insufficient Balance! Aapke paas ₹{bal} hain.", show_alert=True)

    # 🚀 DYNAMIC QR GENERATOR FOR PLANS
    elif call.data.startswith("pay_"):
        code = call.data.replace("pay_", "")
        p_name, amt = PLAN_DATA.get(code, ("VIP Plan", 30))
        
        bot.edit_message_text("⏳ <b>Generating VIP QR Code...</b>", cid, mid, parse_mode="HTML")
        
        try:
            # FamGateway se 10 min wala QR mangwana
            order = fg.create_order(amount=float(amt), customer_name=str(uid))
            
            cap = (
                f"🛒 <b>YOUR PLAN:</b> {p_name}\n\n"
                f"📲 <b>Niche diye QR Code ko scan karke ₹{amt} pay karein.</b>\n"
                f"⏳ <i>Note: Ye QR code aur session 10 minute mein expire ho jayega!</i>\n\n"
                f"⚡ Payment hote hi system aapko automatically account deliver kar dega."
            )
            
            m = InlineKeyboardMarkup(row_width=2)
            m.add(
                InlineKeyboardButton("✅ I Paid", callback_data=f"chk_qr|{order.order_id}"),
                InlineKeyboardButton("❌ Cancel", callback_data="cancel_qr")
            )
            
            bot.delete_message(cid, mid)
            sent_msg = bot.send_photo(cid, photo=order.qr_url, caption=cap, reply_markup=m, parse_mode="HTML")
            
            # Start Auto-Checker in Background
            threading.Thread(target=poll_order_status, args=(order.order_id, cid, sent_msg.message_id, code, amt), daemon=True).start()
            
        except Exception as e:
            bot.send_message(cid, "⚠️ API Error. Admin se contact karein.")

    # 🚀 DYNAMIC QR FOR WALLET
    elif call.data == "add_wallet_prompt":
        msg = bot.send_message(cid, "💰 <b>Aap kitna balance add karna chahte hain?</b>\n(Sirf number type karein, eg: 50)", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_add_balance)

    # ❌ CANCEL BUTTON WORKING
    elif call.data == "cancel_qr":
        try: bot.delete_message(cid, mid)
        except: pass
        bot.send_message(cid, "❌ <b>Order Cancelled.</b>", parse_mode="HTML", reply_markup=products_menu())

    # ✅ I PAID BUTTON POPUP
    elif call.data.startswith("chk_qr|"):
        order_id = call.data.split("|")[1]
        try:
            if fg.get_status(order_id).is_paid:
                bot.answer_callback_query(call.id, "✅ Payment Verified! System aage ka process kar raha hai...", show_alert=True)
            else:
                bot.answer_callback_query(call.id, "⏳ Abhi bank se confirmation nahi aayi hai. QR scan karke pay karein aur auto-verify ka wait karein.", show_alert=True)
        except:
            bot.answer_callback_query(call.id, "⚠️ Check karne mein error aayi, thoda wait karein.", show_alert=True)

    # ID Delivery Logs
    elif call.data.startswith("reply_pass_"):
        t_uid = call.data.split("_")[2]
        msg = bot.send_message(cid, "🔑 Is user ke liye ID / Password type karke bhejo:")
        bot.register_next_step_handler(msg, lambda m: bot.send_message(t_uid, f"🔐 ACCOUNT DETAILS:\n\n{m.text}"))

def process_add_balance(message):
    uid, cid = message.from_user.id, message.chat.id
    try:
        amt = float(message.text)
        if amt < 10: return bot.send_message(cid, "⚠️ Kam se kam ₹10 add karein.")
        
        msg = bot.send_message(cid, "⏳ <b>Generating Wallet QR...</b>", parse_mode="HTML")
        order = fg.create_order(amount=amt, customer_name=f"wallet_{uid}")
        
        cap = f"💳 <b>WALLET RECHARGE</b>\n💰 Amount: <b>₹{amt}</b>\n\n📲 QR Code scan karein.\n⏳ <i>Note: Ye QR 10 minute mein expire ho jayega!</i>\n⚡ Payment hote hi balance auto-add ho jayega."
        m = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("✅ I Paid", callback_data=f"chk_qr|{order.order_id}"), InlineKeyboardButton("❌ Cancel", callback_data="cancel_qr"))
        
        bot.delete_message(cid, msg.message_id)
        sent_msg = bot.send_photo(cid, photo=order.qr_url, caption=cap, reply_markup=m, parse_mode="HTML")
        threading.Thread(target=poll_order_status, args=(order.order_id, cid, sent_msg.message_id, "wallet", amt), daemon=True).start()
    except:
        bot.send_message(cid, "⚠️ Sirf number type karein.")

def process_successful_payment(uid, code, p_name, amt):
    bot.send_message(uid, "🎉 <b>PAYMENT VERIFIED AUTOMATICALLY!</b> ✅\n\n⏳ Admin aapko jaldi hi account details send karenge!", parse_mode="HTML")
    cap = f"🔔 <b>NEW AUTO-PAYMENT VERIFIED!</b>\n📦 Plan: {p_name}\n👤 User ID: <code>{uid}</code>\n💰 Amount: ₹{amt}\nAction: Niche click karke ID/Pass bhejein:"
    m = InlineKeyboardMarkup().add(InlineKeyboardButton("🔑 Send ID/Pass", callback_data=f"reply_pass_{uid}"))
    bot.send_message(ADMIN_ID, cap, reply_markup=m, parse_mode="HTML")

if __name__ == '__main__':
    keep_alive()
    bot.remove_webhook()
    print("🚀 VIP V-Premium Bot is running with Auto FamGateway...")
    bot.infinity_polling(skip_pending=True)
                    
