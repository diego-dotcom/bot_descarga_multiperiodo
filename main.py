import tkinter as tk
import webbrowser
import bot
from tkinter import Label, Button
from tkinter.ttk import Separator


def link_clicked():
    webbrowser.open_new_tab("https://cafecito.app/diego-dotcom")


def create_window():

    root = tk.Tk()
    root.title("Bot descarga desde Mis Comprobantes")
    root.geometry("640x200")
    root.iconbitmap("icono.ico")

    # Frame para agrupar los elementos principales
    frame_main = tk.Frame(root)
    frame_main.pack(pady=5)

    Label(frame_main, text="No olvide modificar y guardar el archivo 'contribuyentes.xlsx' según su preferencia").pack(
        fill='x', pady=5)

    Label(frame_main, text="Tiene a su disposicion el archivo 'Leeme.txt' en la carpeta donde instalo el bot").pack(
        fill='x', pady=5)

    # Botones para generar listado de facturas a CF
    Button(frame_main, text="Iniciar bot", command=bot.descarga).pack(pady=10)

    # Separación
    separator = Separator(root, orient='horizontal')
    separator.pack(fill='x', pady=5)

    # Frame para agrupar elementos de créditos
    frame_colaborar = tk.Frame(root)
    frame_colaborar.pack(pady=5)
    Label(frame_colaborar, text="Si te simplificó el trabajo, colaborá con el proyecto!").pack(
        side=tk.LEFT)
    btn_colaborar = Button(
        frame_colaborar, text="Cafecito", command=link_clicked)
    btn_colaborar.pack(side=tk.RIGHT, padx=5)
    Label(root, text="https://twitter.com/diegom3ndizabal").pack(side=tk.BOTTOM, pady=5)

    root.mainloop()


if __name__ == "__main__":
    create_window()
