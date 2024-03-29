import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser as wb
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, # interface between Figure class and Tkinter's Canvas
    NavigationToolbar2Tk # built-in toolbar for the figure
)

#Funkcija raksta atvēršanai 
def onDoubleClick(event):
    SearchTree = event.widget
    article = SearchTree.identify('item',event.x,event.y)
    link = SearchTree.item(article)['values'][3]
    if link != "":
        wb.open_new_tab(link)

#Funkcija rezultātu nosūtīšanai uz excel failu
def toExcel(results):
    articleList = []
    for result in results:
        for article in results[result]:
            articleList.append([result, results[result][article]['Title'], results[result][article]['Date'], article])
    df = pd.DataFrame(articleList)
    file_name = filedialog.asksaveasfilename(filetypes=[('excel file', '*.xlsx')], defaultextension='.xlsx', initialfile=f"results-{datetime.now().strftime('%d-%m-%yT%H-%M')}")
    df.to_excel(file_name, sheet_name='results', index=False, header=["Mājaslapa", "Virsraksts", "Datums", "Lapa"])

#Funkcija dienā izveidoto rakstu diagrammas parādīšanai
def dailyGraph(results):
    #Iegūst dienā izveidoto rakstu skaitu un saglabā to countDict vārdnīcā
    countDict = {}
    for result in results:
        for article in results[result]:
            day = results[result][article]['Date']
            if day in countDict:
                countDict[day] += 1
            else:
                countDict[day] = 1

    #Ja dienu skaits ir mazāks par 2, tad no diagrammas nav jēga, tādēļ tiek parādīta kļūda
    if len(set(countDict.keys())) < 2:
        messagebox.showerror(title="Diagrammas kļūda", message="Nav rezultāti par pietiekami daudz dienām!")
        return
    
    #Piepilda vārdnīcu ar dienām starp, kurās nav raksti
    minDay = min(countDict)
    maxDay = max(countDict)

    for x in range(0, (maxDay - minDay).days):
        day = minDay + timedelta(days=x)
        if day not in countDict:
            countDict[day] = 0

    #Sakārto dienas un iegūst x un y asis diagrammai
    countDict = dict(sorted(countDict.items()))
    x = list(countDict.keys())
    y = list(countDict.values())

    #Izveido logu un grafiku
    graphWindow = tk.Toplevel()
    graphWindow.title("Dienā izveidoto rakstu diagramma")

    figure = matplotlib.figure.Figure()
    graph = figure.add_subplot()
    graph.plot(x, y)
    
    for tick in graph.get_xticklabels():
        tick.set_rotation(90)

    #Savieno logu ar grafiku un pievieno toolbar
    canvas = FigureCanvasTkAgg(figure, graphWindow)
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, graphWindow)
    toolbar.update()

    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    graphWindow.update()

#Funkcija mājaslapu rakstu skaita diagrammas parādīšanai
def siteGraph(results):
    #Izveido logu
    graphWindow = tk.Toplevel()
    graphWindow.title("Mājaslapu rakstu skaita diagramma")

    #Iegūst x un y asis
    x = results.keys()
    y = list(map(lambda site: len(results[site]), results))

    #Izveido grafiku un pievieno to logam ar toolbar
    figure = matplotlib.figure.Figure()
    graph = figure.add_subplot()
    graph.bar(x, y)

    canvas = FigureCanvasTkAgg(figure, graphWindow)
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, graphWindow)
    toolbar.update()

    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    graphWindow.update()

#Funkcija meklēšanas rezultātu loga parādīšanai
def searchResults(results):
    #Izveido logu
    sresult = tk.Toplevel()
    sresult.title("Meklēšanas rezultāti")
    sresult.geometry("850x500")

    DescriptionLabel = tk.Label(sresult, text="Meklēšanas rezultāti", font=('Verdana', 18))
    DescriptionLabel.pack(padx=10, pady=10)

    #Rāmis excel un diagrammu pogām
    ButtonFrame = tk.Frame(sresult)

    DailyArticlesButton = tk.Button(ButtonFrame, text="Dienā izveidoto rakstu diagramma", font=('Verdana', 14), command=lambda: dailyGraph(results))
    DailyArticlesButton.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    SiteGraphButton = tk.Button(ButtonFrame, text="Mājaslapu rakstu skaita diagramma", font=('Verdana', 14), command=lambda: siteGraph(results))
    SiteGraphButton.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    ToExcelButton = tk.Button(ButtonFrame, text="Izvadīt excel failā", font=('Verdana', 14), command=lambda: toExcel(results))
    ToExcelButton.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

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