import tkinter
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import math

# TODO 2 Add opacity controller
# TODO 3 Add save function
# TODO 4 Add help / instructions
# TODO 5 Add scrollbar when image is large
# TODO 6 Add controller for number of repeaing words in row and grid and spacing between words

# Opens a starting Image
im = Image.open("Images/greenpython.jpg").convert("RGBA")
custom_text=""
text_size_options = 10
main_bg_color = "#A2FAC4"
main_window_bg_color = "#507A60"

# Opens the image to watermark
def select_image():
    global im, coordinate_x, coordinate_y
    filetypes = (
        ('All files', '*.*'),
        ('Jpeg files', '*.jpeg'),
        ('Bitmap files', '*.bmp')
    )

    filename = fd.askopenfilename(
        title='Open an Image',
        initialdir='/',
        filetypes=filetypes
    )

    im = Image.open(filename).convert("RGBA")
    current_img = ImageTk.PhotoImage(image=im)
    canvas.itemconfig(image_canvas, image=current_img, anchor="center")
    canvas.image = current_img
    canvas.config(height=im.size[0], width=im.size[1])
    canvas.moveto(image_canvas, x=0, y=0)
    canvas.configure(yscrollcommand=h_scrollbar.set)
    canvas.configure(xscrollcommand=v_scrollbar.set)
    picture_frame.pack_propagate(False)
    coordinate_x = im.size[0]/2
    coordinate_y = im.size[1]/2

# Saves the image
def save_image():
    filetypes = (
        ('Jpeg files', '*.jpeg'),
        ('Jpg files', '*.jpg')
    )
    filename = fd.asksaveasfilename(
        title='Save image',
        initialdir='Images',
        filetypes=filetypes
    )
    filename = filename + ".jpg"
    new_im = ImageTk.getimage(canvas.image)
    new_im = new_im.convert("RGB")
    new_im = new_im.save(filename)

# Adds or updates the watermark with the set properties
def add_watermark():
    global im, coordinate_x, coordinate_y
    custom_text = watermark_text.get()
    if mode_clicked.get() == "Row":
        custom_text = custom_text + (" " * spaceingrow_scale.get())
        custom_text = custom_text * rowmultiples_scale.get()
    elif mode_clicked.get() == "Grid":
        custom_text = custom_text + (" " * spaceingrow_scale.get())
        custom_text = custom_text * rowmultiples_scale.get()
        custom_text = custom_text + ("\n" * spaceingcolumn_scale.get())
        custom_text = custom_text * columnmultiples_scale.get()



    text_watermark_image = Image.new("RGBA", im.size, (255, 255, 255, 0))
    font = ImageFont.truetype(font_dict[font_clicked.get()], textsize_scale.get())
    d = ImageDraw.Draw(text_watermark_image)
    d.text((int(coordinate_x), int(coordinate_y)), custom_text, fill=(0, 0, 0, opacity_scale.get()), font=font, anchor='mm')
    rotated_image = text_watermark_image.rotate(rotation_scale.get())
    combined_image = Image.alpha_composite(im, rotated_image)
    starting_img = ImageTk.PhotoImage(image=combined_image)
    canvas.itemconfig(image_canvas, image=starting_img, anchor="center")
    canvas.image = starting_img

# Moves the watermark to desired place on image
def move(event):
    global coordinate_x, coordinate_y, im

    coordinate_x, coordinate_y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    custom_text = watermark_text.get()

    if mode_clicked.get() == "Row":
        custom_text = custom_text + (" " * spaceingrow_scale.get())
        custom_text = custom_text * rowmultiples_scale.get()
    elif mode_clicked.get() == "Grid":
        custom_text = custom_text + (" " * spaceingrow_scale.get())
        custom_text = custom_text * rowmultiples_scale.get()
        custom_text = custom_text + ("\n" * spaceingcolumn_scale.get())
        custom_text = custom_text * columnmultiples_scale.get()

    text_watermark_image = Image.new("RGBA", im.size, (255, 255, 255, 0))
    font = ImageFont.truetype(font_dict[font_clicked.get()], textsize_scale.get())
    d = ImageDraw.Draw(text_watermark_image)
    d.text((coordinate_x, coordinate_y), custom_text, fill=(0, 0, 0, opacity_scale.get()), font=font, anchor='mm')
    rotated_image = text_watermark_image.rotate(rotation_scale.get())
    combined_image = Image.alpha_composite(im, rotated_image)
    starting_img = ImageTk.PhotoImage(image=combined_image)
    canvas.itemconfig(image_canvas, image=starting_img)
    canvas.image = starting_img


