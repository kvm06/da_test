from users.models import CustomUser
from django.core.mail import send_mail, EmailMessage


def send_emails_to_users(from_user, to_user):
    """Send message for two users who liked each other"""
    from_email = from_user.email
    recipient_list = [to_user.email]
    message = f'Вы нравитесь пользователю {from_user.first_name} {from_user.last_name}, его email: {from_user.email}'
    subject = 'Взаимная симпатия с пользователем'

    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list
    )

    email.send()
