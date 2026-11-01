import math
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# /start command အတွက်
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        " မင်္ဂလာပါ! Dami မှ ကြိုဆိုပါတယ်ရှင့်🧣\n\n"
        
    )
    await update.message.reply_text(welcome_text)

# စာသားရိုက်ပို့ပါက တွက်ချက်ပေးမည့် Function
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expression = update.message.text.strip()
    
    # မြန်မာဂဏန်း သို့မဟုတ် အခြား သင်္ချာသင်္ကေတများ ပြင်ဆင်ခြင်း
    expression = expression.replace('x', '*').replace('X', '*').replace('÷', '/')
    
    try:
        # ဘေးကင်းစွာ တွက်ချက်နိုင်ရန် eval သုံးထားခြင်း
        allowed_chars = "0123456789+-*/(). "
        if not all(c in allowed_chars for c in expression):
            await update.message.reply_text("⚠️ ကျေးဇူးပြု၍ ဂဏန်းနှင့် သင်္ချာသင်္ကေတ (+, -, *, /) များကိုသာ အသုံးပြုပါ။")
            return
            
        result = eval(expression)
        
        # ရလဒ်ကို ကောင်းမွန်စွာ ဖော်ပြခြင်း
        if isinstance(result, float) and result.is_integer():
            result = int(result)
            
        formatted_result = f"{result:,}"  # ဥပမာ 10000 ကို 10,000 ဖြစ်အောင် ကော်မာခြားပေးခြင်း
        
        await update.message.reply_text(f" **📋** `{expression}`\n **✅ ** `{ formatted_result } `", parse_mode='Markdown')
        
    except ZeroDivisionError:
        await update.message.reply_text("❌ 0 ဖြင့် စား၍ မရပါ။")
    except Exception:
        await update.message.reply_text("❌ တွက်ချက်မှု ပုံစံ မှားယွင်းနေပါသည်။ စာလုံးပေါင်းနှင့် သင်္ကေတများကို ပြန်စစ်ပေးပါ။")

if __name__ == '__main__':
    
    TOKEN = "8854143857:AAEcVMS9AzB0Bw8DiOABy9NUk5clSDgwu0U"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))
    
    print("Bot is running...")
    app.run_polling()
