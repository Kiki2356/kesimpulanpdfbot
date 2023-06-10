import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from fpdf import FPDF
from flask import Flask, render_template
from threading import Thread
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Inisialisasi status bot
bot_running = False
bot_error = ""

# Fungsi untuk memulai bot
def start_bot():
    global bot_running, bot_error
    try:
        # Mendapatkan token bot Telegram dari variabel lingkungan
        token = os.environ.get('TELEGRAM_BOT_TOKEN')

        # Buat objek updater dan pengendali
        updater = Updater(token, use_context=True)
        dp = updater.dispatcher

        # Daftarkan handler perintah /start
        dp.add_handler(CommandHandler("start", start))

        # Daftarkan handler untuk mengunggah file PDF
        dp.add_handler(MessageHandler(Filters.document, handle_upload_pdf))

        # Jalankan bot
        updater.start_polling()
        bot_running = True
    except Exception as e:
        bot_error = str(e)
        bot_running = False

# Fungsi untuk mengolah file PDF dan membuat kesimpulan jurnal
def handle_upload_pdf(update: Update, context):
    # Periksa apakah file PDF telah dikirimkan
    if not update.message.document:
        update.message.reply_text('Mohon unggah file PDF.')
        return

    # Dapatkan objek file PDF dari pesan
    pdf_file = update.message.document.get_file()
    pdf_file.download("input.pdf")

    # Proses file PDF dan buat kesimpulan jurnal

    # Buat PDF hasil kesimpulan
    output_pdf = FPDF()
    output_pdf.add_page()
    output_pdf.set_font("Arial", size=12)
    output_pdf.cell(200, 10, txt="Kesimpulan jurnal", ln=1, align="C")
    output_pdf.cell(200, 10, txt="Isi kesimpulan jurnal...", ln=2, align="L")

    # Simpan PDF hasil kesimpulan
    output_pdf.output("output.pdf")

    # Kirim PDF hasil kesimpulan ke pengguna
    context.bot.send_document(chat_id=update.effective_chat.id, document=open("output.pdf", "rb"))

# Route untuk halaman utama
@app.route("/")
def index():
    return render_template("index.html", bot_running=bot_running, bot_error=bot_error)

# Route untuk memulai bot
@app.route("/start")
def start():
    global bot_running, bot_error
    if not bot_running:
        # Memulai bot di dalam thread terpisah agar tidak menghentikan aplikasi Flask
        bot_thread = Thread(target=start_bot)
        bot_thread.start()
        bot_running = True
        bot_error = ""
    return "Bot telah dimulai"

# Menjalankan aplikasi Flask
if __name__ == "__main__":
    app.run()
