from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

import logging

logger = logging.getLogger(__name__)

def send_response_notification(response):
    message = f'''
        Новый отклик на объявление "{response.post.title}" от {response.author.username}:

        "{response.text}"

        Ссылка на объявление: http://127.0.0.1:8000{response.post.get_absolute_url}
    '''
    logger.info(message)

def send_status_change_notification(response):
    if response.status == 'accepted':
        status_text = 'принят'
    elif response.status == 'rejected':
        status_text = 'отклонен'
    else:
        return

    message = f'''
        Статус вашего отклика на объявление "{response.post.title}" изменён на "{status_text}".

        Ссылка на объявление: http://127.0.0.1:8000{response.post.get_absolute_url}
    '''
    logger.info(message)

def send_newsletter_email(subscription, newsletter):
    subject = newsletter.subject
    message = render_to_string('ads/newsletter_email.html', {'newsletter': newsletter})
    recipient_list = [subscription.user.email]
    logger.info(f"Отправка рассылки '{subject}' пользователю {recipient_list[0]}:\n{message}")

def send_registration_confirmation(user):
    subject = 'Подтверждение регистрации'
    message = f'''
        Здравствуйте, {user.username}!

        Для подтверждения регистрации на сайте перейдите по ссылке:
        http://127.0.0.1:8000/accounts/confirm/{user.registration_code}/

        С уважением,
        Команда сайта. 
    '''
    recipient_list = [user.email]
    logger.info(f"Отправка письма с кодом подтверждения на {recipient_list[0]}:\n{message}")