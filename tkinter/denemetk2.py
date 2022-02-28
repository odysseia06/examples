import tkinter as tk
import threading



forward = ["Forward", "forward"]
back = ["Back", "back"]
left = ["Left", "left"]
right = ["Right", "right"]

btn_list = [forward, back, left, right]
BTN_NAME = 0
BTN_CMD = 1

class runButtonThread(threading.Thread):
    def __init__(self, btn_cmd):
        threading.Thread.__init__(self)
        self.cmd = btn_cmd
    def run(self):
        try:
            print("Button thread started")
        except:
            pass
        finally:
            print("Button thread finished")


class Buttons:
    def __init__(self, gui, btn_index, x, y):
        #Add buttons to window with coordinates
        btn = tk.Button(gui, text= btn_list[btn_index][BTN_NAME], width=30, command=self.buttonFunction)
        btn.place(x=x, y=y)
        self.btn_cmd = btn_list[btn_index][BTN_CMD]
        self.btn_name = btn_list[btn_index][BTN_NAME]
    def buttonFunction(self):
        print("%s button is pressed." %self.btn_name)
        runButtonThread(self.btn_cmd).start()




window = tk.Tk()
window.title("Client")
window.geometry("800x600")

x = 10
y = 10
for index, button in enumerate(btn_list):
    Buttons(window, index, x, y)
    y += 30
    









window.mainloop()