# Rotates the watermark text
def rotate(degrees):
    global im, coordinate_x, coordinate_y

    custom_text = watermark_text.get()
    if mode_clicked.get() == "Row":
        custom_text = custom_text + (" " * spaceingrow_scale.get())
        custom_text = custom_text * rowmultiples_scale.get()
    elif mode_clicked.get() == "Grid":
        custom_text = custom_text + (" " * spaceingrow_scale.get())
        custom_text = custom_text * rowmultiples_scale.get()
        custom_text = custom_text + ("\n" * spaceingcolumn_scale.get())
        custom_text = custom_text * columnmultiples_scale.get()

    text_watermark_image = Image.new("RGBA", im.size, (255, 255, 255, 0))
    font = ImageFont.truetype(font_dict[font_clicked.get()], textsize_scale.get())
    d = ImageDraw.Draw(text_watermark_image)
    d.text((int(coordinate_x), int(coordinate_y)), custom_text, fill=(0, 0, 0, opacity_scale.get()), font=font, anchor='mm')

    rotated_image = text_watermark_image.rotate(rotation_scale.get())

    combined_image = Image.alpha_composite(im, rotated_image)
    starting_img = ImageTk.PhotoImage(image=combined_image)
    canvas.itemconfig(image_canvas, image=starting_img)
    canvas.image = starting_img

# Expands grid or row to cover the whole image
def confirm_watermark():
    global im, coordinate_x, coordinate_y

    if rotation_scale.get() > 10:
        # Sets watermark image to cover original image regardless of rotation ( when centered)
        if im.size[0] > im.size[1]:
           watermarking_size = (int(im.size[0]*2), int(im.size[0]*2))
        else:
           watermarking_size = (int(im.size[1]*2), int(im.size[1]*2))

        custom_text = watermark_text.get()
        if mode_clicked.get() == "Row":
            custom_text = custom_text + (" " * spaceingrow_scale.get())
            custom_text = custom_text * 100
        elif mode_clicked.get() == "Grid":
            custom_text = custom_text + (" " * spaceingrow_scale.get())
            custom_text = custom_text * 100
            custom_text = custom_text + ("\n" * spaceingcolumn_scale.get())
            custom_text = custom_text * 100
        width = int(im.size[0]*2)
        height = int(im.size[1]*2)
        text_watermark_image = Image.new("RGBA", watermarking_size, (255, 255, 255, 0))
        font = ImageFont.truetype(font_dict[font_clicked.get()], textsize_scale.get())
        d = ImageDraw.Draw(text_watermark_image)
        d.text((int(coordinate_x), int(coordinate_y)), custom_text, fill=(0, 0, 0, opacity_scale.get()), font=font,
               anchor='mm')
        rotated_image = text_watermark_image.rotate(rotation_scale.get())
        sub_image =  rotated_image.crop(box=(30, 30, watermarking_size[0] - 30, watermarking_size[1] -30))
        text_watermark_image = Image.new("RGBA", im.size, (255, 255, 255, 0))
        text_watermark_image.paste(sub_image, (-int(watermarking_size[0]*0.3), -int(watermarking_size[0]*0.3)))
        rotated_image = text_watermark_image
        combined_image = Image.alpha_composite(im, rotated_image)
        starting_img = ImageTk.PhotoImage(image=combined_image)
        canvas.itemconfig(image_canvas, image=starting_img, anchor="center")
        canvas.image = starting_img



window = tkinter.Tk()
window.configure(background="#FFFFFF")
window.title("Watermarker")
window.minsize(height=800, width=800)
window.grid_rowconfigure(0, minsize=2)
window.grid_columnconfigure(0, minsize=2)

# Frame that contains the canvas and picture to be watermarked
picture_frame = tkinter.Frame(window, height=500, width=500, padx=10, pady=0, highlightbackground="#79BA92", highlightthickness=2)
picture_frame.grid(row=0, column=0, rowspan=3, columnspan=2, sticky="nw")
picture_frame.configure(background=main_bg_color)
picture_frame.pack_propagate(False)

