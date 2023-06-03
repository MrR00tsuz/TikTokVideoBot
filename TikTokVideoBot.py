import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# /start komutunu işleyen bir fonksiyon
def start(update, context):
    update.message.reply_text('Videoları indirmek için linki gönderin.')

# HTML'den href değerini alarak linki döndüren fonksiyon
def get_download_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    link = soup.find('a', class_='tik-button-dl button dl-success')['href']
    return link

# Linki işleyen bir fonksiyon
def handle_link(update, context):
    link = update.message.text

    # Brave tarayıcısı için ChromeDriver'ı başlat
    brave_options = webdriver.ChromeOptions()
    brave_options.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Brave tarayıcının yolu
    brave_options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran olarak başlatmak için

    driver = webdriver.Chrome(executable_path=r"path/to/chromedriver", options=brave_options)  # ChromeDriver'ın yolu

    try:
        # Savetik.co sitesine git
        driver.get('https://savetik.co/tr?q=' + link)

        # XPath'in yüklenmesini bekleyin
        wait = WebDriverWait(driver, 10)  # 10 saniye boyunca bekleme süresi (değiştirebilirsiniz)

        # XPath'e göre düğmeyi bul
        xpath = '//a[contains(@class, "tik-button-dl") and contains(@class, "button") and contains(@class, "dl-success")]'
        button = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        button_html = button.get_attribute('outerHTML')

        # Düğme HTML kodundan download linkini al
        download_link = get_download_link(button_html)

        # Linki gönderen kişiye download linkini mesaj olarak gönder
        update.message.reply_text(download_link)

        # Video indirme tamamlandıktan sonra sayfayı kapatmak için bekle
        time.sleep(10)  # 10 saniye boyunca bekler (değiştirebilirsiniz)

    finally:
        # Tarayıcıyı kapat
        driver.quit()

# Telegram botunuzu başlatan kod
updater = Updater('BOT_TOKEN', use_context=True)  # Botunuzun TOKEN'ını buraya girin
dispatcher = updater.dispatcher

# /start komutunu işleyen bir handler (işleyici) ekliyoruz
dispatcher.add_handler(CommandHandler('start', start))

# Linki işleyen bir handler (işleyici) ekliyoruz
dispatcher.add_handler(MessageHandler(Filters.text, handle_link))

# Botu çalıştırıyoruz
updater.start_polling()
