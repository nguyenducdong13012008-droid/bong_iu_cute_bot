import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ==================== CẤU HÌNH TOKEN ====================
# Thay token của bot anh vừa tạo và Chat ID của anh vào đây
TOKEN = "8823751597:AAH-z4AvizV04UFGWUBdI9qWv4PO2Zk3Qe0"
MY_CHAT_ID = "9154392502"

# ==================== LỜI NHẮN TỰ ĐỘNG ====================
LOH_KHUYEN = [
    "Anh nhớ uống thêm nước nhé!",
    "Làm xong nhớ kiểm tra lại kết quả 2 lần như anh dặn nha!",
    "Cố lên anh nhé, em luôn ủng hộ anh!",
    "Đừng thức khuya quá giữ sức khỏe nha anh!"
]

def tao_loi_nhan_thong_minh(noi_dung_goc):
    loi_khuyen = random.choice(LOH_KHUYEN)
    return f"🔔 **THÔNG BÁO TỪ BÔNG**\n\n📌 **Nội dung:** {noi_dung_goc}\n💡 **Lời nhắn nhỏ:** {loi_khuyen}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dạ em Bông đây ạ! Anh muốn em nhắc việc gì hay hẹn giờ cứ bảo em nhé!")

async def nhac_nho_job(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    loi_nhan = tao_loi_nhan_thong_minh(job.data)
    await context.bot.send_message(chat_id=job.chat_id, text=loi_nhan, parse_mode="Markdown")

async def hen_gio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        thoigian = int(context.args[0])
        noi_dung = " ".join(context.args[1:])
        context.job_queue.run_once(nhac_nho_job, thoigian, chat_id=update.effective_chat.id, data=noi_dung)
        await update.message.reply_text(f"Dạ em đã ghi nhận! Sau {thoigian} giây em sẽ nhắn báo cho anh ngay ạ.")
    except (IndexError, ValueError):
        await update.message.reply_text("Anh hãy nhập đúng cú pháp nha:\nVí dụ: `/nhac 60 Ôn lại bài`")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nhac", hen_gio))
    print("Bot Bông đang chạy trên điện thoại...")
    app.run_polling()
