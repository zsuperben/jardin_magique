import logging
import smtplib
from email.mime.text import MIMEText

_alertsConf = None
logger = logging.getLogger('api')

def init(conf):
    global _alertsConf
    _alertsConf = conf['alerts']

def alert(msg):
    if _alertsConf['mail'] == 'yes':
        try:
            sendMail(msg)
        except Exception as e:
            logger.error('Failed to send alert mail: %s' % e)

def sendMail(msg):
    msg = MIMEText('Le jardin magique est dans les choux: ' + msg)
    msg['Subject'] = 'Alerte du jardin magique'
    msg['From'] = _alertsConf['from']
    msg['To'] = ', '.join(_alertsConf['to'])
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(_alertsConf['from'], _alertsConf['to'], msg.as_string())
    smtp.quit()
