import tkinter as tk
from subprocess import call
import threading
#The example in this recipe shows how we can define our own variations of Tkinter objects to generate custom controls and dynamically construct
#a menu with them. it also includes threads to allow other tasks to continue to function while a particular task is being executed.

# We create special class for the application buttons.

leafpad = ["Leafpad", "leafpad"]
scratch = ["Scratch", "scratch"]
pistore = ["Pi Store", "pistore"]

app_list = [leafpad, scratch, pistore]
APP_NAME = 0
APP_CMD = 1

class runApplicationThread(threading.Thread):
    def __init__(self,app_cmd):
        # We first call the __init__ function of the inherited class to ensure it is set up correctly.
        threading.Thread.__init__(self)
        self.cmd = app_cmd
    def run(self):
        #Run the command if valid
        try:
            call(self.cmd)
        except:
            print("Unable to run: %s" %self.cmd)

class appButtons:
    def __init__(self,gui,app_index):
        #Add buttons to window
        btn = tk.Button(gui, text=app_list[app_index][APP_NAME], width=30, command=self.startApp)
        btn.pack()
        self.app_cmd = app_list[app_index][APP_CMD]
    def startApp(self):
        # If we run the application command here directly, the Tkinter window will freeze until the application we have opened is closed again.
        # To avoid this, we can use the Python threading module, which allows us to perform multiple actions at the same time.
        print("APP_CMD:  %s" %self.app_cmd)
        runApplicationThread(self.app_cmd).start()

root = tk.Tk()
root.title("App Menu")
prompt = "    Select and application     "
label1 = tk.Label(root, text=prompt, width=len(prompt), bg="yellow")
label1.pack()
#Create menu buttons from app_list 
for index, app in enumerate(app_list):
    appButtons(root, index)
    print("index:" , index)
    print("app:", app)      
#Run the tk window
root.mainloop()
#End        