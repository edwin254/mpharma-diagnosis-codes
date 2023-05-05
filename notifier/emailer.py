# subscriber.py
import json
import logging
import smtplib
import time

import redis

logger = logging.getLogger(__name__)

def send_email(receiver):

        sender = 'from@fromdomain.com'
        receivers = [receiver]

        message = f"""From: From Person <from@fromdomain.com>
        Subject: SMTP Diagnosis uploaded

        Diagnosis records uploaded.
        """

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message)
            logger.info( "Successfully sent email")

        except smtplib.SMTPException:
            logger.error( f"Error: unable to send email")


r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe("diagnosis_codes")

while True:
    message = p.get_message()
    if message:
         logger.info(f"Received message: {message.data}")
         send_email(data['receiver'])

    time.sleep(0.01)