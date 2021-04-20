from tkinter import *
from PIL import ImageTk, Image
from setup import setup
from canvas import canvas
from virtual_pen import pen
from virtual_keyboard import keyboard

def create_button(text = "", x = 0, y = 0, command = None):
	btn = Button(root, text = text, command = command)
	btn.place(y = y, x = x, width = 100)
	return btn

if __name__ == '__main__':
    root = Tk()
    root.title("Image Processing Project")
    root.geometry("506x550")
    root.iconbitmap('./icon/favicon.ico')
    background_img = ImageTk.PhotoImage(Image.open('./icon/cvc-logo_3.png'))
    background_lbl = Label(root, image = background_img)
    background_lbl.place(x = 0, y = 0)
    setup_btn = create_button("Setup", 203, 140, setup)
    pen_btn = create_button("Show Pen", 203, 180, pen)
    canvas_btn = create_button("Show Canvas", 203, 355, canvas)
    keyboard_btn = create_button("Show Keyboard", 203, 395, keyboard)
    # close_btn = create_button("Close", 203, 290, root.destroy)

    root.mainloop()