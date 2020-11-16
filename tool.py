import os, sys, socket, docker, re, argparse
import threading, subprocess
import tkinter as tk
from tkinter import font
from tkinter import *
from PIL import Image, ImageTk

parser = argparse.ArgumentParser(prog='program',
                                    usage='%(prog)s [options]', 
                                    description="Master Tool of Hacking",
                                    epilog='Enjoy the program!')

parser.add_argument('-u',
                       '--url',
                       action='store',
                       help='url of the site')
                       
parser.add_argument('-g',
                       '--gui',
                       action='store_true',
                       help="open the program in GUI")
                       
parser.add_argument('-c',
                       '--cmd',
                       action='store',
                       help="run kali linux command")                        

parser.add_argument('-r',
                       '--recon',
                       action='store_true',
                       help="reconnaissance of the target")

parser.add_argument('-v',
                       '--vulnerability',
                       action='store_true',
                       help="enumeration of the target")

parser.add_argument('-f',
                       '--full',
                       action='store_true',
                       help="reconnaissance and enumeration of the target")                        

parser.add_argument('-t',
                       '--terminal',
                       action='store_true',
                       help="open a new kali linux terminal")
                       
parser.add_argument('-p',
                       '--prune',
                       action='store_true',
                       help="stop running containers")

                                            
if len(sys.argv)==1:
    parser.print_help()
    parser.exit()
    
args = parser.parse_args()
client = docker.from_env()
root = None
entry = None
lower_text = None
history = []
history_index = -1

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
text='''
 __  __           _         _______          _        __ _    _            _    _             
|  \/  |         | |       |__   __|        | |      / _| |  | |          | |  (_)            
| \  / | __ _ ___| |_ ___ _ __| | ___   ___ | | ___ | |_| |__| | __ _  ___| | ___ _ __   __ _ 
| |\/| |/ _` / __| __/ _ \ '__| |/ _ \ / _ \| |/ _ \|  _|  __  |/ _` |/ __| |/ / | '_ \ / _` |
| |  | | (_| \__ \ ||  __/ |  | | (_) | (_) | | (_) | | | |  | | (_| | (__|   <| | | | | (_| |
|_|  |_|\__,_|___/\__\___|_|  |_|\___/ \___/|_|\___/|_| |_|  |_|\__,_|\___|_|\_\_|_| |_|\__, |
                                                                                         __/ |
                                                                                        |___/

URL        recon and enumeration of the target
command    execute linux command / kali linux tools
kali       open a new kali linux terminal
prune      stop running containers
clear      clear the textbox
exit       close the GUI
                                                                                      
'''

def cycleHistoryUp(event):
    global history_index
    if history_index == 0:
        history_index -=1
    if len(history):
        try:
            comm = history[history_index]
            history_index -= 1
        except IndexError:
            history_index= -1 
            comm = ""       
        entry.delete(0,tk.END)
        entry.insert(0,comm)
               
def cycleHistoryDown(event):
    global history_index
    if history_index == -1:
        history_index +=1
    if len(history):
        try:
            comm = history[history_index]
            history_index += 1             
        except IndexError:
            history_index = 0
            comm = ""      
        entry.delete(0,tk.END)    
        entry.insert(0,comm)
                  
def runCommand(cmd):
    history.append(cmd)
    global history_index
    history_index = -1
    entry.delete(0,tk.END)
    container = client.containers.run('kali',auto_remove=True, detach=True, stdin_open = True, tty= True)
    response=container.exec_run(cmd, stream=True).output
    for line in response:
        if line.decode("utf-8").startswith("OCI runtime exec failed"):
            lower_text.delete('1.0',END)
            lower_text.insert(tk.END, "Not a valid command.")
            break
        else:
            lower_text.insert(tk.END, line.decode("utf-8"))
    container.stop()

def runInlineCommand(cmd):
    container = client.containers.run('kali',auto_remove=True, detach=True, stdin_open = True, tty= True)
    response=container.exec_run(cmd, stream=True).output
    for line in response:
        if line.decode("utf-8").startswith("OCI runtime exec failed"):
            print("Not a valid command.")
            break
        else:
            print(line.decode("utf-8"))
    container.stop()
    
def clearLocalhost(url):
    protocol = url[:url.find(':')+3]
    host = url[url.find(':')+3:].split('/')[0]
    ip=socket.gethostbyname(socket.gethostname())
    resource =url[url.find(':')+3+len(host):]
    newurl=protocol+ip+resource
    return newurl
    
