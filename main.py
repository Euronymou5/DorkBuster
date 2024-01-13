# DorkBuster
# By: Euronymou5
# VERSION v1.2

import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import configparser
from tkinter import messagebox
import requests
import sys
import threading
from bs4 import BeautifulSoup
from tkinter.scrolledtext import ScrolledText
from googlesearch import search        
import random
from duckduckgo_search import DDGS
import json

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
      #  entry_custom_args.destroy()
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
        sys.exit(1)

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
    modulos_combobox.configure(values = ('Google-Python', 'Yahoo', 'Google-Python-Requests', 'DuckDuckGo'))
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
        sys.exit(1)

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
            args = [
               f"allintext:{busqueda}",
               f"allinurl:{busqueda}",
               f"intext:{busqueda} filetype:pdf",
               f"intext:{busqueda} filetype:venv",
               f"intitle:{busqueda}",
               f"intext:{busqueda} filetype:pcf",
               f"intext:{busqueda}",
               f"inurl:{busqueda}",
               f"intitle:index.of {busqueda}",
               f"filetype:conf {busqueda}",
               f"intitle:{busqueda} filetype:doc OR filetype:pdf OR filetype:txt",
               f"intitle:{busqueda} filetype:sql",
               f"intitle:{busqueda} filetype:log",
               f"intitle:{busqueda} filetype:backup OR filetype:bkf OR filetype:sqlbak",
               f"intitle:{busqueda} filetype:err",
               f"intitle:{busqueda} filetype:htpasswd OR filetype:htaccess",
               f"intitle:{busqueda} filetype:config OR filetype:ini OR filetype:conf"
            ]

            # Mensaje de inicio
            messagebox.showinfo('DorkBuster', f'Busqueda comenzada de {busqueda}.')

            # Seleccionar aleatoriamente 'resultados' elementos de la lista args
            args_to_search = random.sample(args, min(len(args), int(resultados)))

            # Realizar búsquedas y mostrar resultados
            for arg in args_to_search:
               results = search(arg, tld, num=int(resultados), stop=int(resultados), pause=int(cooldown))
               for result in results:
                   result_list.append(result)
                   resultados_text.insert(tk.END, f'{result}\n')

            # --------------- Txt Save ------------
            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in result_list:
                        file.write("%s\n" % item)
            else:
                pass                        
            messagebox.showinfo('DorkBuster', 'Busqueda finalizada.')
    elif modulos == "Google-Python-Requests":
        result_list = []
        config.read('config.ini')
        valor = config.get('Settings', 'custom_args')
        if valor == "False":
            # Version BETA  
            queries = [
               f"allintext:{busqueda}",
               f"allinurl:{busqueda}",
               f"intext:{busqueda} filetype:pdf",
               f"intext:{busqueda} filetype:venv",
               f"intitle:{busqueda}",
               f"intext:{busqueda} filetype:pcf",
               f"intext:{busqueda}",
               f"inurl:{busqueda}",
               f"intitle:index.of {busqueda}",
               f"filetype:conf {busqueda}",
               f"intitle:{busqueda} filetype:doc OR filetype:pdf OR filetype:txt",
               f"intitle:{busqueda} filetype:sql",
               f"intitle:{busqueda} filetype:log",
               f"intitle:{busqueda} filetype:backup OR filetype:bkf OR filetype:sqlbak",
               f"intitle:{busqueda} filetype:err",
               f"intitle:{busqueda} filetype:htpasswd OR filetype:htaccess",
               f"intitle:{busqueda} filetype:config OR filetype:ini OR filetype:conf"
            ]

            # Mensaje de inicio
            messagebox.showinfo('DorkBuster', f'Busqueda comenzada de {busqueda}.')
        
            # Seleccionar aleatoriamente 'resultados' elementos de la lista queries
            queries_to_search = random.sample(queries, min(len(queries), int(resultados)))

            # Realizar búsquedas y mostrar resultados
            url = "https://www.google.com/search?"
            for query in queries_to_search:
               params = {"q": query}
               response = requests.get(url, params=params)
               
               if response.status_code == 200:
                  for url in response.text.split('<a href="/url?q=')[1:]:
                        resultados_text.insert(tk.END, f"{url.split('&amp;sa=U&amp;')[0]}\n")
                        result_list.append(url.split('&amp;sa=U&amp;')[0])
                  resultados_text.insert(tk.END, "\n")
               else:
                    messagebox.showinfo('DorkBuster', 'Error al conectar con Google')
            #--------- Txt save ---------------
            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in result_list:
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
                   result_list.append(url.split('&amp;sa=U&amp;')[0])
                print("\n")
            else:
                messagebox.showinfo('DorkBuster', 'Error al conectar con google')
            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in result_list:
                        file.write("%s\n" % item)
            else:
                pass
            messagebox.showinfo('DorkBuster', 'Busqueda finalizada.')
    # --------------  Yahoo ------------
    elif modulos == "Yahoo":
        resultados = []
        config.read('config.ini')
        valor = config.get('Settings', 'custom_args')
        limit = config.get('Settings', 'resultados')
        if valor == "False":
            messagebox.showinfo('DorkBuster', f'Busqueda comenzada de {busqueda}.')
            
            resultados = []
          #  queries = [f"allintext:{busqueda}",f"allinurl:{busqueda}",f"intext:{busqueda} filetype:pdf",f"intext:{busqueda} filetype:venv",f"intitle:{busqueda}",f"intext:{busqueda} filetype:pcf",f"intext:{busqueda}",f"inurl:{busqueda}"] 
            queries = [
               f"allintext:{busqueda}",
               f"allinurl:{busqueda}",
               f"intext:{busqueda} filetype:pdf",
               f"intext:{busqueda} filetype:venv",
               f"intitle:{busqueda}",
               f"intext:{busqueda} filetype:pcf",
               f"intext:{busqueda}",
               f"inurl:{busqueda}",
               f"intitle:index.of {busqueda}",
               f"filetype:conf {busqueda}",
               f"intitle:{busqueda} filetype:doc OR filetype:pdf OR filetype:txt",
               f"intitle:{busqueda} filetype:sql",
               f"intitle:{busqueda} filetype:log",
               f"intitle:{busqueda} filetype:backup OR filetype:bkf OR filetype:sqlbak",
               f"intitle:{busqueda} filetype:err",
               f"intitle:{busqueda} filetype:htpasswd OR filetype:htaccess",
               f"intitle:{busqueda} filetype:config OR filetype:ini OR filetype:conf"
            ]

            # Seleccionar aleatoriamente 'limit' elementos de la lista queries
            queries_to_search = random.sample(queries, min(len(queries), int(limit)))

            # Comenzar busqueda
            for query in queries_to_search:
                url = f"https://search.yahoo.com/search?q={query}"
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                results = soup.find_all("div", class_="compTitle options-toggle")

            for i, result in enumerate(results[:int(limit)]):
                url_result = result.find('a')['href']
                resultados.append(url_result)
                resultados_text.insert(tk.END, f"{url_result}\n")

            # ------ Txt Save --------------
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

    # ------ Duckduckgo ------- #
    elif modulos == "DuckDuckGo":
        resultados = []
        config.read('config.ini')
        valor = config.get('Settings', 'custom_args')
        limit = config.get('Settings', 'resultados')

        if valor == "True":
            messagebox.showinfo('DorkBuster', f'Busqueda comenzada de {busqueda}.')

            with DDGS() as ddgs:
                bsq = [r for r in ddgs.text(busqueda, max_results=int(limit))]
                datos = json.loads(json.dumps(bsq))
                for item in datos:
                    href = item['href']
                    resultados.append(href)

                    resultados_text.insert(tk.END, f"{href}\n")

            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in resultados:
                        file.write("%s\n" % item)
            else:
                pass
            messagebox.showinfo('DorkBuster', 'Busqueda finalizada.')
                
        else: # No custom args--
            messagebox.showinfo('DorkBuster', f'Busqueda comenzada de {busqueda}.')

            queries = [
                f"allintext:{busqueda}",
                f"allinurl:{busqueda}",
                f"intext:{busqueda} filetype:pdf",
                f"intext:{busqueda} filetype:venv",
                f"intitle:{busqueda}",
                f"intext:{busqueda} filetype:pcf",
                f"intext:{busqueda}",
                f"inurl:{busqueda}",
                f"intitle:index.of {busqueda}",
                f"filetype:conf {busqueda}",
                f"intitle:{busqueda} filetype:doc OR filetype:pdf OR filetype:txt",
                f"intitle:{busqueda} filetype:sql",
                f"intitle:{busqueda} filetype:log",
                f"intitle:{busqueda} filetype:backup OR filetype:bkf OR filetype:sqlbak",
                f"intitle:{busqueda} filetype:err",
                f"intitle:{busqueda} filetype:htpasswd OR filetype:htaccess",
                f"intitle:{busqueda} filetype:config OR filetype:ini OR filetype:conf"
            ]

            queries_to_search = random.sample(queries, min(len(queries), int(limit)))

            with DDGS() as ddgs:
               for query in queries_to_search:
                    bsq = [r for r in ddgs.text(query, max_results=int(limit))]
                    datos = json.loads(json.dumps(bsq))
            
                    for item in datos:
                       href = item['href']
                       resultados.append(href)
                       resultados_text.insert(tk.END, f"{href}\n")

            if txt_save == True:
                new = busqueda.replace(" ", "")
                with open(f"busqueda_{new}.txt", "w+") as file:
                    for item in resultados:
                        file.write("%s\n" % item)
            else:
                pass
            messagebox.showinfo('DorkBuster', 'Busqueda finalizada.')

# Hecho solo para evitar que el programa se congele al iniciar la funcion "search_func"
def start_search():
    th = threading.Thread(target=search_func)
    th.start()

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
buscar_button.configure(command=start_search)

resultados_text = ScrolledText(ventana)
resultados_text.configure(background="#aaaaaa",font="{Calibri} 10 {}",foreground="#000000")
resultados_text.place(anchor="nw",relheight=0.36,relwidth=0.44,relx=0.30,rely=0.47,x=0,y=0)

if __name__ == "__main__":
    ventana.mainloop()
