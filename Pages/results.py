import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import webbrowser as wb
import pandas as pd
from datetime import datetime

def onDoubleClick(event):
    SearchTree = event.widget
    article = SearchTree.identify('item',event.x,event.y)
    link = SearchTree.item(article)['values'][3]
    if link != "":
        wb.open_new_tab(link)

def toExcel(results):
    articleList = []
    for result in results:
        for article in results[result]:
            articleList.append([result, results[result][article]['Title'], results[result][article]['Date'], article])
    df = pd.DataFrame(articleList)
    file_name = filedialog.asksaveasfilename(filetypes=[('excel file', '*.xlsx')], defaultextension='.xlsx', initialfile=f"results-{datetime.now().strftime('%d-%m-%yT%H-%M')}")
    df.to_excel(file_name, sheet_name='results', index=False, header=["Mājaslapa", "Virsraksts", "Datums", "Lapa"])

def searchResults(results):

    sresult = tk.Toplevel()
    sresult.title("Meklēšanas rezultāti")
    sresult.geometry("850x500")

    DescriptionLabel = tk.Label(sresult, text="Meklēšanas rezultāti", font=('Verdana', 18))
    DescriptionLabel.pack(padx=10, pady=10)

    ButtonFrame = tk.Frame(sresult)

    ToExcelButton = tk.Button(ButtonFrame, text="Izvadīt excel failā", font=('Verdana', 14), command=lambda: toExcel(results))
    ToExcelButton.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    ButtonFrame.pack(padx=10, pady=10)

    HelpLabel = tk.Label(sresult, text="Nospiediet dubultklikšķi, lai atvērtu rakstu", font=('Verdana', 10))
    HelpLabel.pack(padx=10, pady=10)

    # Rāmis tabulai, kura parāda visus meklēšanas rezultātus
    ResultFrame = tk.Frame(sresult)

    # Definē tabulu
    columns = ('homepage', 'title', 'date', 'page')
    SearchTree = ttk.Treeview(ResultFrame, columns=columns, show="tree headings", selectmode="none")
    SearchTree.heading('homepage', text="Mājaslapa")
    SearchTree.heading('title', text="Virsraksts")
    SearchTree.heading('date', text="Datums")

    SearchTree.column('homepage', width=100)
    SearchTree.column('title', width=500)
    minwidth = SearchTree.column('#0', option='minwidth')
    SearchTree.column('#0', width=minwidth)
    SearchTree.column('date', width=100)
    SearchTree.column('page', width=0, stretch="no")

    # Atjaunina tabulas saturu
    for result in results:
        SearchTree.insert('', tk.END, iid=result, open=False, values=(result, "", "", ""))
        for article in results[result]:
            SearchTree.insert(result, tk.END, values=(result, results[result][article]['Title'], results[result][article]['Date'], article))
    SearchTree.grid(row=0, column=0, sticky="nsew")
    SearchTree.bind('<Double-1>', onDoubleClick)
    # Pievieno ritjoslu rāmim
    scrollbar = ttk.Scrollbar(ResultFrame, orient=tk.VERTICAL, command=SearchTree.yview)
    SearchTree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Pievieno rāmi logam
    ResultFrame.pack(padx=10, pady=5)