# Frame that contains the different options for the watermark
control_frame = tkinter.Frame(window, height=600, width=300, pady=20, highlightbackground="#79BA92", highlightthickness=2, borderwidth=2 )
control_frame.grid(row=0, column=3, rowspan=4, sticky="nw")
control_frame.configure(background=main_bg_color)
control_frame.grid_propagate(False)

# Info text on moveing and coordinates
coordinate_x = im.size[0]/2
coordinate_y = im.size[1]/2
placementinfo_label = tkinter.Label(window, text="Click and drag on Image for position \n Please note rotation will cause offset in movement", font=("Helvetica", text_size_options), background="#FFFFFF")
placementinfo_label.grid(row=3, column=1, sticky="w")

# Initialize image
text_watermark_image = Image.new("RGBA", im.size, (255, 255, 255, 0))
font = ImageFont.truetype("ELEPHNT.TTF", 24)
d = ImageDraw.Draw(text_watermark_image)
combined_image = Image.alpha_composite(im, text_watermark_image)
starting_img = ImageTk.PhotoImage(image=combined_image)
canvas = tkinter.Canvas(picture_frame,  width=im.size[0], height=im.size[1])
image_canvas = canvas.create_image(139, 94, image=starting_img, anchor="center")
canvas.pack()

# Adding scrolling
h_scrollbar = tkinter.ttk.Scrollbar(window, orient='vertical', command=canvas.yview)
h_scrollbar.grid(row=0, column=2, rowspan=3, pady=10, padx=2, sticky="ns")
canvas.configure(yscrollcommand=h_scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

v_scrollbar = tkinter.ttk.Scrollbar(window, orient='horizontal', command=canvas.xview)
v_scrollbar.grid(row=3, column=0, columnspan=3, padx=30, pady=2, sticky="NWE")
canvas.configure(xscrollcommand=v_scrollbar.set)
canvas.bind('<Configure>', lambda  e: canvas.configure(scrollregion=canvas.bbox("all")))

# Info text under picture
info_text = tkinter.Label(control_frame, justify=tkinter.LEFT, text="Enter watermark text, choose font, rotation,\n"
                              " size and opacity. Click apply to preview.\n"
                              " You can move the watermark by drag and\n drop on the image.", background=main_bg_color)
info_text.grid(row=0, column=0, columnspan=2, pady=10, padx=20)

# Field to enter watermark text
watermarkentry_label = tkinter.Label(control_frame, text=" Watermark text: ", font=("Helvetica", text_size_options), background=main_bg_color)
watermarkentry_label.grid(row=1, column=0)
text = tkinter.StringVar()
watermark_text = tkinter.Entry(control_frame, textvariable=text)
watermark_text.grid(row=1, column=1, pady=10, sticky="w")

# Button to add/update watermark on image
okay_btn = tkinter.Button(control_frame, text="Apply/Update Watermark", command=add_watermark, background="white", highlightbackground="white")
okay_btn.grid(row=11, column=1, pady=10, sticky="w")

# Button to expand grid or row to cover whole image even if watermark is rotated
confirm_button = tkinter.Button(control_frame, text="Expand Grid", command=confirm_watermark, background="white", highlightbackground="white")
confirm_button.grid(row=12, column=1, pady=5, sticky="w")

# Moving watermark text
canvas.bind("<B1-Motion>", move)


# OPTIONS FRAME, includes, FONT, MODE of WATERMARK ( SINGLE, ROW, GRID), ORIENTATION (ROTATION)

# Font, dropdown
font_label = tkinter.Label(control_frame, text="Font: ", font=("Helvetica", text_size_options), background=main_bg_color)
font_label.grid(row=2, column=0, sticky="e")

font_dict = {
    'HARLOWSI': 'Fonts/HARLOWSI.TTF',
    'ELEPHNT': 'Fonts/ELEPHNT.TTF',
    'Arial': 'Fonts/arial.TTF',
    'STENCIL': 'Fonts/STENCIL.TTF'
             }
font_options = ['HARLOWSI', 'ELEPHNT', 'Arial', 'STENCIL']
font_clicked = tkinter.StringVar()
font_clicked.set('ELEPHNT')
font_dropdown = tkinter.OptionMenu(control_frame, font_clicked, *font_options)
font_dropdown.configure(background="white", highlightbackground=main_bg_color, activebackground="white")
font_dropdown.grid(row=2, column=1, sticky="w")


# MODE of Watermark
mode_label = tkinter.Label(control_frame, text="Mode: ", font=("Helvetica", text_size_options), background=main_bg_color)
mode_label.grid(row=3, column=0, sticky="e")
mode_dict = {
    'Single': 1,
    'Row': 10,
    'Grid': 20,
}
mode_options = ['Single', 'Row', 'Grid']
mode_clicked = tkinter.StringVar()
mode_clicked.set('Single')
mode_dropdown = tkinter.OptionMenu( control_frame, mode_clicked, *mode_options)
mode_dropdown.configure(background="white", highlightbackground=main_bg_color, activebackground="white")
mode_dropdown.grid(row=3, column=1, sticky="w")


# Number of repeated words in row
rowmultiples_label = tkinter.Label(control_frame, text="Words in row: ", font=("Helvetica", text_size_options), background=main_bg_color)
rowmultiples_label.grid(row=4, column=0, sticky="e")
rowmultiples_scale = tkinter.Scale(control_frame, from_=1, to=30, orient="horizontal", background=main_bg_color, highlightbackground=main_bg_color, activebackground="white")
rowmultiples_scale.grid(row=4, column=1, sticky="w")


# Number of rows column
columnmultiples_label = tkinter.Label(control_frame, text="Rows in column: ", font=("Helvetica", text_size_options), background=main_bg_color)
columnmultiples_label.grid(row=5, column=0, sticky="e")
columnmultiples_scale = tkinter.Scale(control_frame, from_=1, to=30, orient="horizontal", background=main_bg_color, highlightbackground=main_bg_color, activebackground="white")
columnmultiples_scale.grid(row=5, column=1, sticky="w")


# Spacing between words in rows
spaceingrow_label = tkinter.Label(control_frame, text="Space between words: ", font=("Helvetica", text_size_options), background=main_bg_color)
spaceingrow_label.grid(row=6, column=0, sticky="e")
spaceingrow_scale = tkinter.Scale(control_frame, from_=1, to=100, orient="horizontal", background=main_bg_color, highlightbackground=main_bg_color, activebackground="white")
spaceingrow_scale.grid(row=6, column=1, sticky="w")


# Spacing between rows in column
spaceingcolumn_label = tkinter.Label(control_frame, text="Space between rows: ", font=("Helvetica", text_size_options), background=main_bg_color)
spaceingcolumn_label.grid(row=7, column=0, sticky="e")
spaceingcolumn_scale = tkinter.Scale(control_frame, from_=1, to=100, orient="horizontal", background=main_bg_color, highlightbackground=main_bg_color, activebackground="white")
spaceingcolumn_scale.grid(row=7, column=1, sticky="w")


#Orientation of watermark ( Rotation )
rotation_label = tkinter.Label(control_frame, text="Rotation: ", font=("Helvetica", text_size_options), background=main_bg_color)
rotation_label.grid(row=8, column=0, sticky="e")
rotation_scale = tkinter.Scale(control_frame, from_=0, to=359, orient="horizontal", command=rotate, background=main_bg_color, highlightbackground=main_bg_color, activebackground="white")
rotation_scale.grid(row=8, column=1, sticky="w")


# Text size
textsize_label = tkinter.Label(control_frame, text="Size: ", font=("Helvetica", text_size_options), background=main_bg_color)
textsize_label.grid(row=9, column=0, sticky="e")
textsize_scale = tkinter.Scale(control_frame, from_=10, to=52, orient="horizontal", background=main_bg_color, highlightbackground=main_bg_color, activebackground="white")
textsize_scale.set(24)
textsize_scale.grid(row=9, column=1, sticky="w")


# Text opacity
opacity_label = tkinter.Label(control_frame, text="Opacity: ", font=("Helvetica", text_size_options), background=main_bg_color)
opacity_label.grid(row=10, column=0,sticky="e")
opacity_scale = tkinter.Scale(control_frame, from_=10, to=255, orient="horizontal", background=main_bg_color, highlightbackground=main_bg_color, activebackground="white")
opacity_scale.set(80)
opacity_scale.grid(row=10, column=1, sticky="w")


#MENU
menubar = tkinter.Menu(window)
window.config(menu=menubar)
file_menu = tkinter.Menu(menubar, tearoff=False)

file_menu.add_command(label='Open', command=select_image)
file_menu.add_command(label='Save as', command=save_image)
file_menu.add_command(
    label='Exit',
    command=window.destroy,
)

menubar.add_cascade(
    label='File',
    menu=file_menu,
    underline=0
)


window.mainloop()

