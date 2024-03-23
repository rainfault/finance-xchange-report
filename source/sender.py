import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config import (email_password, 
                    email_sender, 
                    email_receiver, 
                    address, port,
                    EXCEL_FILEPATH )

class Sender:

    def send_with_attachment(self, rows: int) -> None:
        """Осуществляет отправку письма с вложением на указанный e-mail."""
        
        message = MIMEMultipart()
        message['From'] = email_sender
        message['To'] = email_receiver
        message['Subject'] = 'Report'

        # Указываю, сколько сток содержится в полученном xlsx файле:
        body = f"В полученной таблице содержится {rows} строк"

        last_digit = str(rows)[-1]

        if last_digit in ("0", "5", "6", "7", "8", "9"):
            body += "."
        elif last_digit == 1:
            body += "а."
        else:
            body += "и."

        message.attach(MIMEText(body, 'plain'))

        # Добавляю вложение
        attachment = open(EXCEL_FILEPATH, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + "report.xlsx")

        message.attach(part)
        
        self.connect_to_server_and_send(message)

    @staticmethod
    def connect_to_server_and_send(msg):
        """Отправка сообщения с вложением на указанный e-mail."""
        try:
            server = smtplib.SMTP_SSL(address, port, timeout=3)
            # server.starttls()
            server.login(email_sender, email_password)
            text = msg.as_string()
            server.sendmail(email_sender, email_receiver, text)
            server.quit()
            print("Письмо успешно отправлено!")
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")