def checkSite(event):
    url= entry.get().strip()
    try:
        if re.match(regex, url):
            if "localhost" in url:
                newurl=clearLocalhost(url)
                finalRecon(newurl)
                golismero(newurl) 
            else:
                finalRecon(url)
                golismero(url)
        elif url =="kali":
            entry.delete(0,tk.END)
            getTerminal()
        elif url =="exit":
            root.destroy() 
        elif url=="clear":
            entry.delete(0,tk.END)
            lower_text.delete('1.0',END)
            lower_text.insert(tk.END, text)
        elif url=="prune":
            [i.stop() for i in client.containers.list(all=True)]
            entry.delete(0,tk.END)
            out="All runing containers successfully stoped!"
            lower_text.delete('1.0',END)
            lower_text.insert(tk.END, out)
        else:
            if url != "":
                lower_text.delete('1.0',END)
                th = threading.Thread(target=runCommand, args=(url,))
                th.daemon=True
                th.start()
            else:
                lower_text.delete('1.0',END)
                lower_text.insert(tk.END, "You need to insert a command.")
    except:
        [i.stop() for i in client.containers.list(all=True) if i.name == "kali" or i.name == "golismero" or i.name == "finalrecon"]
 
def Gui():
    #Graphical Interface
    global root
    root = tk.Tk()
    root.title("Master Tool of Hacking") 
    canvas = tk.Canvas(root, height=700, width=1030)
    canvas.pack()
    image = Image.open("images/bytes.jpeg")
    background_image = ImageTk.PhotoImage(image)
    background_label = tk.Label(root, image = background_image)
    background_label.place(relwidth=1, relheight=1) 
    frame= tk.Frame(root, bg="black", bd=5)
    frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')
    global entry
    entry = tk.Entry(frame, bd =10, font=40, fg="green", bg="black", insertbackground='green')
    entry.bind("<Return>",checkSite)
    entry.bind("<Up>",cycleHistoryUp)
    entry.bind("<Down>",cycleHistoryDown)
    entry.focus()
    entry.place(relwidth=0.65, relheight=1)
    if args.url:
        if "localhost" in args.url:
            args.url=clearLocalhost(args.url)
        entry.insert(0,args.url)
    button=tk.Button(frame, bd=10,text="Check",fg="green", bg="black",activebackground="black", command=lambda:checkSite(""))
    button['font'] = tk.font.Font(weight='bold')
    button.place(relx=0.7, relheight=1, relwidth=0.3)
    global lower_text
    lower_text=tk.Text(root, bg="black",fg="green", bd=10)
    lower_text.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')
    lower_text.insert(tk.END, text) 
    root.mainloop()
    
def getTerminal():
    container = client.containers.run('kali',auto_remove=True,tty= True, detach=True,stdin_open = True, hostname="kali", volumes={r''+os.getcwd()+'\output': {'bind': '/root', 'mode': 'rw'}})
    p = subprocess.Popen(["powershell.exe","docker attach "+container.id],creationflags=subprocess.CREATE_NEW_CONSOLE)
    
def golismero(cmd):
    container = client.containers.run('kali',auto_remove=True,tty= True, detach=True,stdin_open = True, name="golismero", hostname="kali" , volumes={r''+os.getcwd()+'\output': {'bind': '/root', 'mode': 'rw'}}) 
    p = subprocess.Popen(["powershell.exe","docker exec golismero golismero scan "+cmd+" -o "+cmd[cmd.find(':')+3:].split('/')[0]+"_Vulnerabilities.txt -o "+cmd[cmd.find(':')+3:].split('/')[0]+"_Vulnerabilities.html;docker attach golismero"],creationflags=subprocess.CREATE_NEW_CONSOLE)
    
def finalRecon(cmd): 
    container = client.containers.run('kali',auto_remove=True,tty= True, detach=True,stdin_open = True, name="finalrecon", hostname="kali", volumes={r''+os.getcwd()+'\output': {'bind': '/usr/share/finalrecon/dumps', 'mode': 'rw'}}) 
    p = subprocess.Popen(["powershell.exe","docker exec finalrecon finalrecon "+cmd+" --full;docker attach finalrecon"],creationflags=subprocess.CREATE_NEW_CONSOLE)
    
def main():
    if args.prune:
        [i.stop() for i in client.containers.list(all=True)]
        out="All runing containers successfully stoped!"
        print(out)
    if args.terminal:
        getTerminal()
    if args.cmd:
        runInlineCommand(args.cmd)
    if args.url:
        if re.match(regex, args.url):
            if "localhost" in args.url:
               args.url=clearLocalhost(args.url)
            if args.full:
               finalRecon(args.url) 
               golismero(args.url)
            else:   
                if args.recon:
                    finalRecon(args.url)
                elif args.vulnerability:
                    golismero(args.url)
                else:    
                    print("Insert other options!")        
        else:
            print("URL invalid!")                     
    if args.gui:
        Gui()
       
if __name__=="__main__":
    main() 