import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from fpdf import FPDF

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

def main():
    # Konfigurasi logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Buat objek updater dan pengendali
    updater = Updater("5649401123:AAHs97ocsxdZIm9Uc4tXsZZk8t68WxsodMw", use_context=True)
    dp = updater.dispatcher

    # Daftarkan handler perintah /start
    dp.add_handler(CommandHandler("start", start))

    # Daftarkan handler untuk mengunggah file PDF
    dp.add_handler(MessageHandler(Filters.document, handle_upload_pdf))

    # Jalankan bot
    updater.start_polling()

    # Matikan bot saat ditekan Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
