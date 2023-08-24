# DorkBuster
# By: Euronymou5
# VERSION BETA

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import configparser
import re
from tkinter import messagebox
import requests
import sys
import time
from bs4 import BeautifulSoup
from tkinter.scrolledtext import ScrolledText
from googlesearch import search        
import random

args_variable = ""
config = configparser.ConfigParser()

global IsActive_custom_checkbutton

def nose():
    valor = guardar_txt_variable.get()
    config.read('config.ini')
    config.set('Settings', 'guardar_txt', str(valor))
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def spinbox_changed():
    valor = spinbox_variable.get()
    config.read('config.ini')
    config.set('Settings', 'resultados', str(valor))
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def change_combo(event):
    valor = modulos_variable.get()
    config.read('config.ini')
    config.set('Settings', 'modulos_busqueda', str(valor))
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
        
def cooldow_changed():
    valor = cooldown_variable.get()
    config.read('config.ini')
    config.set('Settings', 'cooldown', str(valor))
    with open('config.ini', 'w') as config_file:
        config.write(config_file)


def custom_args_func():
    valor = IsActive_custom_checkbutton.get()
    try:
        IsActive_defaultargs_checkbutton.set(False)
    except:
        pass
    if valor == True:
        config.read('config.ini')
        config.set('Settings', 'custom_args', str(valor))
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
       # custom_args = tk.StringVar()
    else:
        config.read('config.ini')
        config.set('Settings', 'custom_args', 'False')
        with open('config.ini', 'w') as config_file:
            config.write(config_file)

def args_default_func():
    valor = IsActive_defaultargs_checkbutton.get()
    try:
        IsActive_custom_checkbutton.set(False)
        entry_custom_args.destroy()
    except:
        pass    
    if valor == True:
        config.read('config.ini')
        config.set('Settings', 'custom_args', 'False')
        with open('config.ini', 'w') as config_file:
            config.write(config_file)

def args_menu():
    # Definiendo variables globales:
    global IsActive_custom_checkbutton
    global IsActive_defaultargs_checkbutton
    global args_level

    # Estructura de la ventana de configuracion de argumentos y programacion de las funciones:
    args_level = tk.Toplevel(ventana)
    args_level.configure(background="#3f3f3f", height=136, width=284)
    args_level.resizable(width=False, height=False)
    args_level.title("Argumentos")
    
    busqueda_label = tk.Label(args_level)
    busqueda_label.configure(background="#3f3f3f",font="{Arial} 9 {}",foreground="#ffffff",text='Utilizar argumentos por defecto:')
    busqueda_label.place(anchor="nw", relx=0.01, rely=0.06, x=0, y=0)
    
    custom_args_label = tk.Label(args_level)
    custom_args_label.configure(background="#3f3f3f",font="{Arial} 9 {}",foreground="#ffffff",text='Utilizar argumentos personalizados:')
    custom_args_label.place(anchor="nw", relx=0.01, rely=0.35, x=0, y=0)
    
    args_default_checkbutton = tk.Checkbutton(args_level)
    IsActive_defaultargs_checkbutton = tk.BooleanVar(value=False)
    args_default_checkbutton.configure(background="#3f3f3f",variable=IsActive_defaultargs_checkbutton)
    args_default_checkbutton.place(anchor="nw", relx=0.64, rely=0.06, x=0, y=0)
    args_default_checkbutton.configure(command=args_default_func)
    
    custom_args_checkbutton = tk.Checkbutton(args_level)
    IsActive_custom_checkbutton = tk.BooleanVar(value=False)
    custom_args_checkbutton.configure(background="#3f3f3f", variable=IsActive_custom_checkbutton)
    custom_args_checkbutton.place(anchor="nw", relx=0.74, rely=0.34, x=0, y=0)
    custom_args_checkbutton.configure(command=custom_args_func)
    # Deteccion automatica de valores de args_menu
    try:
        config.read('config.ini')
        valor = config.get('Settings', 'custom_args')
        if valor == 'False':
            IsActive_defaultargs_checkbutton.set(True)
        elif valor == 'True':
            IsActive_custom_checkbutton.set(True)
    except:
        messagebox.showerror("DorkBuster", "Imposible de poder leer el archivo de configuracion.")
        sys.exit(0)

