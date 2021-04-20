from tkinter import *
from setup import setup
from canvas import canvas
from virtual_pen import pen
from virtual_keyboard import keyboard

def create_button(text = "", y = 0, x = 0, command = None):
	btn = Button(root, text = text, command = command)
	btn.place(y = y, x = x, width = 100)
	return btn

if __name__ == '__main__':
    root = Tk()
    root.title("Image Processing Project")
    root.geometry("1005x705")
    setup_btn = create_button("Setup", 60, 20, setup)
    canvas_btn = create_button("Show Canvas", 60, 300, canvas)
    pen_btn = create_button("Show Pen", 60, 120, pen)
    keyboard_btn = create_button("Show Keyboard", 60, 400, keyboard)
    close_btn = create_button("Close", 120, 290, root.destroy)

    root.mainloop()