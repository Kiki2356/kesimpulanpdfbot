from flask import Flask, render_template
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from fpdf import FPDF
import os

app = Flask(__name__)
bot_running = False

# Fungsi untuk mengolah file PDF dan membuat kesimpulan jurnal
def handle_upload_pdf(update, context):
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

def start(update, context):
    global bot_running
    bot_running = True
    update.message.reply_text('Bot Telegram telah diaktifkan.')

def run_bot():
    # Dapatkan token akses bot dari variabel lingkungan
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    # Buat objek updater dan pengendali dengan token akses
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    # Daftarkan handler perintah /start
    dp.add_handler(CommandHandler("start", start))

    # Daftarkan handler untuk mengunggah file PDF
    dp.add_handler(MessageHandler(Filters.document, handle_upload_pdf))

    # Jalankan bot
    updater.start_polling()

    # Matikan bot saat ditekan Ctrl+C
    updater.idle()

@app.route('/')
def index():
    return render_template('index.html', bot_running=bot_running)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
