import os
import sched
import smtplib
import time
from email.message import EmailMessage

from loguru import logger
import bash

base_path = os.path.split(os.path.realpath(__file__))[0]
log_path = os.path.join(base_path, 'output.log')
address_path = os.path.join(base_path, 'address.txt')
logger.add(log_path, colorize=True)
s = sched.scheduler(time.time, time.sleep)
INC = 60 * 60

def get_ip():
    ip_address = bash.run("ip address")

    if not os.path.exists(address_path):
        with open(address_path, 'w') as f:
            f.write('')

    with open(address_path, 'r') as f:
        file_address = f.read()
    
    if ip_address.output == file_address:
        return False

    with open(address_path, 'w') as f:
        f.write(ip_address.output)

    return True

def send_email():
    with open(address_path, 'r') as f:
        msg = EmailMessage()
        msg.set_content(f.read())

    msg['Subject'] = 'Raspberry PI update ip address'
    msg['From'] = 'tengshan2008@hotmail.com'
    msg['To'] = 'tengshan2008@hotmail.com'

    s = smtplib.SMTP('smtp.live.com')
    s.starttls()
    s.login('tengshan2008@hotmail.com', 'believedestiny')
    s.send_message(msg)
    s.quit()

def check_ip(inc):
    s.enter(inc, 0, check_ip, (inc,))
    logger.info('start check ip address')

    need_update = get_ip()
    if need_update:
        send_email()
        logger.info('have new ip address, send a email')

def check_job(inc=INC):
    s.enter(0, 0, check_ip, (inc,))
    s.run()

if __name__ == "__main__":
    check_job()
