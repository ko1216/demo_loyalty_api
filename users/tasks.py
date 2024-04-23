from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_sms(code, phone_number):
    """
    :param code: int number, length of 4 digits
    :param phone_number: user's phone number
    send a message with authentication code to user's phone. But now just imitate it and print a string to console
    """
    logger.info(f'send a code [{code}] to phone: {phone_number}')
    print(f'send a code [{code}] to phone: {phone_number}')
