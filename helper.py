import smtplib
import os
from email.mime.text import MIMEText


def send_email(email, height, avg_height, count):
    """
    :param email: email address to send email to
    :param height: Height entered by the user
    :param avg_height: Avergae height calculated
    :param count: Total heights in the database
    """
    from_email = os.environ["FROM_EMAIL"]
    from_password = os.environ["FROM_PASSWORD"]
    to_email = email

    subject = "Height Data"
    message = """Your height is <strong>{}</strong>. Average height is <strong>{}</strong>
    and that is calculated out of <strong>{}</strong> people""".format(
        height, avg_height, count)

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