def config_func():
    # Definiendo variables:
    global spinbox_variable
    global spinbox
    global cooldown_variable
    global guardar_txt_variable
    global modulos_variable
    
    
    # Estructura de la ventana de configuracion y programacion de las funciones:
    config_level = tk.Toplevel(ventana)
    config_level.resizable(width=False, height=False)
    config_level.title("Configuracion")    
    config_level.configure(background="#3f3f3f", height=176, width=384)
    
    resultados_label = ttk.Label(config_level)
    resultados_label.configure(background="#3f3f3f",font="{Arial} 10 {}",foreground="#f3f3f3",text='Resultados:')
    resultados_label.place(anchor="nw", relx=0.01, rely=0.14, x=0, y=0)
    
    spinbox = ttk.Spinbox(config_level, from_=1, to=100)
    spinbox_variable = tk.IntVar()
    spinbox.configure(justify="center",textvariable=spinbox_variable)
    spinbox.place(anchor="nw",relwidth=0.17,relx=0.22,rely=0.14,x=0,y=0)
    spinbox.config(command=spinbox_changed)
    spinbox_variable.trace("w", lambda name, index, mode, sv=spinbox_variable: spinbox_changed())
    
    cooldown_label = ttk.Label(config_level)
    cooldown_label.configure(background="#3f3f3f",font="{Arial} 10 {}",foreground="#f3f3f3",text='Cooldown:')
    cooldown_label.place(anchor="nw", relx=0.01, rely=0.37, x=0, y=0)
    
    cooldown_variable = tk.IntVar()
    cooldown_spinbox = ttk.Spinbox(config_level, from_=0, to=100)
    cooldown_spinbox.configure(justify="center", textvariable=cooldown_variable)
    cooldown_spinbox.place(anchor="nw",relwidth=0.17,relx=0.22,rely=0.37,x=0,y=0)
    cooldown_spinbox.config(command=cooldow_changed)
    cooldown_variable.trace("w", lambda name, index, mode, sv=cooldown_variable: cooldow_changed())
    
    guardar_en_txt_label = ttk.Label(config_level)
    guardar_en_txt_label.configure(background="#3f3f3f",font="{Arial} 8 {}",foreground="#f3f3f3",text='Guardar resultados en un .txt')
    guardar_en_txt_label.place(anchor="nw", relx=0.01, rely=0.57, x=0, y=0)
    
    guardar_txt_checkbutton = tk.Checkbutton(config_level)
    guardar_txt_variable = tk.BooleanVar(value=False)
    guardar_txt_checkbutton.configure(background="#3f3f3f", variable=guardar_txt_variable)
    guardar_txt_checkbutton.place(anchor="nw", relx=0.41, rely=0.55, x=0, y=0)
    guardar_txt_checkbutton.configure(command=nose)
    
    modulos_label = ttk.Label(config_level)
    modulos_label.configure(background="#3f3f3f",font="{Arial} 8 {}",foreground="#f3f3f3",text='Modulos de busqueda')
    modulos_label.place(anchor="nw", relx=0.01, rely=0.75, x=0, y=0)
    
    modulos_combobox = ttk.Combobox(config_level)
    modulos_variable = tk.StringVar()
    modulos_combobox.configure(justify="center", textvariable=modulos_variable)
    modulos_combobox.configure(values = ('Google-Python', 'Yahoo', 'Google-Python-Requests'))
    modulos_combobox.place(anchor="nw",relwidth=0.41,relx=0.32,rely=0.75)
    modulos_combobox.bind("<<ComboboxSelected>>", change_combo)
    # Deteccion de valores del archivo de configuracion:
    try:
        config.read('config.ini')
        valor = config.get('Settings', 'resultados')
        cool_valor = config.get('Settings', 'cooldown')
        guardar_valor = config.getboolean('Settings', 'guardar_txt')
        combo_valor = config.get('Settings', 'modulos_busqueda')
        spinbox_variable.set(valor)
        cooldown_variable.set(cool_valor)
        guardar_txt_variable.set(guardar_valor)
        modulos_combobox.set(combo_valor)
    except:
        messagebox.showerror("DorkBuster", "Imposible de poder leer el archivo de configuracion.")
        sys.exit(0)

