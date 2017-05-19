import logging
import smtplib
from email.mime.text import MIMEText
from config import load_config

_alertsConf = None
logger = logging.getLogger('api')

def init():
    global _alertsConf
    _alertsConf = load_config()['alerts']

init()
def alert(msg):
    if _alertsConf['mail'] == 'yes':
        try:
            sendMail(msg)
        except Exception as e:
            logger.error('Failed to send alert mail: %s' % e)

def sendMail(msg):
    msg = MIMEText('Un probleme est survenu dans le jardin: ' + msg)
    msg['Subject'] = 'Alerte du jardin magique'
    msg['From'] = _alertsConf['from']
    msg['To'] = ', '.join(_alertsConf['to'])
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(_alertsConf['from'], _alertsConf['to'], msg.as_string())
    smtp.quit()
