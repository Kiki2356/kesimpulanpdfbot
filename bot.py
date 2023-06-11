import os
import telegram
from telegram.ext import Updater, MessageHandler, filters
import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Mengambil token bot dari environment variable
bot_token = os.getenv('BOT_TOKEN')
bot = telegram.Bot(token=bot_token)

# Fungsi untuk menangani pesan yang diterima
def handle_message(update, context):
    message = update.message
    chat_id = message.chat_id

    # Cek jika pesan berisi file PDF
    if message.document:
        file_id = message.document.file_id
        file = bot.get_file(file_id)
        file.download('input.pdf')
        text = extract_text_from_pdf('input.pdf')
    else:
        text = message.text

    # Membuat kesimpulan menggunakan pendekatan ekstraksi informasi
    summary = summarize_text(text)

    # Mengirimkan kesimpulan kembali ke pengguna
    bot.send_message(chat_id=chat_id, text=summary)

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

def summarize_text(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary_sentences = summarizer(parser.document, sentence_count=None)  # Tidak ada batasan jumlah kalimat
    summary = " ".join([str(sentence) for sentence in summary_sentences])
    return summary

def main():
    # Membuat objek updater dan dispatcher
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    # Menambahkan handler untuk pesan yang diterima
    message_handler = MessageHandler(filters.all, handle_message)
    dispatcher.add_handler(message_handler)

    # Memulai bot
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