def search_func():
    config.read('config.ini')
    resultados_text.delete('1.0', tk.END)
    busqueda = search_var.get()
    cooldown = config.get('Settings', 'cooldown')
    txt_save = config.getboolean('Settings', 'guardar_txt')
    modulos = config.get('Settings', 'modulos_busqueda')
    resultados = config.get('Settings', 'resultados')
    args = config.get('Settings', 'custom_args')
    # Programacion de la busqueda:
    if modulos == "Google-Python": # Utilizacion del modulo "Google Search"
        if args == "True":
            result_list = []
            dom = ["com","com.tw","co.in","be","de","co.uk","co.ma","dz","ru","ca"]
            
            tld = random.choice(dom)

            messagebox.showinfo('DorkBuster', f'Busqueda comenzada de {busqueda}.')
            
            results = search(busqueda, tld,num=int(resultados), stop=int(resultados), pause=int(cooldown))
            for result in results:
                result_list.append(result)
                resultados_text.insert(tk.END, f'{result}\n')
                
            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in result_list:
                        file.write("%s\n" % item)
            else:
                pass                
            messagebox.showinfo('DorkBuster', 'Busqueda finalizada.')
        elif args == "False":
            # Seleccion de dominios de manera random:
            dom = ["com","com.tw","co.in","be","de","co.uk","co.ma","dz","ru","ca"]
            tld = random.choice(dom)
            result_list = []
            # Argumentos por defecto:
            arg = f"allintext:{busqueda} site:@"
            arg_a = f"allinurl:{busqueda} site:@"
            arg_b = f"intext:{busqueda} site:@ filetype:pdf"
            arg_c = f"intext:{busqueda} site:@ filetype:venv"
            arg_d = f"intitle:{busqueda}"
            arg_e = f"intext:{busqueda} filetype:pcf"
            arg_f = f"intext:{busqueda}"
            arg_g = f"inurl:{busqueda}"
            #--------------------------
            messagebox.showinfo('DorkBuster', f'Busqueda comenzada de {busqueda}.')
            #---------------------------
            results = search(arg, tld,num=int(resultados), stop=int(resultados), pause=int(cooldown))
            for result in results:
                result_list.append(result)
                resultados_text.insert(tk.END, f'{result}\n')
            # Busqueda arg_a
            results_a = search(arg_a, tld,num=int(resultados), stop=int(resultados), pause=int(cooldown))
            for result1 in results_a:
                result_list.append(result1)
                resultados_text.insert(tk.END, f'{result1}\n')
            # Busqueda arg_b
            results_m = search(arg_b, tld,num=int(resultados), stop=int(resultados), pause=int(cooldown))
            for result2 in results_m:
                result_list.append(result2)
                resultados_text.insert(tk.END, f'{result2}\n')
            # Busqueda arg_c
            results_c = search(arg_c, tld,num=int(resultados), stop=int(resultados), pause=int(cooldown))
            for result3 in results_c:
                result_list.append(result3)
                resultados_text.insert(tk.END, f'{result3}\n')
            # Busqueda arg_d
            results_d = search(arg_d, tld,num=int(resultados), stop=int(resultados), pause=int(cooldown))
            for result4 in results_d:
                result_list.append(result4)
                resultados_text.insert(tk.END, f'{result4}\n')
            # Busqueda arg_e
            results_e = search(arg_e, tld,num=int(resultados), stop=int(resultados), pause=int(cooldown))
            for result5 in results_e:
                result_list.append(result5)
                resultados_text.insert(tk.END, f'{result5}\n')
            # Busqueda arg_f
            results_f = search(arg_f, tld,num=int(resultados), stop=int(resultados), pause=int(cooldown))
            for result6 in results_f:
                result_list.append(result6)
                resultados_text.insert(tk.END, f'{result6}\n')
            # Busqueda arg_g
            results_g = search(arg_g, tld,num=int(resultados), stop=int(resultados), pause=int(cooldown))
            for result7 in results_g:
                result_list.append(result7)
                resultados_text.insert(tk.END, f'{result7}\n')
            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in result_list:
                        file.write("%s\n" % item)
            else:
                pass                        
            messagebox.showinfo('DorkBuster', 'Busqueda finalizada.')
    elif modulos == "Google-Python-Requests":
        resultados = []
        config.read('config.ini')
        valor = config.get('Settings', 'custom_args')
        if valor == "False":
            # Version BETA  
            queries = [f"allintext:{busqueda} site:@",f"allinurl:{busqueda} site:@",f"intext:{busqueda} site:@ filetype:pdf",f"intext:{busqueda} site:@ filetype:venv",f"intitle:{busqueda}",f"intext:{busqueda} filetype:pcf",f"intext:{busqueda}",f"inurl:{busqueda}"]
            url = "https://www.google.com/search?"
            for varr in queries:
                params = {"q": varr}
                response = requests.get(url, params=params)
            if response.status_code == 200:
                for url in response.text.split('<a href="/url?q=')[1:]:
                    resultados_text.insert(tk.END, f"{url.split('&amp;sa=U&amp;')[0]}\n")
                    resultados.append(url.split('&amp;sa=U&amp;')[0])
                resultados_text.insert(tk.END, "\n")
            else:
                messagebox.showinfo('DorkBuster', 'Error al conectar con google')
                    
            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in resultados:
                        file.write("%s\n" % item)
            else:
                pass
            messagebox.showinfo('DorkBuster', 'Busqueda finalizada.')
        elif valor == "True":
            url = "https://www.google.com/search?"
            params = {"q": busqueda}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                for url in response.text.split('<a href="/url?q=')[1:]:
                   resultados_text.insert(tk.END, f"{url.split('&amp;sa=U&amp;')[0]}\n")
                   resultados.append(url.split('&amp;sa=U&amp;')[0])
                print("\n")
            else:
                messagebox.showinfo('DorkBuster', 'Error al conectar con google')
            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in resultados:
                        file.write("%s\n" % item)
            else:
                pass
            messagebox.showinfo('DorkBuster', 'Busqueda finalizada.')
    elif modulos == "Yahoo":
        resultados = []
        config.read('config.ini')
        valor = config.get('Settings', 'custom_args')
        limit = config.get('Settings', 'resultados')
        if valor == "False":
            messagebox.showinfo('DorkBuster', f'Busqueda comenzada de {busqueda}.')
            
            resultados = []
            queries = [f"allintext:{busqueda} site:@",f"allinurl:{busqueda} site:@",f"intext:{busqueda} site:@ filetype:pdf",f"intext:{busqueda} site:@ filetype:venv",f"intitle:{busqueda}",f"intext:{busqueda} filetype:pcf",f"intext:{busqueda}",f"inurl:{busqueda}"]
            
            for varr in queries:
                url = f"https://search.yahoo.com/search?q={varr}"
                response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("div", class_="compTitle options-toggle")
            
            for i, result in enumerate(results[:int(limit)]):
                resultados.append(result.find('a')['href'])
                resultados_text.insert(tk.END, f"{result.find('a')['href']}\n")
            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in resultados:
                        file.write("%s\n" % item)
            else:
                pass
            messagebox.showinfo('DorkBuster', 'Busqueda finalizada.')
        elif valor == "True":
            messagebox.showinfo('DorkBuster', f'Busqueda comenzada de {busqueda}.')
            
            resultados = []
            
            url = f"https://search.yahoo.com/search?q={busqueda}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("div", class_="compTitle options-toggle")
            
            for i, result in enumerate(results[:int(limit)]):
                resultados.append(result.find('a')['href'])
                resultados_text.insert(tk.END, f"{result.find('a')['href']}\n")
            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in resultados:
                        file.write("%s\n" % item)
            else:
                pass
            messagebox.showinfo('DorkBuster', 'Busqueda finalizada.')

