from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import cv2
import math
import numpy as np

def show_main_app():
    app.deiconify()  # Menampilkan aplikasi utama
    registration_screen.destroy()  # Menutup halaman registrasi

def register_user():
    # Mendapatkan nilai dari inputan pengguna
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()

    # Melakukan validasi
    if not name:
        showinfo(title="Error", message="Nama tidak boleh kosong.")
        return
    elif not email:
        showinfo(title="Error", message="email tidak boleh kosong.")
        return
    elif not password:
        showinfo(title="Error", message="password tidak boleh kosong.")
        return
    elif '@' not in email:
        showinfo(title="Error", message="Email harus mengandung karakter '@'.")
        return
    elif len(password) < 8:
        showinfo(title="Error", message="Password harus memiliki minimal 8 karakter.")
        return

    # Jika registrasi berhasil, panggil fungsi untuk menampilkan aplikasi utama
    show_main_app()
    showinfo(title="Information", message="User Registered Successfully!")

def on_click_exit():
    app.destroy()
    registration_screen.destroy()

def on_click_choose():
    global path
    global photo
    # Library tkinter membuka file menggunakan filedialog
    path = filedialog.askopenfilename()
    # Mencari sumber gambar
    load = Image.open(path)
    # Load gambar
    load.thumbnail(image_display_size, Image.LANCZOS)
    # Load gambar ke GUI
    np_load = np.asarray(load)
    np_load = Image.fromarray(np.uint8(np_load))
    render = ImageTk.PhotoImage(np_load)
    photo = Label(app, image=render)
    photo.image = render
    photo.place(x=20, y=50)

def on_click_clear():
    global path
    global photo
    # Clear path
    path = None
    # Clear photo
    if photo:
        photo.destroy()
    # Clear txt
    txt.delete("1.0","end")

