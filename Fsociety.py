#!/usr/bin/env python3
# ███████╗███████╗ ██████╗  ██████╗██╗███████╗████████╗██╗   ██╗
# ██╔════╝██╔════╝██╔═══██╗██╔════╝██║██╔════╝╚══██╔══╝╚██╗ ██╔╝
# █████╗  ███████╗██║   ██║██║     ██║█████╗     ██║    ╚████╔╝
# ██╔══╝  ╚════██║██║   ██║██║     ██║██╔══╝     ██║     ╚██╔╝
# ██║     ███████║╚██████╔╝╚██████╗██║███████╗   ██║      ██║
# ╚═╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚══════╝   ╚═╝      ╚═╝
#
#                     Greet's To IcoDz - Canejo
#                       Tool For Hacking
#                       Author : Manisso
#                  Python 3 Upgrade: fsociety team

import sys
import argparse
import os
import subprocess
import re
import socket
import urllib.request
import urllib.parse
import http.client
import json
import telnetlib
import glob
import random
import queue
import threading
import base64
import time
import configparser
import itertools
from sys import argv
from getpass import getpass
from xml.dom import minidom
from urllib.parse import urlparse
from optparse import OptionParser
from time import gmtime, strftime, sleep
from datetime import datetime

# ─────────────────────────────────────────────────────────────
#  ANSI COLOR / STYLE CONSTANTS
# ─────────────────────────────────────────────────────────────

