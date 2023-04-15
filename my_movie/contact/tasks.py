import requests
from celery import shared_task



@shared_task()
def send_message2boss():
    '''Notificate me about some event in Telegram'''
    TOKEN = '5984989128:AAEOXtMXwF15eFiSE4qRcc-bKihdqc9vN5o'
    message = 'Бла-бла-бла...'
    chat_id = '704339275'
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)