def encrypt_data():
    global path
    
    data = txt.get(1.0, "end-1c")
    img = cv2.imread(path)
    data = [format(ord(i), '08b') for i in data] # Mengubah data menjadi biner (spasi dan enter dimasukkan)
    _, width ,_ = img.shape # Lebar dari image yang dimasukkan
    PixReq = len(data) * 3

    RowReq = PixReq/width
    RowReq = math.ceil(RowReq) # Baris yang dibutuhkan

    count=0
    charCount=0
    for i in range(RowReq + 1):
        while(count < width and charCount < len(data)):
            char = data[charCount]
            charCount += 1

            for index_k, k in enumerate(char):
                if((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (k == '0' and img[i][count][index_k % 3] %2 == 1)):
                    img[i][count][index_k % 3] -= 1
                if(index_k % 3 == 2):
                    count += 1
                if(index_k == 7):
                    if(charCount*3 < PixReq and img[i][count][2] % 2 == 1):
                        img[i][count][2] -= 1
                    if(charCount*3 >= PixReq and img[i][count][2] % 2 == 0):
                        img[i][count][2] -= 1
                    count += 1
        count = 0

    # Library tkinter membuka file menggunakan filedialog
    fileType = [("Image Files", "*.png *.jpg")]
    savePath = filedialog.asksaveasfilename(filetypes=fileType, defaultextension=fileType)
    # Menyimpan gambar dengan path yang sudah ditentukan
    cv2.imwrite(savePath, img)
    # Melakukan checking success
    success = cv2.imwrite(savePath, img)
    if success:
        showinfo(title="Information", message="Enkripsi Sukses!")
    else:
        showinfo(title="Information", message="Enkripsi Gagal!")

def decrypt_data():
    # Algoritma untuk mendekripsi data dari gambar
    img = cv2.imread(path)
    data = []
    stop = False
    # Setiap pixel memiliki 1 bit informasi, ditambahkan ke variabel data menggunakan looping for
    for index_i, i in enumerate(img):
        i.tolist()
        for index_j, j in enumerate(i):
            # Periksa apakah karakter EOF(End of File) tercapai
            # Jika ya maka berhenti, jika tidak maka lanjut
            if((index_j) % 3 == 2):
                # pixel 1
                data.append(bin(j[0])[-1])
                # pixel 2
                data.append(bin(j[1])[-1])
                # pixel 3
                if(bin(j[2])[-1] == '1'):
                    stop = True
                    break
            else:
                # pixel 1
                data.append(bin(j[0])[-1])
                # pixel 2
                data.append(bin(j[1])[-1])
                # pixel 3
                data.append(bin(j[2])[-1])
        if(stop):
            break
    # ASCII disimpan dalam variabel data
    message = [data[i*8:(i*8)+8] for i in range(int(len(data)/8))]

    # Gabungkan semua huruf untuk membentuk pesan
    decoded_message = ''
    for binary_char in message:
        binary_str = ''.join(binary_char)
        if binary_str:  # Check if the string is not empty
            decoded_message += chr(int(binary_str, 2))

    txt.insert(END, decoded_message) # Jika ingin menggunakan textbox
    # showinfo(title="Information", message=decoded_message) # Jika ingin menggunakan showinfo

app = Tk()
app.withdraw()  # Sembunyikan aplikasi utama

global path
global img
global photo
image_display_size = 300, 300

# Register App
registration_screen = Toplevel()
registration_screen.title("Registration")
registration_screen.geometry('400x250')
registration_screen.resizable(False, False)
registration_screen.configure(background='crimson')

# Register Frame
register_frame = Frame(registration_screen)
register_frame.pack(padx=10, pady=10, fill="x", expand=True)

# Komponen-komponene formulir registrasi
label_name = Label(register_frame, text="Name", font=("Times New Roman", 11))
label_name.pack(padx=10, fill="x", expand=True)

entry_name = Entry(register_frame, font=("Times New Roman", 11))
entry_name.pack(padx=10, fill="x", expand=True)

label_email = Label(register_frame, text="Email", font=("Times New Roman", 11))
label_email.pack(padx=10, fill="x", expand=True)

entry_email = Entry(register_frame, font=("Times New Roman", 11))
entry_email.pack(padx=10, fill="x", expand=True)

label_password = Label(register_frame, text="Password", font=("Times New Roman", 11))
label_password.pack(padx=10, fill="x", expand=True)

entry_password = Entry(register_frame, show="*", font=("Times New Roman", 11))  # Show asterisks for password
entry_password.pack(padx=10, fill="x", expand=True)

# Tombol registrasi
register_button = Button(register_frame, text="Register", bg='ivory3', fg='black', font=("Times New Roman", 11), command=register_user)
register_button.pack(padx=10, pady=5, fill="x", expand=True)

# Main App
app.title("Program Steganography")
app.geometry('600x400')
app.resizable(False, False)
app.configure(background='crimson')

# Canvas
myCanvas = Canvas(app, bg="lemonchiffon1", height=300, width=300)
myCanvas.pack(side=LEFT, padx=20, pady=50)

# Textbox
txt = Text(app, wrap=WORD, bg="lemonchiffon1", font=("Times New Roman", 12), width=30)
txt.place(x=340, y=50, height=200)

# Choose Image (Button)
on_click_button = Button(app, text="Choose Image", bg='ivory3', fg='black', font=("Times New Roman", 11), command=on_click_choose)
on_click_button.place(x=125, y=15)

# Clear Image (Button)
on_click_button = Button(app, text="Clear Image", bg='ivory3', fg='black', font=("Times New Roman", 11), command=on_click_clear)
on_click_button.place(x=133, y=360)

# Encrypt (Button)
encrypt_button = Button(app, text="Encrypt", bg='ivory3', fg='black', font=("Times New Roman", 11), command=encrypt_data)
encrypt_button.place(x=395, y=260)

# Decrypt (Button)
decrypt_button = Button(app, text="Decrypt", bg='ivory3', fg='black', font=("Times New Roman", 11), command=decrypt_data)
decrypt_button.place(x=480, y=260)

# Exit (Button)
exit_button = Button(app, text="Exit", bg='ivory3', fg='black', font=("Times New Roman", 11), command=on_click_exit)
exit_button.place(x=560, y=360)

# Main
app.mainloop()
