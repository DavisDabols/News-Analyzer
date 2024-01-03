import tkinter as tk
from tkinter import ttk

def searchResults(results):
    sresult = tk.Toplevel()
    sresult.title("Meklēšanas rezultāti")
    sresult.geometry("850x500")

    DescriptionLabel = tk.Label(sresult, text="Meklēšanas rezultāti", font=('Verdana', 18))
    DescriptionLabel.pack(padx=10, pady=10)

    # Rāmis tabulai, kura parāda visus meklēšanas rezultātus
    ResultFrame = tk.Frame(sresult)

    # Definē tabulu
    columns = ('homepage', 'title', 'page')
    SearchTree = ttk.Treeview(ResultFrame, columns=columns, show="headings")
    SearchTree.heading('homepage', text="Mājaslapa")
    SearchTree.heading('title', text="Virsraksts")
    SearchTree.heading('page', text="Adrese")
    # Atjaunina tabulas saturu
    for result in results:
        for article in results[result]:
            print(article)
            SearchTree.insert('', tk.END, values=(result, results[result][article], article))
    SearchTree.grid(row=0, column=0, sticky="nsew")
    # Pievieno ritjoslu rāmim
    scrollbar = ttk.Scrollbar(ResultFrame, orient=tk.VERTICAL, command=SearchTree.yview)
    SearchTree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Pievieno rāmi logam
    ResultFrame.pack(padx=10, pady=5)