class color:
    HEADER    = '\033[95m'
    IMPORTANT = '\033[35m'
    NOTICE    = '\033[33m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    RED       = '\033[91m'
    END       = '\033[0m'
    UNDERLINE = '\033[4m'
    LOGGING   = '\033[34m'
    BOLD      = '\033[1m'
    CYAN      = '\033[96m'
    WHITE     = '\033[97m'
    DIM       = '\033[2m'
    BLINK     = '\033[5m'

# Palette used for logo colour cycling
COLOR_PALETTE = [
    color.RED, color.OKGREEN, color.CYAN, color.WARNING,
    color.HEADER, color.OKBLUE, color.IMPORTANT,
]

# ─────────────────────────────────────────────────────────────
#  TERMINAL HELPERS
# ─────────────────────────────────────────────────────────────

def clearScr():
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter(text, delay=0.03, color_code=''):
    """Print text with a typewriter effect."""
    end = color.END if color_code else ''
    for ch in text:
        sys.stdout.write(color_code + ch + end)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def box(lines, width=50, title='', color_code=color.OKGREEN):
    """Return a box-drawing string around the given lines."""
    inner = width - 2
    top_title = (' ' + title + ' ') if title else ''
    top_fill  = '─' * ((inner - len(top_title)) // 2)
    top_right = '─' * (inner - len(top_fill) - len(top_title))
    out  = color_code + '┌' + top_fill + top_title + top_right + '┐' + color.END + '\n'
    for line in lines:
        visible = _strip_ansi(line)
        pad = inner - len(visible)
        out += color_code + '│' + color.END + ' ' + line + ' ' * max(pad - 1, 0) + color_code + '│' + color.END + '\n'
    out += color_code + '└' + '─' * inner + '┘' + color.END
    return out

def _strip_ansi(s):
    """Remove ANSI escape codes for length calculation."""
    import re as _re
    return _re.sub(r'\033\[[0-9;]*m', '', s)

def spinner_run(label, func, *args, **kwargs):
    """Run func(*args, **kwargs) in a thread while showing a spinner."""
    frames = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    done   = threading.Event()
    result = [None]
    exc    = [None]

    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exc[0] = e
        finally:
            done.set()

    t = threading.Thread(target=target, daemon=True)
    t.start()
    idx = 0
    while not done.is_set():
        sys.stdout.write('\r  ' + color.OKGREEN + frames[idx % len(frames)] + color.END +
                         '  ' + color.CYAN + label + color.END + '   ')
        sys.stdout.flush()
        time.sleep(0.1)
        idx += 1
    sys.stdout.write('\r  ' + color.OKGREEN + '✓' + color.END +
                     '  ' + color.CYAN + label + color.END + '   \n')
    sys.stdout.flush()
    if exc[0]:
        raise exc[0]
    return result[0]

def live_clock():
    """Return a formatted current time string."""
    return datetime.now().strftime('%H:%M:%S')

def glitch_logo(logo_lines, iterations=6):
    """Flash the logo with random colour glitches."""
    glitch_chars = ['█','▓','▒','░','╬','╪','╫','╩','╦','╠','╣']
    colors = COLOR_PALETTE[:]
    for _ in range(iterations):
        c = random.choice(colors)
        clearScr()
        for line in logo_lines:
            # randomly corrupt a few characters
            corrupted = ''
            for ch in line:
                if ch != ' ' and random.random() < 0.04:
                    corrupted += random.choice(glitch_chars)
                else:
                    corrupted += ch
            print(c + corrupted + color.END)
        sys.stdout.flush()
        time.sleep(0.07)

def boot_sequence():
    """Animated boot sequence shown on first launch."""
    clearScr()
    messages = [
        (color.DIM   + color.OKGREEN, "[ SYSTEM INIT ]"),
        (color.OKGREEN,               "[ LOADING MODULES ... ]"),
        (color.OKGREEN,               "[ ESTABLISHING SECURE CHANNEL ... ]"),
        (color.WARNING,               "[ WARNING: UNAUTHORIZED ACCESS IS ILLEGAL ]"),
        (color.OKGREEN,               "[ FSOCIETY FRAMEWORK READY ]"),
    ]
    for col, msg in messages:
        typewriter('  ' + msg, delay=0.025, color_code=col)
        time.sleep(0.15)
    time.sleep(0.4)

# ─────────────────────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────────────────────

installDir = os.path.dirname(os.path.abspath(__file__)) + '/'
configFile = installDir + "fsociety.cfg"

config = configparser.RawConfigParser()
config.read(configFile)

toolDir = installDir + config.get('fsociety', 'toolDir')
logDir  = installDir + config.get('fsociety', 'logDir')
yes     = config.get('fsociety', 'yes').split()

# ─────────────────────────────────────────────────────────────
#  LOGO & PROMPTS
# ─────────────────────────────────────────────────────────────

LOGO_LINES = [
    "  ███████╗███████╗ ██████╗  ██████╗██╗███████╗████████╗██╗   ██╗",
    "  ██╔════╝██╔════╝██╔═══██╗██╔════╝██║██╔════╝╚══██╔══╝╚██╗ ██╔╝",
    "  █████╗  ███████╗██║   ██║██║     ██║█████╗     ██║    ╚████╔╝ ",
    "  ██╔══╝  ╚════██║██║   ██║██║     ██║██╔══╝     ██║     ╚██╔╝  ",
    "  ██║     ███████║╚██████╔╝╚██████╗██║███████╗   ██║      ██║   ",
    "  ╚═╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚══════╝   ╚═╝      ╚═╝  ",
]

alreadyInstalled = color.OKGREEN + "  ✓  Already installed" + color.END
continuePrompt   = "\n  Press [Return] to continue..."

termsAndConditions = color.NOTICE + '''
  I shall not use fsociety to:
  (i)  upload or otherwise transmit, display or distribute any content that
       infringes any trademark, trade secret, copyright or other proprietary
       or intellectual property rights of any person;
  (ii) upload or otherwise transmit any material that contains software
       viruses or any other computer code, files or programs designed to
       interrupt, destroy or limit the functionality of any computer
       software or hardware or telecommunications equipment;
''' + color.END

mrrobot4 = color.CYAN + '''
  Hello,

  As we all know, Mr. Robot 4.0 is the end of Mr. Robot.
  This framework has been upgraded to Python 3 to keep it running.
  Feel free to join the Discord: [ https://discord.gg/xB87X9z ]

  Thanks for reading,
  Zachary, CRO-THEHACKER - Dev
''' + color.END

# ─────────────────────────────────────────────────────────────
#  AGREEMENT
# ─────────────────────────────────────────────────────────────

def agreement():
    while not config.getboolean("fsociety", "agreement"):
        clearScr()
        print(termsAndConditions)
        print(mrrobot4)
        agree = input(color.WARNING + "  You must agree to our terms and conditions first (Y/n): " + color.END).lower()
        if agree in yes:
            config.set('fsociety', 'agreement', 'true')
            with open(configFile, 'w') as f:
                config.write(f)

def yesOrNo():
    return (input(color.WARNING + "  Continue Y / N: " + color.END) in yes)

# ─────────────────────────────────────────────────────────────
#  PROMPT HELPER
# ─────────────────────────────────────────────────────────────

def prompt(path='main'):
    return (color.OKGREEN + '[' + color.END +
            color.BOLD + color.RED + 'fsociety' + color.END +
            color.OKGREEN + ':' + color.END +
            color.CYAN + path + color.END +
            color.OKGREEN + ']' + color.END +
            color.WHITE + '~# ' + color.END)

# ─────────────────────────────────────────────────────────────
#  HEADER PRINTER
# ─────────────────────────────────────────────────────────────

def print_header(menu_name=''):
    """Print the glitchy logo + clock header."""
    logo_color = random.choice(COLOR_PALETTE)
    for line in LOGO_LINES:
        print(logo_color + line + color.END)
    clock_line = (color.DIM + '  ' + '─' * 30 +
                  '  ' + color.OKGREEN + '⏱  ' + live_clock() + color.END +
                  color.DIM + '  ' + '─' * 30 + color.END)
    print(clock_line)
    if menu_name:
        print(color.DIM + color.OKGREEN +
              '  ┌─ ' + color.END + color.BOLD + menu_name + color.END)
    print()

# ─────────────────────────────────────────────────────────────
#  INSTALL STATUS HELPER
# ─────────────────────────────────────────────────────────────

def install_badge(installed):
    if installed:
        return color.OKGREEN + ' ✓' + color.END
    return color.RED + ' ✗' + color.END

# ─────────────────────────────────────────────────────────────
#  WINDOWS COMPATIBILITY HELPER
# ─────────────────────────────────────────────────────────────

# Tools that have a native Windows installer available
WINDOWS_DOWNLOAD_LINKS = {
    'nmap':       ('Nmap',       'https://nmap.org/download.html'),
    'wpscan':     ('WPScan',     'https://github.com/wpscanteam/wpscan#installation'),
    'sqlmap':     ('sqlmap',     'https://github.com/sqlmapproject/sqlmap'),
    'wireshark':  ('Wireshark',  'https://www.wireshark.org/download.html'),
}

# Tools that are Linux-only (no Windows equivalent)
LINUX_ONLY_TOOLS = {
    'setoolkit', 'ssls', 'reaver', 'pixiewps', 'bluepot',
    'atscan', 'shellnoob', 'commix', 'gabriel', 'jboss',
    'bsqlbf', 'androidhash', 'cmsfew', 'pisher', 'smtpsend',
    'brutex', 'arachni', 'sitechecker', 'poet', 'weeman',
    'crips', 'CMSmap', 'XSStrike', 'doork', 'cupp',
    'maine', 'ifinurl', 'wppjmla', 'gravity', 'sqlscan',
    'wpminiscanner', 'wppluginscan', 'shelltarget',
    'joomlarce', 'vbulletinrce', 'Fscan',
}

def windows_not_supported(tool_name, extra_msg=''):
    """Print a friendly Windows-not-supported message."""
    print()
    print(color.RED + '  ╔══════════════════════════════════════════════════╗' + color.END)
    print(color.RED + '  ║  ⚠  Windows Not Supported                        ║' + color.END)
    print(color.RED + '  ╚══════════════════════════════════════════════════╝' + color.END)
    print()
    print(color.WARNING + '  ' + tool_name + color.END +
          color.WHITE + ' requires a Linux environment.' + color.END)
    if extra_msg:
        print(color.DIM + '  ' + extra_msg + color.END)
    print()
    print(color.CYAN + '  To run this tool, use one of:' + color.END)
    print(color.WHITE + '    • WSL  (Windows Subsystem for Linux)' + color.END)
    print(color.WHITE + '         wsl --install' + color.END)
    print(color.WHITE + '    • Docker  (already configured in this repo)' + color.END)
    print(color.WHITE + '         docker-compose up -d' + color.END)
    print(color.WHITE + '         docker-compose exec fsociety python3 fsociety.py' + color.END)
    print()

def check_windows(tool_name):
    """Return True if we should abort (Windows + Linux-only tool)."""
    if os.name == 'nt':
        windows_not_supported(tool_name)
        return True
    return False

# ─────────────────────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────────────────────

class fsociety:
    def __init__(self):
        clearScr()
        self.createFolders()
        glitch_logo(LOGO_LINES, iterations=5)
        clearScr()
        print_header()

        menu_items = [
            ('01', '🔍', 'Information Gathering'),
            ('02', '🔑', 'Password Attacks'),
            ('03', '📡', 'Wireless Testing'),
            ('04', '💀', 'Exploitation Tools'),
            ('05', '🌐', 'Sniffing & Spoofing'),
            ('06', '🔒', 'Web Hacking'),
            ('07', '🛠 ', 'Private Web Hacking'),
            ('08', '⚡', 'Post Exploitation'),
            ('00', '⬇ ', 'Install & Update'),
            ('11', '👥', 'Contributors'),
            ('99', '🚪', 'Exit'),
        ]

        lines = []
        for num, icon, label in menu_items:
            num_str  = color.OKGREEN + '[' + color.END + color.BOLD + num + color.END + color.OKGREEN + ']' + color.END
            icon_str = icon
            lbl_str  = color.WHITE + label + color.END
            lines.append('  ' + num_str + '  ' + icon_str + '  ' + lbl_str)

        print(box(lines, width=56, title=' MAIN MENU ', color_code=color.OKGREEN))
        print()

        choice = input(prompt('main'))
        clearScr()

        if choice == "1" or choice == "01":
            informationGatheringMenu()
        elif choice == "2" or choice == "02":
            passwordAttacksMenu()
        elif choice == "3" or choice == "03":
            wirelessTestingMenu()
        elif choice == "4" or choice == "04":
            exploitationToolsMenu()
        elif choice == "5" or choice == "05":
            sniffingSpoofingMenu()
        elif choice == "6" or choice == "06":
            webHackingMenu()
        elif choice == "7" or choice == "07":
            privateWebHacking()
        elif choice == "8" or choice == "08":
            postExploitationMenu()
        elif choice == "0" or choice == "00":
            self.update()
        elif choice == "11":
            self.githubContributors()
        elif choice == "99":
            with open(configFile, 'w') as f:
                config.write(f)
            print(color.OKGREEN + '\n  Goodbye. Stay safe out there.\n' + color.END)
            sys.exit()
        elif choice.strip() in ('', '\r', '\n'):
            self.__init__()
        else:
            try:
                os.system(choice)
            except Exception:
                pass
        self.completed()

    def githubContributors(self):
        clearScr()
        print_header('Contributors')
        contributorsURL = 'https://api.github.com/repos/manisso/fsociety/contributors'
        try:
            req  = urllib.request.Request(contributorsURL,
                                          headers={'User-Agent': 'fsociety-framework'})
            data = urllib.request.urlopen(req).read()
            contributors = json.loads(data)
            lines = []
            for c in contributors:
                lines.append(color.OKGREEN + '  ★  ' + color.END + color.WHITE + c['login'] + color.END)
            print(box(lines, width=50, title=' CONTRIBUTORS ', color_code=color.OKGREEN))
        except Exception as e:
            print(color.RED + '  Could not fetch contributors: ' + str(e) + color.END)
        print()

    def createFolders(self):
        if not os.path.isdir(toolDir):
            os.makedirs(toolDir)
        if not os.path.isdir(logDir):
            os.makedirs(logDir)

    def completed(self):
        input(color.DIM + continuePrompt + color.END)
        self.__init__()

    def update(self):
        print(color.OKGREEN + '  Updating fsociety...' + color.END)
        os.system("git clone --depth=1 https://github.com/Manisso/fsociety.git")
        os.system("cd fsociety && bash ./update.sh")
        os.system("fsociety")


# ─────────────────────────────────────────────────────────────
#  INFORMATION GATHERING MENU
# ─────────────────────────────────────────────────────────────

class informationGatheringMenu:
    def __init__(self):
        clearScr()
        print_header('Information Gathering')

        tools = [
            ('1', '🔍', 'Nmap',       nmap),
            ('2', '🛠 ', 'SEToolkit',  setoolkit),
            ('3', '🌐', 'Host To IP', host2ip),
            ('4', '🔒', 'WPScan',     wpscan),
            ('5', '🗺 ', 'CMSmap',     CMSmap),
            ('6', '⚡', 'XSStrike',   XSStrike),
            ('7', '🚪', 'Doork',      doork),
            ('8', '💀', 'Crips',      crips),
        ]

        lines = []
        for num, icon, label, cls in tools:
            try:
                inst = cls.__new__(cls)
                inst.installDir = toolDir + label.lower().replace(' ', '')
                badge = install_badge(os.path.isdir(inst.installDir))
            except Exception:
                badge = ''
            n = color.OKGREEN + '[' + color.END + color.BOLD + num.zfill(2) + color.END + color.OKGREEN + ']' + color.END
            lines.append('  ' + n + '  ' + icon + '  ' + color.WHITE + label + color.END + badge)
        lines.append('')
        lines.append('  ' + color.RED + '[99]' + color.END + '  🔙  ' + color.WHITE + 'Back to Main Menu' + color.END)

        print(box(lines, width=56, title=' INFO GATHERING ', color_code=color.OKBLUE))
        print()

        choice = input(prompt('info'))
        clearScr()

        dispatch = {'1': nmap, '2': setoolkit, '3': host2ip, '4': wpscan,
                    '5': CMSmap, '6': XSStrike, '7': doork, '8': crips}
        if choice in dispatch:
            dispatch[choice]()
        elif choice == "99":
            fsociety()
        else:
            self.__init__()
        self.completed()

    def completed(self):
        input(color.DIM + continuePrompt + color.END)
        self.__init__()


# ─────────────────────────────────────────────────────────────
#  INFORMATION GATHERING TOOL CLASSES
# ─────────────────────────────────────────────────────────────

class nmap:
    nmapLogo = color.OKGREEN + r"""
  ███╗   ██╗███╗   ███╗ █████╗ ██████╗
  ████╗  ██║████╗ ████║██╔══██╗██╔══██╗
  ██╔██╗ ██║██╔████╔██║███████║██████╔╝
  ██║╚██╗██║██║╚██╔╝██║██╔══██║██╔═══╝
  ██║ ╚████║██║ ╚═╝ ██║██║  ██║██║
  ╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝
""" + color.END

    def __init__(self):
        self.installDir = toolDir + "nmap"
        self.gitRepo    = "https://github.com/nmap/nmap.git"
        self.targetPrompt = "  Enter Target IP/Subnet/Range/Host: "

        if not self.installed():
            spinner_run("Installing nmap...", self.install)
        self.run()

    def installed(self):
        if os.name == 'nt':
            return os.path.isfile(r"C:\Program Files (x86)\Nmap\nmap.exe") or \
                   os.path.isfile(r"C:\Program Files\Nmap\nmap.exe")
        return (os.path.isfile("/usr/bin/nmap") or os.path.isfile("/usr/local/bin/nmap"))

    def install(self):
        if os.name == 'nt':
            print(color.WARNING + "\n  Nmap is not installed." + color.END)
            print(color.CYAN + "  Download and install from: https://nmap.org/download.html" + color.END)
            print(color.DIM + "  Then restart your terminal and try again.\n" + color.END)
            return
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        os.system("cd %s && ./configure && make && make install" % self.installDir)

    def run(self):
        clearScr()
        print(self.nmapLogo)
        target = input(color.CYAN + self.targetPrompt + color.END)
        self.menu(target)

    def menu(self, target):
        clearScr()
        print(self.nmapLogo)
        lines = [
            color.WHITE + '  Target: ' + color.OKGREEN + target + color.END,
            '',
            '  ' + color.OKGREEN + '[1]' + color.END + '  Simple Scan [-sV]',
            '  ' + color.OKGREEN + '[2]' + color.END + '  Port Scan [-Pn]',
            '  ' + color.OKGREEN + '[3]' + color.END + '  OS Detection [-A]',
            '',
            '  ' + color.RED    + '[99]' + color.END + ' Return to menu',
        ]
        print(box(lines, width=50, title=' NMAP ', color_code=color.OKGREEN))
        print()
        response = input(prompt('nmap'))
        clearScr()
        logPath = logDir + "nmap-" + strftime("%Y-%m-%d_%H-%M-%S", gmtime())
        # Use full path on Windows
        nmap_cmd = r'"C:\Program Files (x86)\Nmap\nmap.exe"' if os.name == 'nt' else 'nmap'
        if os.name == 'nt' and not os.path.isfile(r"C:\Program Files (x86)\Nmap\nmap.exe"):
            nmap_cmd = r'"C:\Program Files\Nmap\nmap.exe"'
        try:
            if response == "1":
                os.system("%s -sV -oN %s %s" % (nmap_cmd, logPath, target))
                input(continuePrompt)
            elif response == "2":
                os.system("%s -Pn -oN %s %s" % (nmap_cmd, logPath, target))
                input(continuePrompt)
            elif response == "3":
                os.system("%s -A -oN %s %s" % (nmap_cmd, logPath, target))
                input(continuePrompt)
            elif response == "99":
                pass
            else:
                self.menu(target)
        except KeyboardInterrupt:
            self.menu(target)


class setoolkit:
    def __init__(self):
        if check_windows('SEToolkit'): return
        self.installDir = toolDir + "setoolkit"
        self.gitRepo    = "https://github.com/trustedsec/social-engineer-toolkit.git"

        if not self.installed():
            spinner_run("Installing SEToolkit...", self.install)
        else:
            print(alreadyInstalled)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isfile("/usr/bin/setoolkit") or os.path.isdir(self.installDir)

    def install(self):
        os.system("apt-get --force-yes -y install git apache2 python3-requests "
                  "libapache2-mod-php python3-pexpect python3-openssl")
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        os.system("cd %s && python3 setup.py install" % self.installDir)

    def run(self):
        os.system("setoolkit")


class host2ip:
    host2ipLogo = color.CYAN + r"""
  ██╗  ██╗ ██████╗ ███████╗████████╗██████╗ ██╗██████╗
  ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝╚════██╗██║██╔══██╗
  ███████║██║   ██║███████╗   ██║    █████╔╝██║██████╔╝
  ██╔══██║██║   ██║╚════██║   ██║   ██╔═══╝ ██║██╔═══╝
  ██║  ██║╚██████╔╝███████║   ██║   ███████╗██║██║
  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝╚═╝
""" + color.END

    def __init__(self):
        clearScr()
        print(self.host2ipLogo)
        host = input(color.CYAN + "  Enter a Host: " + color.END)
        try:
            ip = socket.gethostbyname(host)
            print(color.OKGREEN + "  ✓  %s  →  %s" % (host, ip) + color.END)
        except socket.gaierror as e:
            print(color.RED + "  ✗  Could not resolve: " + str(e) + color.END)
        input(continuePrompt)


class wpscan:
    wpscanLogo = color.WARNING + r"""
  ██╗    ██╗██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗
  ██║    ██║██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║
  ██║ █╗ ██║██████╔╝███████╗██║     ███████║██╔██╗ ██║
  ██║███╗██║██╔═══╝ ╚════██║██║     ██╔══██║██║╚██╗██║
  ╚███╔███╔╝██║     ███████║╚██████╗██║  ██║██║ ╚████║
   ╚══╝╚══╝ ╚═╝     ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
""" + color.END

    def __init__(self):
        if check_windows('WPScan'): return
        self.installDir = toolDir + "wpscan"
        self.gitRepo    = "https://github.com/wpscanteam/wpscan.git"

        if not self.installed():
            spinner_run("Installing WPScan...", self.install)
        clearScr()
        print(self.wpscanLogo)
        target = input(color.CYAN + "  Enter a Target URL: " + color.END)
        self.menu(target)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def menu(self, target):
        clearScr()
        print(self.wpscanLogo)
        lines = [
            color.WHITE + '  Target: ' + color.OKGREEN + target + color.END,
            '',
            '  ' + color.OKGREEN + '[1]' + color.END + '  Username Enumeration [--enumerate u]',
            '  ' + color.OKGREEN + '[2]' + color.END + '  Plugin Enumeration   [--enumerate p]',
            '  ' + color.OKGREEN + '[3]' + color.END + '  Full Enumeration     [--enumerate]',
            '',
            '  ' + color.RED    + '[99]' + color.END + ' Return to menu',
        ]
        print(box(lines, width=54, title=' WPSCAN ', color_code=color.WARNING))
        print()
        response = input(prompt('wpscan'))
        clearScr()
        logPath = logDir + "wpscan-" + strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + ".txt"
        opts = "--no-banner --random-agent --url %s" % target
        try:
            if response == "1":
                os.system("ruby %s/wpscan.rb %s --enumerate u --log %s" % (self.installDir, opts, logPath))
                input(continuePrompt)
            elif response == "2":
                os.system("ruby %s/wpscan.rb %s --enumerate p --log %s" % (self.installDir, opts, logPath))
                input(continuePrompt)
            elif response == "3":
                os.system("ruby %s/wpscan.rb %s --enumerate --log %s" % (self.installDir, opts, logPath))
                input(continuePrompt)
            elif response == "99":
                pass
            else:
                self.menu(target)
        except KeyboardInterrupt:
            self.menu(target)


class CMSmap:
    CMSmapLogo = color.HEADER + r"""
   ██████╗███╗   ███╗███████╗███╗   ███╗ █████╗ ██████╗
  ██╔════╝████╗ ████║██╔════╝████╗ ████║██╔══██╗██╔══██╗
  ██║     ██╔████╔██║███████╗██╔████╔██║███████║██████╔╝
  ██║     ██║╚██╔╝██║╚════██║██║╚██╔╝██║██╔══██║██╔═══╝
  ╚██████╗██║ ╚═╝ ██║███████║██║ ╚═╝ ██║██║  ██║██║
   ╚═════╝╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝
""" + color.END

    def __init__(self):
        if check_windows('CMSmap'): return
        self.installDir = toolDir + "CMSmap"
        self.gitRepo    = "https://github.com/Dionach/CMSmap.git"

        if not self.installed():
            spinner_run("Installing CMSmap...", self.install)
        clearScr()
        print(self.CMSmapLogo)
        target = input(color.CYAN + "  Enter a Target URL: " + color.END)
        self.run(target)
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self, target):
        logPath = logDir + "cmsmap-" + strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + ".txt"
        try:
            os.system("python3 %s/cmsmap.py -t %s -o %s" % (self.installDir, target, logPath))
        except Exception:
            pass


class XSStrike:
    XSStrikeLogo = color.RED + r"""
  ██╗  ██╗███████╗███████╗████████╗██████╗ ██╗██╗  ██╗███████╗
  ╚██╗██╔╝██╔════╝██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝
   ╚███╔╝ ███████╗███████╗   ██║   ██████╔╝██║█████╔╝ █████╗
   ██╔██╗ ╚════██║╚════██║   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝
  ██╔╝ ██╗███████║███████║   ██║   ██║  ██║██║██║  ██╗███████╗
  ╚═╝  ╚═╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝
""" + color.END

    def __init__(self):
        if check_windows('XSStrike'): return
        self.installDir = toolDir + "XSStrike"
        self.gitRepo    = "https://github.com/UltimateHackers/XSStrike.git"

        if not self.installed():
            spinner_run("Installing XSStrike...", self.install)
        clearScr()
        print(self.XSStrikeLogo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        os.system("pip3 install -r %s/requirements.txt" % self.installDir)

    def run(self):
        os.system("python3 %s/xsstrike.py" % self.installDir)


class doork:
    doorkLogo = color.OKBLUE + r"""
  ██████╗  ██████╗  ██████╗ ██████╗ ██╗  ██╗
  ██╔══██╗██╔═══██╗██╔═══██╗██╔══██╗██║ ██╔╝
  ██║  ██║██║   ██║██║   ██║██████╔╝█████╔╝
  ██║  ██║██║   ██║██║   ██║██╔══██╗██╔═██╗
  ██████╔╝╚██████╔╝╚██████╔╝██║  ██║██║  ██╗
  ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
""" + color.END

    def __init__(self):
        if check_windows('Doork'): return
        self.installDir = toolDir + "doork"
        self.gitRepo    = "https://github.com/AeonDave/doork.git"

        if not self.installed():
            spinner_run("Installing Doork...", self.install)
        clearScr()
        print(self.doorkLogo)
        target = input(color.CYAN + "  Enter a Target URL: " + color.END)
        self.run(target)
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        os.system("pip3 install beautifulsoup4 requests")

    def run(self, target):
        if "http://" not in target and "https://" not in target:
            target = "http://" + target
        logPath = logDir + "doork-" + strftime("%Y-%m-%d_%H-%M-%S", gmtime()) + ".txt"
        try:
            os.system("python3 %s/doork.py -t %s -o %s" % (self.installDir, target, logPath))
        except KeyboardInterrupt:
            pass


class crips:
    cripsLogo = color.OKGREEN + r"""
   ██████╗██████╗ ██╗██████╗ ███████╗
  ██╔════╝██╔══██╗██║██╔══██╗██╔════╝
  ██║     ██████╔╝██║██████╔╝███████╗
  ██║     ██╔══██╗██║██╔═══╝ ╚════██║
  ╚██████╗██║  ██║██║██║     ███████║
   ╚═════╝╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝
""" + color.END

    def __init__(self):
        if check_windows('Crips'): return
        self.installDir = toolDir + "Crips"
        self.gitRepo    = "https://github.com/Manisso/Crips.git"

        if not self.installed():
            spinner_run("Installing Crips...", self.install)
        clearScr()
        print(self.cripsLogo)
        self.run()

    def installed(self):
        return (os.path.isdir(self.installDir) or
                os.path.isdir("/usr/share/doc/Crips"))

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        os.system("bash %s/install.sh" % self.installDir)

    def run(self):
        try:
            os.system("crips")
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────
#  PASSWORD ATTACKS MENU
# ─────────────────────────────────────────────────────────────

class passwordAttacksMenu:
    def __init__(self):
        clearScr()
        print_header('Password Attacks')

        lines = [
            '  ' + color.OKGREEN + '[01]' + color.END + '  🔑  ' + color.WHITE + 'Cupp  - Common User Passwords Profiler' + color.END,
            '  ' + color.OKGREEN + '[02]' + color.END + '  💀  ' + color.WHITE + 'BruteX - Brute force all services on target' + color.END,
            '',
            '  ' + color.RED    + '[99]' + color.END + '  🔙  ' + color.WHITE + 'Back to Main Menu' + color.END,
        ]
        print(box(lines, width=56, title=' PASSWORD ATTACKS ', color_code=color.RED))
        print()

        choice = input(prompt('passwd'))
        clearScr()

        if choice in ('1', '01'):
            cupp()
        elif choice in ('2', '02'):
            brutex()
        elif choice == "99":
            fsociety()
        else:
            self.__init__()
        self.completed()

    def completed(self):
        input(color.DIM + continuePrompt + color.END)
        self.__init__()


class cupp:
    cuppLogo = color.WARNING + r"""
   ██████╗██╗   ██╗██████╗ ██████╗
  ██╔════╝██║   ██║██╔══██╗██╔══██╗
  ██║     ██║   ██║██████╔╝██████╔╝
  ██║     ██║   ██║██╔═══╝ ██╔═══╝
  ╚██████╗╚██████╔╝██║     ██║
   ╚═════╝ ╚═════╝ ╚═╝     ╚═╝
""" + color.END

    def __init__(self):
        if check_windows('CUPP'): return
        self.installDir = toolDir + "cupp"
        self.gitRepo    = "https://github.com/Mebus/cupp.git"

        if not self.installed():
            spinner_run("Installing CUPP...", self.install)
        clearScr()
        print(self.cuppLogo)
        self.run()

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        os.system("python3 %s/cupp.py -i" % self.installDir)


class brutex:
    brutexLogo = color.RED + r"""
  ██████╗ ██████╗ ██╗   ██╗████████╗███████╗██╗  ██╗
  ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝╚██╗██╔╝
  ██████╔╝██████╔╝██║   ██║   ██║   █████╗   ╚███╔╝
  ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝   ██╔██╗
  ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗██╔╝ ██╗
  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝
""" + color.END

    def __init__(self):
        if check_windows('BruteX'): return
        self.installDir = toolDir + "brutex"
        self.gitRepo    = "https://github.com/1N3/BruteX.git"

        if not self.installed():
            spinner_run("Installing BruteX...", self.install)
        clearScr()
        print(self.brutexLogo)
        self.run()

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        if not os.path.isdir("/usr/share/brutex"):
            os.makedirs("/usr/share/brutex")
        os.system("cd %s && chmod +x install.sh && ./install.sh" % self.installDir)

    def run(self):
        target = input(color.CYAN + "  Enter Target IP: " + color.END)
        os.system("brutex %s" % target)


# ─────────────────────────────────────────────────────────────
#  WIRELESS TESTING MENU
# ─────────────────────────────────────────────────────────────

class wirelessTestingMenu:
    def __init__(self):
        clearScr()
        print_header('Wireless Testing')

        lines = [
            '  ' + color.OKGREEN + '[01]' + color.END + '  📡  ' + color.WHITE + 'Reaver  - WPS PIN attack' + color.END,
            '  ' + color.OKGREEN + '[02]' + color.END + '  ⚡  ' + color.WHITE + 'PixieWPS - Offline WPS brute force' + color.END,
            '  ' + color.OKGREEN + '[03]' + color.END + '  🔵  ' + color.WHITE + 'BluePot  - Bluetooth Honeypot GUI' + color.END,
            '',
            '  ' + color.RED    + '[99]' + color.END + '  🔙  ' + color.WHITE + 'Back to Main Menu' + color.END,
        ]
        print(box(lines, width=56, title=' WIRELESS TESTING ', color_code=color.CYAN))
        print()

        choice = input(prompt('wireless'))
        clearScr()

        if choice in ('1', '01'):
            reaver()
        elif choice in ('2', '02'):
            pixiewps()
        elif choice in ('3', '03'):
            bluepot()
        elif choice == "99":
            fsociety()
        else:
            self.__init__()
        self.completed()

    def completed(self):
        input(color.DIM + continuePrompt + color.END)
        self.__init__()


class reaver:
    reaverLogo = color.CYAN + r"""
  ██████╗ ███████╗ █████╗ ██╗   ██╗███████╗██████╗
  ██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗
  ██████╔╝█████╗  ███████║██║   ██║█████╗  ██████╔╝
  ██╔══██╗██╔══╝  ██╔══██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
  ██║  ██║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║
  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
""" + color.END

    def __init__(self):
        if check_windows('Reaver'): return
        self.installDir = toolDir + "reaver"
        self.gitRepo    = "https://github.com/t6x/reaver-wps-fork-t6x.git"

        if not self.installed():
            spinner_run("Installing Reaver...", self.install)
        clearScr()
        print(self.reaverLogo)
        self.run()

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        os.system("apt-get -y install build-essential libpcap-dev sqlite3 "
                  "libsqlite3-dev aircrack-ng pixiewps")
        os.system("cd %s/src && ./configure && make && sudo make install" % self.installDir)

    def run(self):
        os.system("reaver --help")


class pixiewps:
    pixiewpsLogo = color.OKBLUE + r"""
  ██████╗ ██╗██╗  ██╗██╗███████╗██╗    ██╗██████╗ ███████╗
  ██╔══██╗██║╚██╗██╔╝██║██╔════╝██║    ██║██╔══██╗██╔════╝
  ██████╔╝██║ ╚███╔╝ ██║█████╗  ██║ █╗ ██║██████╔╝███████╗
  ██╔═══╝ ██║ ██╔██╗ ██║██╔══╝  ██║███╗██║██╔═══╝ ╚════██║
  ██║     ██║██╔╝ ██╗██║███████╗╚███╔███╔╝██║     ███████║
  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝     ╚══════╝
""" + color.END

    def __init__(self):
        if check_windows('PixieWPS'): return
        self.installDir = toolDir + "pixiewps"
        self.gitRepo    = "https://github.com/wiire/pixiewps.git"

        if not self.installed():
            spinner_run("Installing PixieWPS...", self.install)
        clearScr()
        print(self.pixiewpsLogo)
        self.run()

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        os.system("apt-get -y install build-essential")
        os.system("cd %s && make && sudo make install" % self.installDir)

    def run(self):
        os.system("pixiewps --help")


class bluepot:
    bluepotLogo = color.OKBLUE + r"""
  ██████╗ ██╗     ██╗   ██╗███████╗██████╗  ██████╗ ████████╗
  ██╔══██╗██║     ██║   ██║██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
  ██████╔╝██║     ██║   ██║█████╗  ██████╔╝██║   ██║   ██║
  ██╔══██╗██║     ██║   ██║██╔══╝  ██╔═══╝ ██║   ██║   ██║
  ██████╔╝███████╗╚██████╔╝███████╗██║     ╚██████╔╝   ██║
  ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝╚═╝      ╚═════╝    ╚═╝
""" + color.END

    def __init__(self):
        if check_windows('BluePot'): return
        self.installDir = toolDir + "bluepot"

        if not self.installed():
            spinner_run("Installing BluePot...", self.install)
        clearScr()
        print(self.bluepotLogo)
        self.run()

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("apt-get install libbluetooth-dev")
        os.system("wget -O - https://github.com/andrewmichaelsmith/bluepot/raw/master/"
                  "bin/bluepot-0.1.tar.gz | tar xfz -")
        os.system("mv bluepot/ %s/" % self.installDir)

    def run(self):
        os.system("sudo java -jar %s/BluePot-0.1.jar" % self.installDir)


# ─────────────────────────────────────────────────────────────
#  EXPLOITATION TOOLS MENU
# ─────────────────────────────────────────────────────────────

class exploitationToolsMenu:
    def __init__(self):
        clearScr()
        print_header('Exploitation Tools')

        lines = [
            '  ' + color.OKGREEN + '[01]' + color.END + '  💀  ' + color.WHITE + 'ATSCAN  - Advanced Target Scanner' + color.END,
            '  ' + color.OKGREEN + '[02]' + color.END + '  💉  ' + color.WHITE + 'sqlmap  - SQL Injection & Takeover' + color.END,
            '  ' + color.OKGREEN + '[03]' + color.END + '  🐚  ' + color.WHITE + 'Shellnoob - Shellcode writing toolkit' + color.END,
            '  ' + color.OKGREEN + '[04]' + color.END + '  ⚡  ' + color.WHITE + 'commix  - Command Injection Exploiter' + color.END,
            '  ' + color.OKGREEN + '[05]' + color.END + '  📂  ' + color.WHITE + 'FTP Auto Bypass (gabriel)' + color.END,
            '  ' + color.OKGREEN + '[06]' + color.END + '  ☕  ' + color.WHITE + 'JBoss-Autopwn' + color.END,
            '  ' + color.OKGREEN + '[07]' + color.END + '  🔍  ' + color.WHITE + 'bsqlbf  - Blind SQL Injection' + color.END,
            '  ' + color.OKGREEN + '[08]' + color.END + '  📱  ' + color.WHITE + 'Android Hash Bruteforce' + color.END,
            '  ' + color.OKGREEN + '[09]' + color.END + '  🌐  ' + color.WHITE + 'cmsfew  - Joomla SQL Scanner' + color.END,
            '',
            '  ' + color.RED    + '[99]' + color.END + '  🔙  ' + color.WHITE + 'Back to Main Menu' + color.END,
        ]
        print(box(lines, width=58, title=' EXPLOITATION TOOLS ', color_code=color.RED))
        print()

        choice = input(prompt('exploit'))
        clearScr()

        dispatch = {
            '1': atscan, '01': atscan,
            '2': sqlmap, '02': sqlmap,
            '3': shellnoob, '03': shellnoob,
            '4': commix, '04': commix,
            '5': gabriel, '05': gabriel,
            '6': jboss, '06': jboss,
            '7': bsqlbf, '07': bsqlbf,
            '8': androidhash, '08': androidhash,
            '9': cmsfew, '09': cmsfew,
        }
        if choice in dispatch:
            dispatch[choice]()
        elif choice == "99":
            fsociety()
        else:
            self.__init__()
        self.completed()

    def completed(self):
        input(color.DIM + continuePrompt + color.END)
        self.__init__()


# ─── Exploitation Tool Stubs ──────────────────────────────────

def _make_tool_logo(name, color_code):
    return color_code + r"""
  ╔══════════════════════════════════════╗
  ║  """ + name.ljust(36) + r"""║
  ╚══════════════════════════════════════╝
""" + color.END


class atscan:
    logo = _make_tool_logo('ATSCAN - Advanced Target Scanner', color.RED)

    def __init__(self):
        if check_windows('ATSCAN'): return
        self.installDir = toolDir + "atscan"
        self.gitRepo    = "https://github.com/AlisamTechnology/ATSCAN.git"

        if not self.installed():
            spinner_run("Installing ATSCAN...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        os.system("cd %s && chmod +x atscan.pl" % self.installDir)

    def run(self):
        os.system("perl %s/atscan.pl --help" % self.installDir)


class sqlmap:
    logo = _make_tool_logo('sqlmap - SQL Injection & Takeover Tool', color.WARNING)

    def __init__(self):
        if check_windows('sqlmap'): return
        self.installDir = toolDir + "sqlmap"
        self.gitRepo    = "https://github.com/sqlmapproject/sqlmap.git"

        if not self.installed():
            spinner_run("Installing sqlmap...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/sqlmap.py -u %s --dbs" % (self.installDir, target))


class shellnoob:
    logo = _make_tool_logo('Shellnoob - Shellcode Writing Toolkit', color.OKGREEN)

    def __init__(self):
        if check_windows('Shellnoob'): return
        self.installDir = toolDir + "shellnoob"
        self.gitRepo    = "https://github.com/reyammer/shellnoob.git"

        if not self.installed():
            spinner_run("Installing Shellnoob...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        os.system("python3 %s/shellnoob.py --help" % self.installDir)


class commix:
    logo = _make_tool_logo('commix - Command Injection Exploiter', color.RED)

    def __init__(self):
        if check_windows('commix'): return
        self.installDir = toolDir + "commix"
        self.gitRepo    = "https://github.com/commixproject/commix.git"

        if not self.installed():
            spinner_run("Installing commix...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/commix.py --url=%s" % (self.installDir, target))


class gabriel:
    logo = _make_tool_logo('gabriel - FTP Auto Bypass', color.OKBLUE)

    def __init__(self):
        if check_windows('gabriel'): return
        self.installDir = toolDir + "gabriel"
        self.gitRepo    = "https://github.com/Manisso/gabriel.git"

        if not self.installed():
            spinner_run("Installing gabriel...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target IP: " + color.END)
        os.system("python3 %s/gabriel.py %s" % (self.installDir, target))


class jboss:
    logo = _make_tool_logo('JBoss-Autopwn - JBoss Exploitation', color.WARNING)

    def __init__(self):
        if check_windows('JBoss-Autopwn'): return
        self.installDir = toolDir + "jboss"
        self.gitRepo    = "https://github.com/SpiderLabs/jboss-autopwn.git"

        if not self.installed():
            spinner_run("Installing JBoss-Autopwn...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("bash %s/jboss-autopwn-linux.sh %s" % (self.installDir, target))


class bsqlbf:
    logo = _make_tool_logo('bsqlbf - Blind SQL Injection Brute Force', color.RED)

    def __init__(self):
        if check_windows('bsqlbf'): return
        self.installDir = toolDir + "bsqlbf"
        self.gitRepo    = "https://github.com/Manisso/bsqlbf.git"

        if not self.installed():
            spinner_run("Installing bsqlbf...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("perl %s/bsqlbf.pl -url %s" % (self.installDir, target))


class androidhash:
    logo = _make_tool_logo('androidhash - Android Passcode Bruteforce', color.OKGREEN)

    def __init__(self):
        if check_windows('androidhash'): return
        self.installDir = toolDir + "androidhash"
        self.gitRepo    = "https://github.com/Manisso/androidhash.git"

        if not self.installed():
            spinner_run("Installing androidhash...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        hash_val = input(color.CYAN + "  Enter Hash: " + color.END)
        salt_val = input(color.CYAN + "  Enter Salt: " + color.END)
        os.system("python3 %s/androidhash.py %s %s" % (self.installDir, hash_val, salt_val))


class cmsfew:
    logo = _make_tool_logo('cmsfew - Joomla SQL Injection Scanner', color.HEADER)

    def __init__(self):
        if check_windows('cmsfew'): return
        self.installDir = toolDir + "cmsfew"
        self.gitRepo    = "https://github.com/Manisso/cmsfew.git"

        if not self.installed():
            spinner_run("Installing cmsfew...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/cmsfew.py %s" % (self.installDir, target))


# ─────────────────────────────────────────────────────────────
#  SNIFFING & SPOOFING MENU
# ─────────────────────────────────────────────────────────────

class sniffingSpoofingMenu:
    def __init__(self):
        clearScr()
        print_header('Sniffing & Spoofing')

        lines = [
            '  ' + color.OKGREEN + '[01]' + color.END + '  🛠 ' + color.WHITE + 'SEToolkit  - Social Engineering Toolkit' + color.END,
            '  ' + color.OKGREEN + '[02]' + color.END + '  🔒  ' + color.WHITE + 'SSLstrip   - MITM SSL Stripping' + color.END,
            '  ' + color.OKGREEN + '[03]' + color.END + '  🎣  ' + color.WHITE + 'pyPISHER   - Malicious phishing site creator' + color.END,
            '  ' + color.OKGREEN + '[04]' + color.END + '  📧  ' + color.WHITE + 'SMTP Mailer - Send SMTP mail' + color.END,
            '',
            '  ' + color.RED    + '[99]' + color.END + '  🔙  ' + color.WHITE + 'Back to Main Menu' + color.END,
        ]
        print(box(lines, width=58, title=' SNIFFING & SPOOFING ', color_code=color.OKBLUE))
        print()

        choice = input(prompt('sniff'))
        clearScr()

        if choice in ('1', '01'):
            setoolkit()
        elif choice in ('2', '02'):
            ssls()
        elif choice in ('3', '03'):
            pisher()
        elif choice in ('4', '04'):
            smtpsend()
        elif choice == "99":
            fsociety()
        else:
            self.__init__()
        self.completed()

    def completed(self):
        input(color.DIM + continuePrompt + color.END)
        self.__init__()


class ssls:
    logo = _make_tool_logo('SSLstrip - MITM SSL Stripping Attack', color.OKBLUE)

    def __init__(self):
        if check_windows('SSLstrip'): return
        self.installDir = toolDir + "sslstrip"
        self.gitRepo    = "https://github.com/moxie0/sslstrip.git"

        if not self.installed():
            spinner_run("Installing SSLstrip...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        os.system("cd %s && python3 setup.py install" % self.installDir)

    def run(self):
        port = input(color.CYAN + "  Enter listen port [default 10000]: " + color.END) or "10000"
        os.system("python3 %s/sslstrip.py -l %s" % (self.installDir, port))


class pisher:
    logo = _make_tool_logo('pyPISHER - Phishing Site Creator', color.WARNING)

    def __init__(self):
        if check_windows('pyPISHER'): return
        self.installDir = toolDir + "pisher"
        self.gitRepo    = "https://github.com/Manisso/pisher.git"

        if not self.installed():
            spinner_run("Installing pyPISHER...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        os.system("python3 %s/pisher.py" % self.installDir)


class smtpsend:
    logo = _make_tool_logo('SMTP Mailer - Send SMTP Mail', color.OKGREEN)

    def __init__(self):
        if check_windows('SMTP Mailer'): return
        self.installDir = toolDir + "smtpsend"
        self.gitRepo    = "https://github.com/Manisso/smtpsend.git"

        if not self.installed():
            spinner_run("Installing SMTP Mailer...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        os.system("python3 %s/smtpsend.py" % self.installDir)


# ─────────────────────────────────────────────────────────────
#  WEB HACKING MENU
# ─────────────────────────────────────────────────────────────

class webHackingMenu:
    def __init__(self):
        clearScr()
        print_header('Web Hacking')

        lines = [
            '  ' + color.OKGREEN + '[01]' + color.END + '  🌐  ' + color.WHITE + 'Drupal Hacking' + color.END,
            '  ' + color.OKGREEN + '[02]' + color.END + '  🔍  ' + color.WHITE + 'Inurlbr' + color.END,
            '  ' + color.OKGREEN + '[03]' + color.END + '  🔒  ' + color.WHITE + 'WordPress & Joomla Scanner' + color.END,
            '  ' + color.OKGREEN + '[04]' + color.END + '  📋  ' + color.WHITE + 'Gravity Form Scanner' + color.END,
            '  ' + color.OKGREEN + '[05]' + color.END + '  📂  ' + color.WHITE + 'File Upload Checker' + color.END,
            '  ' + color.OKGREEN + '[06]' + color.END + '  🔎  ' + color.WHITE + 'WordPress Exploit Scanner' + color.END,
            '  ' + color.OKGREEN + '[07]' + color.END + '  🔌  ' + color.WHITE + 'WordPress Plugins Scanner' + color.END,
            '  ' + color.OKGREEN + '[08]' + color.END + '  🐚  ' + color.WHITE + 'Shell & Directory Finder' + color.END,
            '  ' + color.OKGREEN + '[09]' + color.END + '  💀  ' + color.WHITE + 'Joomla! 1.5-3.4.5 RCE' + color.END,
            '  ' + color.OKGREEN + '[10]' + color.END + '  ⚡  ' + color.WHITE + 'vBulletin 5.X RCE' + color.END,
            '  ' + color.OKGREEN + '[11]' + color.END + '  🔑  ' + color.WHITE + 'BruteX - Brute force all services' + color.END,
            '  ' + color.OKGREEN + '[12]' + color.END + '  🕷 ' + color.WHITE + 'Arachni - Web App Security Scanner' + color.END,
            '',
            '  ' + color.RED    + '[99]' + color.END + '  🔙  ' + color.WHITE + 'Back to Main Menu' + color.END,
        ]
        print(box(lines, width=58, title=' WEB HACKING ', color_code=color.OKGREEN))
        print()

        choice = input(prompt('web'))
        clearScr()

        dispatch = {
            '1': maine, '01': maine,
            '2': ifinurl, '02': ifinurl,
            '3': wppjmla, '03': wppjmla,
            '4': gravity, '04': gravity,
            '5': sqlscan, '05': sqlscan,
            '6': wpminiscanner, '06': wpminiscanner,
            '7': wppluginscan, '07': wppluginscan,
            '8': shelltarget, '08': shelltarget,
            '9': joomlarce, '09': joomlarce,
            '10': vbulletinrce,
            '11': brutex, '11': brutex,
            '12': arachni, '12': arachni,
        }
        if choice in dispatch:
            dispatch[choice]()
        elif choice == "99":
            fsociety()
        else:
            self.__init__()
        self.completed()

    def completed(self):
        input(color.DIM + continuePrompt + color.END)
        self.__init__()


# ─── Web Hacking Tool Stubs ───────────────────────────────────

class maine:
    logo = _make_tool_logo('Drupal Hacking Tool', color.WARNING)

    def __init__(self):
        if check_windows('Drupal Hacking'): return
        self.installDir = toolDir + "drupal-hacking"
        self.gitRepo    = "https://github.com/Manisso/drupal-hacking.git"
        if not self.installed():
            spinner_run("Installing Drupal Hacking...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/drupal.py %s" % (self.installDir, target))


class ifinurl:
    logo = _make_tool_logo('Inurlbr - Advanced Search in URLs', color.OKBLUE)

    def __init__(self):
        if check_windows('Inurlbr'): return
        self.installDir = toolDir + "inurlbr"
        self.gitRepo    = "https://github.com/googleinurl/SCANNER-INURLBR.git"
        if not self.installed():
            spinner_run("Installing Inurlbr...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        query = input(color.CYAN + "  Enter Search Query: " + color.END)
        os.system("php %s/inurlbr.php --dork '%s' -s output.txt" % (self.installDir, query))


class wppjmla:
    logo = _make_tool_logo('WordPress & Joomla Scanner', color.OKGREEN)

    def __init__(self):
        if check_windows('WP/Joomla Scanner'): return
        self.installDir = toolDir + "wppjmla"
        self.gitRepo    = "https://github.com/Manisso/wppjmla.git"
        if not self.installed():
            spinner_run("Installing WP/Joomla Scanner...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/scanner.py %s" % (self.installDir, target))


class gravity:
    logo = _make_tool_logo('Gravity Form Scanner', color.HEADER)

    def __init__(self):
        if check_windows('Gravity Scanner'): return
        self.installDir = toolDir + "gravity"
        self.gitRepo    = "https://github.com/Manisso/gravity.git"
        if not self.installed():
            spinner_run("Installing Gravity Scanner...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/gravity.py %s" % (self.installDir, target))


class sqlscan:
    logo = _make_tool_logo('File Upload Checker', color.RED)

    def __init__(self):
        if check_windows('File Upload Checker'): return
        self.installDir = toolDir + "sqlscan"
        self.gitRepo    = "https://github.com/Manisso/sqlscan.git"
        if not self.installed():
            spinner_run("Installing File Upload Checker...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/sqlscan.py %s" % (self.installDir, target))


class wpminiscanner:
    logo = _make_tool_logo('WordPress Exploit Scanner', color.WARNING)

    def __init__(self):
        if check_windows('WP Exploit Scanner'): return
        self.installDir = toolDir + "wpminiscanner"
        self.gitRepo    = "https://github.com/Manisso/wpminiscanner.git"
        if not self.installed():
            spinner_run("Installing WP Exploit Scanner...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/wpminiscanner.py %s" % (self.installDir, target))


class wppluginscan:
    logo = _make_tool_logo('WordPress Plugins Scanner', color.OKBLUE)

    def __init__(self):
        if check_windows('WP Plugin Scanner'): return
        self.installDir = toolDir + "wppluginscan"
        self.gitRepo    = "https://github.com/Manisso/wppluginscan.git"
        if not self.installed():
            spinner_run("Installing WP Plugin Scanner...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/wppluginscan.py %s" % (self.installDir, target))


class shelltarget:
    logo = _make_tool_logo('Shell & Directory Finder', color.OKGREEN)

    def __init__(self):
        if check_windows('Shell Finder'): return
        self.installDir = toolDir + "shelltarget"
        self.gitRepo    = "https://github.com/Manisso/shelltarget.git"
        if not self.installed():
            spinner_run("Installing Shell Finder...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/shelltarget.py %s" % (self.installDir, target))


class joomlarce:
    logo = _make_tool_logo('Joomla! 1.5-3.4.5 Remote Code Execution', color.RED)

    def __init__(self):
        if check_windows('Joomla RCE'): return
        self.installDir = toolDir + "joomlarce"
        self.gitRepo    = "https://github.com/Manisso/joomlarce.git"
        if not self.installed():
            spinner_run("Installing Joomla RCE...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/joomlarce.py %s" % (self.installDir, target))


class vbulletinrce:
    logo = _make_tool_logo('vBulletin 5.X Remote Code Execution', color.RED)

    def __init__(self):
        if check_windows('vBulletin RCE'): return
        self.installDir = toolDir + "vbulletinrce"
        self.gitRepo    = "https://github.com/Manisso/vbulletinrce.git"
        if not self.installed():
            spinner_run("Installing vBulletin RCE...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("python3 %s/vbulletinrce.py %s" % (self.installDir, target))


class arachni:
    logo = _make_tool_logo('Arachni - Web Application Security Scanner', color.HEADER)

    def __init__(self):
        if check_windows('Arachni'): return
        self.installDir = toolDir + "arachni"
        self.gitRepo    = "https://github.com/Arachni/arachni.git"
        if not self.installed():
            spinner_run("Installing Arachni...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Target URL: " + color.END)
        os.system("%s/bin/arachni %s" % (self.installDir, target))


# ─────────────────────────────────────────────────────────────
#  PRIVATE WEB HACKING MENU
# ─────────────────────────────────────────────────────────────

class privateWebHacking:
    def __init__(self):
        clearScr()
        print_header('Private Web Hacking')

        lines = [
            color.WHITE + '  Full-spectrum scan against a private target IP.' + color.END,
            color.DIM   + '  Uses Fscan to enumerate all open services.' + color.END,
        ]
        print(box(lines, width=56, title=' PRIVATE WEB HACKING ', color_code=color.RED))
        print()

        target = input(color.CYAN + "  Enter Target IP: " + color.END)
        Fscan(target)
        self.completed()

    def completed(self):
        input(color.DIM + continuePrompt + color.END)
        self.__init__()


class Fscan:
    logo = _make_tool_logo('Fscan - Internal Network Scanner', color.RED)

    def __init__(self, target=None):
        if check_windows('Fscan'): return
        self.installDir = toolDir + "fscan"
        self.gitRepo    = "https://github.com/shadow1ng/fscan.git"

        if not self.installed():
            spinner_run("Installing Fscan...", self.install)
        clearScr()
        print(self.logo)
        if target is None:
            target = input(color.CYAN + "  Enter Target IP/Range: " + color.END)
        self.run(target)
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))
        os.system("cd %s && go build -o fscan main.go" % self.installDir)

    def run(self, target):
        os.system("%s/fscan -h %s" % (self.installDir, target))


# ─────────────────────────────────────────────────────────────
#  POST EXPLOITATION MENU
# ─────────────────────────────────────────────────────────────

class postExploitationMenu:
    def __init__(self):
        clearScr()
        print_header('Post Exploitation')

        lines = [
            '  ' + color.OKGREEN + '[01]' + color.END + '  🔍  ' + color.WHITE + 'Shell Checker - Verify shell access' + color.END,
            '  ' + color.OKGREEN + '[02]' + color.END + '  🎭  ' + color.WHITE + 'POET         - Post Exploitation Tool' + color.END,
            '  ' + color.OKGREEN + '[03]' + color.END + '  🎣  ' + color.WHITE + 'Weeman       - Phishing Framework' + color.END,
            '',
            '  ' + color.RED    + '[99]' + color.END + '  🔙  ' + color.WHITE + 'Back to Main Menu' + color.END,
        ]
        print(box(lines, width=56, title=' POST EXPLOITATION ', color_code=color.WARNING))
        print()

        choice = input(prompt('post'))
        clearScr()

        if choice in ('1', '01'):
            sitechecker()
        elif choice in ('2', '02'):
            poet()
        elif choice in ('3', '03'):
            weeman()
        elif choice == "99":
            fsociety()
        else:
            self.__init__()
        self.completed()

    def completed(self):
        input(color.DIM + continuePrompt + color.END)
        self.__init__()


class sitechecker:
    logo = _make_tool_logo('Shell Checker - Verify Shell Access', color.OKGREEN)

    def __init__(self):
        if check_windows('Shell Checker'): return
        self.installDir = toolDir + "sitechecker"
        self.gitRepo    = "https://github.com/Manisso/sitechecker.git"

        if not self.installed():
            spinner_run("Installing Shell Checker...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        target = input(color.CYAN + "  Enter Shell URL: " + color.END)
        os.system("python3 %s/sitechecker.py %s" % (self.installDir, target))


class poet:
    logo = _make_tool_logo('POET - Post Exploitation Tool', color.WARNING)

    def __init__(self):
        if check_windows('POET'): return
        self.installDir = toolDir + "poet"
        self.gitRepo    = "https://github.com/mossberg/poet.git"

        if not self.installed():
            spinner_run("Installing POET...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        os.system("python3 %s/poet.py --help" % self.installDir)


class weeman:
    logo = _make_tool_logo('Weeman - HTTP Server for Phishing', color.RED)

    def __init__(self):
        if check_windows('Weeman'): return
        self.installDir = toolDir + "weeman"
        self.gitRepo    = "https://github.com/evait-security/weeman.git"

        if not self.installed():
            spinner_run("Installing Weeman...", self.install)
        clearScr()
        print(self.logo)
        self.run()
        input(continuePrompt)

    def installed(self):
        return os.path.isdir(self.installDir)

    def install(self):
        os.system("git clone --depth=1 %s %s" % (self.gitRepo, self.installDir))

    def run(self):
        os.system("python3 %s/weeman.py" % self.installDir)


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='fsociety - Penetration Testing Framework',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='fsociety 2.0 (Python 3)'
    )
    args = parser.parse_args()

    try:
        boot_sequence()
        agreement()
        fsociety()
    except KeyboardInterrupt:
        print(color.OKGREEN + '\n\n  Interrupted. Goodbye.\n' + color.END)
        sys.exit(0)


if __name__ == '__main__':
    main()

