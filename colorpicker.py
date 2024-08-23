import tkinter as tk
import pyautogui
import mss
from pynput import mouse

esperando_clique = False

def ativar_captura():
    global esperando_clique, listener
    esperando_clique = True
    label_status.config(text="Clique em qualquer lugar na tela para capturar a cor.")
    
    listener = mouse.Listener(on_click=on_click)
    listener.start()

def capturar_clique(x, y):
    global esperando_clique
    if esperando_clique:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            screenshot = sct.grab(monitor)
            pixel = screenshot.pixel(x, y)

        r, g, b = pixel[0], pixel[1], pixel[2]
        cor_pixel = (r, g, b)
        cor_hex = rgb_para_hex(r, g, b)
        label_cor.config(text=f"Cor: {cor_pixel}", bg=cor_hex)
        
        janela.configure(bg=cor_hex)

        label_status.config(text="Cor capturada! Clique no botão novamente para capturar outra cor.")
        esperando_clique = False
        listener.stop()

def on_click(x, y, button, pressed):
    if pressed and esperando_clique:
        capturar_clique(x, y)
        return False

def rgb_para_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

janela = tk.Tk()
janela.title("Capturar Cor do Pixel")
janela.geometry("300x150")

btn_capturar = tk.Button(janela, text="Clique aqui para capturar cor", command=ativar_captura)
btn_capturar.pack(pady=20)

label_cor = tk.Label(janela, text="Cor: ", font=("Arial", 12))
label_cor.pack(pady=10)

label_status = tk.Label(janela, text="Clique no botão para começar.", font=("Arial", 10))
label_status.pack(pady=10)

janela.mainloop()
