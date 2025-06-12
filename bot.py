
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
import requests


TENURE, MONTHLY, TOTAL = range(3)
user_data = {}

TOKEN = "7227715692:AAGYXJiY0qjUkrGavMuk2EzFTvaMYhg39Fs"

API_URL = "http://127.0.0.1:5000/predict"  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Mijoz ketishini aniqlash uchun kerakli ma’lumotlarni kiriting.\nTenure (oy):")
    return TENURE

async def tenure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["tenure"] = float(update.message.text)
    await update.message.reply_text("MonthlyCharges:")
    return MONTHLY

async def monthly(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["MonthlyCharges"] = float(update.message.text)
    await update.message.reply_text("TotalCharges:")
    return TOTAL

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data["TotalCharges"] = float(update.message.text)

    
    
    user_data.update({
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check"
    })

    
    try:
        res = requests.post(API_URL, json=user_data)
        result = res.json()
        churn = result["churn"]
        prob = result["probability"]

        msg = f"📊 Bashorat: {'Ketadi' if churn else 'Qoladi'}\nEhtimollik: {prob * 100}%"
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text("Xatolik yuz berdi: " + str(e))

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bekor qilindi.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TENURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, tenure)],
            MONTHLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, monthly)],
            TOTAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, total)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
