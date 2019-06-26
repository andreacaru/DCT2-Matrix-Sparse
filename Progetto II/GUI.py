#Andrea Carubelli: 803192
#Alessio Abondio: 808752

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk 
import numpy as np
from scipy.fftpack import fft, dct, idct
import sys


#####################################
#####################################
#####################################
#####################################
#####################################
#####################################


def file_selection():
    print("User is selecting a picture..")
    # Function that allow the user to select an arbitrary file from the computer
    root.filename =  filedialog.askopenfilename(initialdir = "/Users/andreacarubelli/Desktop/UNIVERSITA\'/Magistrale/Metodi\ del\ Calcolo\ scientifico/Progetto\ II/ImmaginiProgettoIIMCS",title = "Select file",filetypes = (("bmp files","*.bmp"), ("jpeg files","*.jpg")))
    # Converting the selected file to Image format.
    original_pic = Image.open(root.filename)
    original_pic.save('img/1.bmp')
    original_pic = Image.open("img/1.bmp")
    w, h = original_pic.size
    d = int(parameter_1.get())
    F = int(parameter_2.get())
    size = min(w,h)

    #FARE CROP
    #TAGLIO IMMAGINE IN MODO QUADRATO IN BASE ALLA MISURA MINORE
    resto = size % F
    if(resto!=0 and w>h):
        cropped = original_pic.crop((0 , 0, h-resto, h-resto))
        cropped.save('img/cropped.bmp')
    elif(resto!=0 and h>w):
        cropped = original_pic.crop((0 , 0, w-resto, w-resto))
        cropped.save('img/cropped.bmp')
    elif(resto==0 and w>h):
        #immagine rettangolare lato lungo w
        cropped = original_pic.crop((0,0,h,h))
        cropped.save('img/cropped.bmp')
    else:
        taglio = h-w
        cropped = original_pic.crop((0,0,w,w))
        cropped.save('img/cropped.bmp') 
    original_photo = cropped.resize((450, 450))
    original_photo = ImageTk.PhotoImage(original_photo)
    original_img.config(image=original_photo)
    original_img.image = original_photo

    print("Picture has been selected and uploaded!\n")

def append_images(images, direction='horizontal',
                  bg_color=(255,255,255), aligment='center'):
    """
    Appends images in horizontal/vertical direction.

    Args:
        images: List of PIL images
        direction: direction of concatenation, 'horizontal' or 'vertical'
        bg_color: Background color (default: white)
        aligment: alignment mode if images need padding;
           'left', 'right', 'top', 'bottom', or 'center'

    Returns:
        Concatenated image as a new PIL image object.
    """
    widths, heights = zip(*(i.size for i in images))

    if direction=='horizontal':
        new_width = sum(widths)
        new_height = max(heights)
    else:
        new_width = max(widths)
        new_height = sum(heights)

    new_im = Image.new('RGB', (new_width, new_height), color=bg_color)


    offset = 0
    for im in images:
        if direction=='horizontal':
            y = 0
            if aligment == 'center':
                y = int((new_height - im.size[1])/2)
            elif aligment == 'bottom':
                y = new_height - im.size[1]
            new_im.paste(im, (offset, y))
            offset += im.size[0]
        else:
            x = 0
            if aligment == 'center':
                x = int((new_width - im.size[0])/2)
            elif aligment == 'right':
                x = new_width - im.size[0]
            new_im.paste(im, (x, offset))
            offset += im.size[1]

    return new_im

