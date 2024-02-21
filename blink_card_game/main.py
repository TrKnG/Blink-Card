import tkinter as tk
from PIL import ImageTk, Image
import json
import socket
from threading import Thread
from tkinter import messagebox

def kontrol():
    global card1_state, card2_state, card3_state, card4_state
    if card1_state == "back" or card2_state == "back":
        if card3_state == "back" or card4_state == "back":
            if card1_state == "front" and card3_state == "front":
                card1_label.config(image=cardback_img)
                card3_label.config(image=cardback_img)
                card1_state = "back"
                card3_state = "back"
            elif card1_state == "front" and card4_state == "front":
                card1_label.config(image=cardback_img)
                card4_label.config(image=cardback_img)
                card1_state = "back"
                card4_state = "back"
    if card3_state == "back" or card4_state == "back":
        if card1_state == "back" or card2_state == "back":
            if card2_state == "front" and card3_state == "front":
                card2_label.config(image=cardback_img)
                card3_label.config(image=cardback_img)
                card2_state = "back"
                card3_state = "back"
            elif card2_state == "front" and card4_state == "front":
                card2_label.config(image=cardback_img)
                card4_label.config(image=cardback_img)
                card2_state = "back"
                card4_state = "back"

def check_blink_strength():
    host = "127.0.0.1"
    port = 13854
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.send(b'{"enableRawOutput": false, "format": "Json"}\n')
    data_buffer = ""
    selected_card = 5
    global card1_state, card2_state, card3_state, card4_state
    card1_state = "back"
    card2_state = "back"
    card3_state = "back"
    card4_state = "back"
    while True:
        data = sock.recv(1024).decode("utf-8")
        data_buffer += data
        while "\r" in data_buffer:
            json_str, data_buffer = data_buffer.split("\r", 1)
            json_data = json.loads(json_str)
            if "blinkStrength" in json_data:
                blink_strength = json_data["blinkStrength"]
                strength_label.config(text="Göz Kırpma Gücü: {}".format(blink_strength))
                if card1_state == "front" and card2_state == "front" and card3_state == "front" and card4_state == "front" :
                    messagebox.showinfo("Tebrikler","Bütün kartları açtınız")
                    root.destroy()
                kontrol()
                if blink_strength > 50:
                    print(selected_card)
                    if selected_card == 0:
                        if card1_state == "back":
                            card1_label.config(image=card1_img)
                            card1_state = "front"
                        elif card1_state == "front" :
                            result_label.config(text="Kart açık!")
                    elif selected_card == 1:
                        if card2_state == "back":
                            card2_label.config(image=card1_img)
                            card2_state = "front"
                        elif card2_state == "front":
                            result_label.config(text="Kart açık!")
                    elif selected_card == 2:
                        if card3_state == "back":
                            card3_label.config(image=card2_img)
                            card3_state = "front"
                        elif card3_state == "front":
                            result_label.config(text="Kart açık!")
                    elif selected_card == 3:
                        if card4_state == "back":
                            card4_label.config(image=card2_img)
                            card4_state = "front"
                        elif card4_state == "front":
                            result_label.config(text="Kart açık!")
                else:
                    if selected_card == 0:
                        if card2_state == "back" and card1_state == "back":
                            card1_label.config(image=cardback_img)
                            card2_label.config(image=cardselect_img)
                            selected_card = 1
                        elif card2_state == "front" and card1_state == "front":
                            selected_card = 1
                        elif card2_state == "front" and card1_state == "back":
                            card1_label.config(image=cardback_img)
                            selected_card = 1
                        elif card2_state == "back" and card1_state == "front":
                            card2_label.config(image=cardselect_img)
                            selected_card = 1
                    elif selected_card == 1:
                        if card3_state == "back" and card2_state == "back":
                            card2_label.config(image=cardback_img)
                            card3_label.config(image=cardselect_img)
                            selected_card = 2
                        elif card3_state == "front" and card2_state == "front":
                            selected_card = 2
                        elif card3_state == "front" and card2_state == "back":
                            card2_label.config(image=cardback_img)
                            selected_card = 2
                        elif card3_state == "back" and card2_state == "front":
                            card3_label.config(image=cardselect_img)
                            selected_card = 2
                    elif selected_card == 2:
                        if card4_state == "back" and card3_state == "back":
                            card3_label.config(image=cardback_img)
                            card4_label.config(image=cardselect_img)
                            selected_card = 3
                        elif card4_state == "front" and card3_state == "front":
                            selected_card = 3
                        elif card4_state == "front" and card3_state == "back":
                            card3_label.config(image=cardback_img)
                            selected_card = 3
                        elif card4_state == "back" and card3_state == "front":
                            card4_label.config(image=cardselect_img)
                            selected_card = 3
                    elif selected_card == 3:
                        if card1_state == "back" and card4_state == "back":
                            card4_label.config(image=cardback_img)
                            card1_label.config(image=cardselect_img)
                            selected_card = 0
                        elif card1_state == "front" and card4_state == "front":
                            selected_card = 0
                        elif card1_state == "front" and card4_state == "back":
                            card4_label.config(image=cardback_img)
                            selected_card = 0
                        elif card1_state == "back" and card4_state == "front":
                            card1_label.config(image=cardselect_img)
                            selected_card = 0
                    elif selected_card == 5:
                        card1_label.config(image=cardselect_img)
                        selected_card = 0
                    print(selected_card)

# Ana pencere oluştur
root = tk.Tk()
root.title("Blink Card Game")
root.config(bg="#f0f0f0")  # Arka plan rengi

# Göz kırpma gücü metni için etiket oluştur
strength_label = tk.Label(root, text="Göz Kırpma Gücü: ", font=("Arial", 12))
strength_label.pack()

# Kartlar için görüntüler yükle
cardback_img = ImageTk.PhotoImage(Image.open("arka.png"))
cardselect_img = ImageTk.PhotoImage(Image.open("ön.png"))
card1_img = ImageTk.PhotoImage(Image.open("kupa.png"))
card2_img = ImageTk.PhotoImage(Image.open("maça.png"))

# Kartları içeren çerçeve oluştur
card_frame = tk.Frame(root, bg="#f0f0f0")
card_frame.pack(pady=10)

# Kart etiketlerini oluştur ve çerçeve içine yerleştir
card1_label = tk.Label(card_frame, image=cardback_img, borderwidth=2, relief="solid")
card1_label.pack(side="left", padx=5)
card2_label = tk.Label(card_frame, image=cardback_img, borderwidth=2, relief="solid")
card2_label.pack(side="left", padx=5)
card4_label = tk.Label(card_frame, image=cardback_img, borderwidth=2, relief="solid")
card4_label.pack(side="right", padx=5)
card3_label = tk.Label(card_frame, image=cardback_img, borderwidth=2, relief="solid")
card3_label.pack(side="right", padx=5)

# Sonuç metni için etiket oluştur
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

# Göz kırpma gücünü kontrol etmek için bir thread başlat
Thread(target=check_blink_strength).start()

# Ana döngüyü başlat
root.mainloop()
