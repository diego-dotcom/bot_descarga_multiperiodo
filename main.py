import tkinter as tk
import webbrowser
import os
import subprocess
import bot
from tkinter import Label, Button, IntVar, Checkbutton, messagebox
from tkinter.ttk import Separator


def link_clicked():
    webbrowser.open_new_tab("https://cafecito.app/diego-dotcom")


def abrir_archivo_xlsx(archivo):
    try:
        excel_file_path = f"./{archivo}.xlsx"
        if os.path.exists(excel_file_path):
            subprocess.Popen(['start', 'excel', excel_file_path], shell=True)
        else:
            messagebox.showerror("Error", "El archivo no existe.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir el archivo: {e}")


def create_window():

    root = tk.Tk()
    root.title("Bot descarga desde Mis Comprobantes")
    root.geometry("640x300")
    root.iconbitmap("icono.ico")

    # Variables globales para los formatos
    excel_var = IntVar(value=0)  # Por defecto, Excel marcado
    csv_var = IntVar(value=1)    # Por defecto, CSV desmarcado

    # Frame principal
    frame_main = tk.Frame(root)
    frame_main.pack(pady=5)

    Label(frame_main, text="No olvide modificar y guardar el archivo 'contribuyentes.xlsx' según su preferencia").pack(
        fill='x', pady=5)

    Label(frame_main, text="Tiene a su disposicion el archivo 'Leeme.txt' en la carpeta del programa").pack(
        fill='x', pady=5)

    # Frame de formatos de descarga
    frame_formatos = tk.Frame(root)
    frame_formatos.pack(pady=5)

    Label(frame_formatos, text="Seleccione los formatos de descarga:").pack()
    Checkbutton(frame_formatos, text="Excel (.xlsx)",
                variable=excel_var).pack()
    Checkbutton(frame_formatos, text="CSV (.csv)", variable=csv_var).pack()

    # Botón principal
    Button(frame_main, text="Iniciar bot", command=lambda: bot.descarga(
        excel_var.get(), csv_var.get())).pack(pady=10)

    Button(frame_main, text="Ver archivo contribuyentes",
           command=lambda: abrir_archivo_xlsx("contribuyentes")).pack(pady=10)

    # Separación

    separator = Separator(root, orient='horizontal')
    separator.pack(fill='x', pady=5)

    # Frame de colaboración
    frame_colaborar = tk.Frame(root)
    frame_colaborar.pack(pady=5)
    Label(frame_colaborar, text="Si te simplificó el trabajo, colaborá con el proyecto!").pack(
        side=tk.LEFT)
    btn_colaborar = Button(
        frame_colaborar, text="Cafecito", command=link_clicked)
    btn_colaborar.pack(side=tk.RIGHT, padx=5)
    Label(root, text="https://twitter.com/diegom3ndizabal").pack(side=tk.BOTTOM, pady=5)
    '''

    root.mainloop()


if __name__ == "__main__":
    create_window()
