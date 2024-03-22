import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Sender:
    def __init__(self, email: str) -> None:
        self.email = email

    def send_with_attachment(attch) -> None:
        """Осуществляет отправку письма с вложением на указанный e-mail."""