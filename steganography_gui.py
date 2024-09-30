import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import os

def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in next(imdata)[:3] +
                              next(imdata)[:3] +
                              next(imdata)[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode(image_path, data, output_path):
    image = Image.open(image_path, 'r')
    if (len(data) == 0):
        raise ValueError('Data is empty')
    newimg = image.copy()
    encode_enc(newimg, data)
    newimg.save(output_path)

def decode(image_path):
    image = Image.open(image_path, 'r')
    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in next(imgdata)[:3] +
                              next(imgdata)[:3] +
                              next(imgdata)[:3]]
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def select_image():
    file_path = filedialog.askopenfilename()
    entry_img_path.delete(0, tk.END)
    entry_img_path.insert(0, file_path)

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    entry_save_path.delete(0, tk.END)
    entry_save_path.insert(0, file_path)

def encode_data():
    image_path = entry_img_path.get()
    data = text_data.get("1.0", tk.END).strip()
    output_path = entry_save_path.get()
    
    if image_path and data and output_path:
        try:
            encode(image_path, data, output_path)
            messagebox.showinfo("Success", "Data encoded and image saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please provide all inputs.")

def decode_data():
    image_path = entry_img_path.get()
    if image_path:
        try:
            decoded_message = decode(image_path)
            text_data.delete("1.0", tk.END)
            text_data.insert(tk.END, decoded_message)
            messagebox.showinfo("Success", "Data decoded successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please provide the image path.")

# Setting up the GUI
root = tk.Tk()
root.title("Steganography - Encode/Decode")
root.geometry("500x400")

# Image path entry
label_img = tk.Label(root, text="Select Image:")
label_img.pack(pady=5)
entry_img_path = tk.Entry(root, width=50)
entry_img_path.pack(pady=5)
btn_select_img = tk.Button(root, text="Browse", command=select_image)
btn_select_img.pack(pady=5)

# Text data to encode
label_data = tk.Label(root, text="Enter Data to Encode:")
label_data.pack(pady=5)
text_data = tk.Text(root, height=4, width=50)
text_data.pack(pady=5)

# Save path entry
label_save = tk.Label(root, text="Save Encoded Image As:")
label_save.pack(pady=5)
entry_save_path = tk.Entry(root, width=50)
entry_save_path.pack(pady=5)
btn_save_img = tk.Button(root, text="Browse", command=save_image)
btn_save_img.pack(pady=5)

# Encode and Decode buttons
btn_encode = tk.Button(root, text="Encode", command=encode_data)
btn_encode.pack(pady=5)

btn_decode = tk.Button(root, text="Decode", command=decode_data)
btn_decode.pack(pady=5)

root.mainloop()
