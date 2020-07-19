import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import json
from email import encoders

with open("pkg/login.json", "r") as lg:
    LG = json.load(lg)

class EmailSender:
    def __init__(self):
        self.fromaddr = LG["email_sender"]
        self.toaddr = LG["email_recipient"]
    def send(self, file):
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = self.toaddr
        msg['Subject'] = "Perfect biking weather"
        body = "The weather seems to be good, check out the temperatures in the attached file"
        attachment = open(file, "rb")
        filename = "weather_table.xlsx"
        msg.attach(MIMEText(body, 'plain'))
        p = MIMEBase('application', 'vnd.ms-excel')

        # To change the payload into encoded form
        p.set_payload(attachment.read())

        attachment.close()

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', 'attachment', filename=filename)

        # attach the instance 'p' to instance 'msg'
        msg.attach(p)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.fromaddr, LG['email_password'])
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()
