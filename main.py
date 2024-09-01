import tkinter as tk
from tkinter import ttk
import pandas as pd

# Definisci le categorie predefinite
predefined_categories = ["Portieri", "Difensori", "Centrocampisti", "Attaccanti"]
spunta_categories = ["Rigorista", "Preferiti"]

# Funzione per caricare i dati dal file
def load_data():
    try:
        df = pd.read_csv("data.csv")
        for _, row in df.iterrows():
            values = [row["Nome"], row["Categoria"]] + [row.get(cat, "") for cat in spunta_categories]
            tree.insert("", "end", values=values)
    except FileNotFoundError:
        pass

# Funzione per salvare i dati nel file
def save_data():
    data = [(tree.item(item)["values"][0], tree.item(item)["values"][1]) + tuple(tree.item(item)["values"][2:]) for item in tree.get_children()]
    columns = ["Nome", "Categoria"] + spunta_categories
    df = pd.DataFrame(data, columns=columns)
    df.to_csv("data.csv", index=False)

# Funzione per aggiungere un nuovo nome alla tabella
def add_name():
    name = entry_name.get()
    category = category_entry.get()
    if name and category:
        values = [name, category] + [""] * len(spunta_categories)
        tree.insert("", "end", values=values)
        entry_name.delete(0, tk.END)
        category_entry.set("")
        save_data()
        update_category_filter()

# Funzione per rimuovere i nomi selezionati dalla tabella
def remove_selected():
    selected_items = tree.selection()
    for item in selected_items:
        tree.delete(item)
    save_data()
    update_category_filter()

# Funzione per aggiornare il filtro delle categorie
def update_category_filter():
    categories = set(tree.item(item)["values"][1] for item in tree.get_children())
    category_filter['values'] = ["Tutte"] + list(categories)

# Funzione per filtrare la tabella in base alla categoria selezionata
def filter_table(*args):
    selected_category = category_filter.get()
    for item in tree.get_children():
        tree.delete(item)
    df = pd.read_csv("data.csv")
    for _, row in df.iterrows():
        if selected_category == "Tutte" or row["Categoria"] == selected_category:
            values = [row["Nome"], row["Categoria"]] + [row.get(cat, "") for cat in spunta_categories]
            tree.insert("", "end", values=values)

# Funzione per aggiornare le spunte dei record selezionati
def update_spunta(category):
    selected_items = tree.selection()
    for item in selected_items:
        values = list(tree.item(item)["values"])
        index = 2 + spunta_categories.index(category)
        values[index] = "✓" if values[index] == "" else ""
        tree.item(item, values=values)
    save_data()

# Funzione per aggiungere una nuova categoria di spunta
def add_spunta_category():
    new_category = new_spunta_entry.get()
    if new_category and new_category not in spunta_categories:
        spunta_categories.append(new_category)
        tree["columns"] = ("Nome", "Categoria") + tuple(spunta_categories)
        tree.heading(new_category, text=new_category)
        save_data()
        new_spunta_entry.delete(0, tk.END)

# Funzione per cercare i record
def search_record(*args):
    search_text = search_entry.get().lower()
    for item in tree.get_children():
        tree.delete(item)
    df = pd.read_csv("data.csv")
    for _, row in df.iterrows():
        if search_text in row["Nome"].lower() or search_text in row["Categoria"].lower():
            values = [row["Nome"], row["Categoria"]] + [row.get(cat, "") for cat in spunta_categories]
            tree.insert("", "end", values=values)

# Funzione per importare dati da un file Excel
def import_excel():
    df = pd.read_excel('fanta.xlsx')
    data = df.values.tolist()
    for row in data:
        tree.insert("", "end", values=row)
    save_data()

# Funzione per importare dati da una lista
def import_list(data):
    for row in data:
        tree.insert("", "end", values=row)
    save_data()

# Crea la finestra principale
root = tk.Tk()
root.title("Tabella Interattiva con Categorie")

# Crea un frame per i pulsanti
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# Crea l'entry per inserire i nomi
tk.Label(button_frame, text="Nome:").grid(row=0, column=0, padx=5)
entry_name = tk.Entry(button_frame)
entry_name.grid(row=0, column=1, padx=5)

# Crea il menu a tendina per inserire le categorie
tk.Label(button_frame, text="Categoria:").grid(row=0, column=2, padx=5)
category_entry = ttk.Combobox(button_frame, values=predefined_categories)
category_entry.grid(row=0, column=3, padx=5)

# Crea il pulsante per aggiungere nomi
btn_add = tk.Button(button_frame, text="Aggiungi Nome", command=add_name)
btn_add.grid(row=0, column=4, padx=5)

# Crea il pulsante per rimuovere i nomi selezionati
btn_remove = tk.Button(button_frame, text="Rimuovi Selezionati", command=remove_selected)
btn_remove.grid(row=0, column=5, padx=5)

# Crea i pulsanti per aggiornare le spunte
for i, category in enumerate(spunta_categories):
    btn_spunta = tk.Button(button_frame, text=f"{category}", command=lambda c=category: update_spunta(c))
    btn_spunta.grid(row=1, column=i, padx=5)

# Crea il campo di input per aggiungere nuove categorie di spunta
tk.Label(button_frame, text="Nuova Categoria di Spunta:").grid(row=2, column=0, padx=5)
new_spunta_entry = tk.Entry(button_frame)
new_spunta_entry.grid(row=2, column=1, padx=5)
btn_add_spunta = tk.Button(button_frame, text="Aggiungi Categoria di Spunta", command=add_spunta_category)
btn_add_spunta.grid(row=2, column=2, padx=5)

# Crea il campo di ricerca
tk.Label(button_frame, text="Cerca:").grid(row=2, column=3, padx=5)
search_entry = tk.Entry(button_frame)
search_entry.grid(row=2, column=4, padx=5)
search_entry.bind("<KeyRelease>", search_record)

# Crea il pulsante per importare dati da Excel
btn_import_excel = tk.Button(button_frame, text="Importa da Excel", command=import_excel)
btn_import_excel.grid(row=2, column=5, padx=5)

# Crea il menu a tendina per filtrare le categorie
tk.Label(button_frame, text="Filtra per Categoria:").grid(row=2, column=6, padx=5)
category_filter = ttk.Combobox(button_frame, values=["Tutte"] + predefined_categories)
category_filter.set("Tutte")
category_filter.grid(row=2, column=7, padx=5)
category_filter.bind("<<ComboboxSelected>>", filter_table)

# Crea la tabella
columns = ("Nome", "Categoria") + tuple(spunta_categories)
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Carica i dati dal file
load_data()
update_category_filter()

# Avvia l'interfaccia grafica
root.mainloop()