def convert():
    original_pic = Image.open("img/1.bmp")
    w, h = original_pic.size
    d = int(parameter_1.get())
    F = int(parameter_2.get())
    size = min(w,h)

    #FARE CROP
    #TAGLIO IMMAGINE IN MODO QUADRATO IN BASE ALLA MISURA MINORE
    resto = size % F
    if(resto!=0 and w>h):
        cropped = original_pic.crop((0 , 0, h-resto, h-resto))
        cropped.save('img/cropped.bmp')
    elif(resto!=0 and h>w):
        cropped = original_pic.crop((0 , 0, w-resto, w-resto))
        cropped.save('img/cropped.bmp')
    elif(resto==0 and w>h):
        #immagine rettangolare lato lungo w
        cropped = original_pic.crop((0,0,h,h))
        cropped.save('img/cropped.bmp')
    else:
        taglio = h-w
        cropped = original_pic.crop((0,0,w,w))
        cropped.save('img/cropped.bmp')
    
    #CREO BLOCCHI FXF
    k=0 #contatore per nome immagine
    w, h = cropped.size
    n = w / F
    n = int(n)
    for y in range (0, n):
        for x in range (0, n):
            immagineCroppata = cropped.crop((x*F,y*F,(x*F)+F,(y*F)+F))
            immagineCroppata.save("img/cropped" + str(k) + ".bmp")
            k += 1

    N = n*n
    for k in range (0, N):
        original_pic = Image.open("img/cropped" + str(k) + ".bmp")
        w1, h1 = original_pic.size
        pix_val = list(original_pic.getdata())
        data = np.array(pix_val)
        shape = (h1, w1)
        skatarata = data.reshape(shape)

        #DCT
        dct1 = dct(skatarata, norm='ortho')
        dct2 = dct(dct1.T, norm='ortho')
        dct2 = dct2.T

        #TAGLIO FREQUENZE D
        for i in range(0, h1):
            for j in range(0, w1):
                if ((i + j >= d)):
                    dct2[i][j] = 0

        #IDCT (DCT INVERSA)
        idct1 = idct(dct2, norm='ortho')
        idct2 = idct(idct1.T, norm='ortho')
        idct2 = idct2.T

        #frequenze <0 assegno 0 frequenza >255 assegno 255
        for i in range(0, h1):
            for j in range(0, w1):
                if ((idct2[i][j] < 0)):
                    idct2[i][j] = 0
                if (idct2[i][j] > 255):
                    idct2[i][j] = 255
                else: round(idct2[i][j])

        #converto in tipo idoneo uint8
        numbers_matrix = np.array(idct2.astype(np.uint8))
        img = Image.fromarray(numbers_matrix)
        img.save('img/SKATARAPUMPUM' + str(k) + '.bmp')


    #CREO NUOVA IMMAGINE
    images = []

    for k in range(0, N):
        images.append(Image.open('img/SKATARAPUMPUM' + str(k) + '.bmp'))
    k=0
    for t in range(0, N, n):
        img1 = append_images(images[t:t+n], direction='horizontal')
        img1.save("img/PUMPUM"+str(k)+".bmp")
        k += 1

    images = []
    for k in range(0, n):
        images.append(Image.open('img/PUMPUM' + str(k) + '.bmp'))

    final = append_images(images, direction='vertical')
    final.save("img/FINAL.bmp")
    
    img_elab = final.resize((450, 450))
    img_elab = ImageTk.PhotoImage(img_elab)
    elab_img.config(image=img_elab)
    elab_img.image = img_elab

#####################################
#####################################
#####################################
#####################################
#####################################


print("Building the GUI interface..")
root = tk.Tk()
root.title("GUI Interface - Frequencies Manipulation")

original_pic = Image.open("no_img.png", 'r')
original_pic = original_pic.resize((450, 450), Image.ANTIALIAS)
original_photo = ImageTk.PhotoImage(original_pic)

# Set the elaborted image label and initialize it to "no_img"
elab_pic = Image.open("no_img.png", 'r')
elab_pic = elab_pic.resize((450, 450), Image.ANTIALIAS)
elab_photo = ImageTk.PhotoImage(elab_pic)

var1_descr = " d: " ; label_descr1 = tk.Label(root, text=var1_descr)
parameter_1 = tk.Entry(root)

var2_descr = " F: "
label_descr2 = tk.Label(root, text=var2_descr)
parameter_2 = tk.Entry(root)

# Images viewer
orig_img_descr = " Original image" ; label_orig_img_descr = tk.Label(root, text=orig_img_descr)
elab_img_descr = " Elaborated image " ; label_elab_img_descr = tk.Label(root, text=elab_img_descr)

original_img = tk.Label(root, image = original_photo)
elab_img = tk.Label(root, image=elab_photo)

# Create the buttons
filename_selection = tk.Button(root, text = "Select input image", command = file_selection)
convert = tk.Button(root, text = "Convert", command = convert)

# Grid is used to add the widgets to root
# Alternatives are Pack and Place
label_descr1.grid(row = 0, column = 1)
parameter_1.grid(row = 1, column = 1)

label_descr2.grid(row = 2, column = 1)
parameter_2.grid(row =3, column = 1)
filename_selection.grid(row = 4, column = 1)
label_orig_img_descr.grid(row = 5, column = 0)
label_elab_img_descr.grid(row = 5, column = 2)
original_img.grid(row = 6, column = 0)
convert.grid(row = 6, column = 1)
elab_img.grid(row = 6, column = 2)

print("GUI Interface is ready!\n")

#LAST OPERATION
root.mainloop() 