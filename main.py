from tkinter import *
root = Tk()
root.title("BookBoxBook")

#window size
#win.geometry(‘400x100+0+0’)  

#can't resizable
#root.resizable(0, 0)
#lab = Label(root, text = "bookboxbook")
#lab.grid(row = 0, column = 0)
#data = Entry(root)
#data.grid(row = 0, column = 1)
def clickInsertBtn():
    
    
def clickGetBtn():
    
    
    
    
btnInsert = Button(root, text = "Insert", width = 15, command = clickInsertBtn)
btnInsert.grid(row = 0, column = 0)

btnGet = Button(root, text = "Get", width = 15, command = clickGetBtn)
btnGet.grid(row = 1, column = 0)


root.mainloop()