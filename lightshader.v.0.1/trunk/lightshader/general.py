import smtplib
import email.utils
from email.mime.text import MIMEText
import webbrowser
import sys
import platform


def openUrl(url):
    webbrowser.open_new_tab(url)

def systemInfo():
    """ Returns relevant basic system information

        @return dict
    """

    systemDict = {'PyVersion': sys.version, 'PyExe': sys.executable, 'Node': platform.node(),
                  'OSRelease': platform.release(), 'OSVersion': platform.version(), 'Machine': platform.machine(),
                  'Processor': platform.processor()}

    return systemDict