# Menu principal:

ventana = tk.Tk()
ventana.title("DorkBuster")
ventana.resizable(width=False, height=False)
ventana.configure(background="#3f3f3f", height=406, width=672)

titulo_label = ttk.Label(ventana)
titulo_label.configure(background="#3f3f3f",font="{Arial} 24 {bold italic}",foreground="#ff0f15",text='DorkBuster')
titulo_label.place(anchor="nw", relx=0.36, rely=0.05, x=0, y=0)

design_label = ttk.Label(ventana)
design_label.configure(background="#ffffff")
design_label.place(anchor="nw",relheight=0.0,relwidth=1.0,relx=0.00,rely=0.16,x=0,y=0)

imagen = Image.open("icons/set.png")
imagen = imagen.resize((25, 25))
imagen = ImageTk.PhotoImage(imagen) 

imagen_args = Image.open("icons/lup.png")
imagen_args = imagen_args.resize((25, 25))
imagen_args = ImageTk.PhotoImage(imagen_args)

button1 = tk.Button(ventana, image=imagen)
button1.configure(background="#3f3f3f", relief="flat")
button1.place(anchor="nw", relx=0.95, rely=0.07, x=0, y=0)
button1.configure(command=config_func)

button_args = tk.Button(ventana, image=imagen_args)
button_args.configure(background="#3f3f3f", relief="flat")
button_args.place(anchor="nw", relx=0.01, rely=0.07, x=0, y=0)
button_args.configure(command=args_menu)

search_entry = ttk.Entry(ventana)
search_var = tk.StringVar()
search_entry.configure(font="{Calibri} 11 {bold}",justify="center",textvariable=search_var)
search_entry.place(anchor="nw",relheight=0.06,relwidth=0.41,relx=0.29,rely=0.19,x=0,y=0)

buscar_button = ttk.Button(ventana)
buscar_button.configure(text='Buscar')
buscar_button.place(anchor="nw",relheight=0.09,relwidth=0.3,relx=0.35,rely=0.32,x=0,y=0)
buscar_button.configure(command=search_func)

resultados_text = ScrolledText(ventana)
resultados_text.configure(background="#aaaaaa",font="{Calibri} 10 {}",foreground="#000000")
resultados_text.place(anchor="nw",relheight=0.36,relwidth=0.44,relx=0.30,rely=0.47,x=0,y=0)

if __name__ == "__main__":
    ventana.mainloop()
