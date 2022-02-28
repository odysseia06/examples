import tkinter as tk


# Creates a button that increase the count by 1 when clicked.


root = tk.Tk()
root.title("Deneme")

intval = tk.IntVar()
count = 0
intval.set(count)

def Button():
    global count
    count += 1
    intval.set(count)

Button = tk.Button(root, text="Deneme Button", command=Button)
keyEnter = tk.Entry(root, textvariable= intval, width=8)

Button.grid(row=2, column=0, sticky=tk.E)
keyEnter.grid(row=3, column=1, sticky=tk.W)

tk.mainloop()