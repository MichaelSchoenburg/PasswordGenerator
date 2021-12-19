import secrets
import string
import time
import os
from pathlib import Path
from datetime import datetime
from shutil import copyfile
import sys
sys.path.append("Lib")
import pyperclip
from infi.systray import SysTrayIcon
from infi.systray.win32_adapter import IMAGE_ICON

pathThisApp = "{}/PasswordGenerator".format(os.getenv('APPDATA'))
pathHistoryFile = "{}/history.html".format(pathThisApp)

if not Path(pathThisApp).is_dir():
    Path(pathThisApp).mkdir(parents=True, exist_ok=True)
if not Path(pathHistoryFile).is_file():
    copyfile("history.html", pathHistoryFile)

def writeHistory(password):
    date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(pathHistoryFile, "r") as f:
        contents = f.readlines()
        s = """        <tr>
            <td class=\"tg-4lxc\">{}</td>
            <td class=\"tg-4lxc\">{}</td>
        </tr>
""".format(date, password)
        contents.insert(16, s)

    with open(pathHistoryFile, "w") as f:
        contents = "".join(contents)
        f.write(contents)

def genPw(len, alphabet, systray):
    password = ''.join(secrets.choice(alphabet) for i in range(len))
    pyperclip.copy(password)
    writeHistory(password)
    systray.update(icon="check.ico")
    time.sleep(1)
    systray.update(icon="secure.ico")

def genPwUnsec(systray):
    alphabet = string.ascii_letters
    len = 8
    genPw(len, alphabet, systray)

def genPwMed(systray):
    alphabet = string.ascii_letters + string.digits
    len = 14
    genPw(len, alphabet, systray)

def genPwSec(systray):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    len = 20
    genPw(len, alphabet, systray)

def showHistory(systray):
    os.popen(pathHistoryFile)

menu_options = (
    ('Histroy', "history.ico", showHistory),
    ('Generate password consisting of letters', "unsecure.ico", genPwUnsec),
    ('Generate password consisting of letters and numbers', "almost_secure.ico", genPwMed),
    ('Generate password consisting of letters, numbers and special characters', "secure.ico", genPwSec),
)

systray = SysTrayIcon("secure.ico", "Password Generator", menu_options, default_menu_index=3)

systray.start()
