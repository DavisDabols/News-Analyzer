import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import settings
import Scraper.scraper as scraper
import Pages.loading_page as lp

#Paņem galveno logu no iestatījumu faila
root = settings.root

#Funkcija SiteLabel teksta atjaunošanai un attiecīgās valodas ievades ieslēgšanai
def UpdateSelectedSiteWidgets():
    SELECTEDSITECOUNT = sum(settings.SITES[site]["enabled"].get() == True for site in settings.SITES)
    SiteLabel.configure(text=f"Izvēlēto mājaslapu skaits: {SELECTEDSITECOUNT}")

    SearchEntryLV.config(state="disabled")
    SearchEntryEN.config(state="disabled")

    for site in settings.SITES:
        if settings.SITES[site]["country"] == "lv" and settings.SITES[site]["enabled"].get() == True:
            SearchEntryLV.config(state="normal")
        elif settings.SITES[site]["country"] == "en" and settings.SITES[site]["enabled"].get() == True:
            SearchEntryEN.config(state="normal")

#Funkcija mājaslapu izvēles logam
def SiteSelection():
    ss = tk.Toplevel()
    ss.title("Izvēlēties")
    ss.geometry("400x400")
    
    DescriptionLabel = tk.Label(ss, text="Izvēlēties mājaslapas", font=('Verdana', 18))
    DescriptionLabel.pack(padx=10, pady=10)

    #Izvada visas mājaslapas kā checkbox
    for site in settings.SITES:
        SiteCheckbox = tk.Checkbutton(ss, text=f"{settings.SITES[site]['name']} [{settings.SITES[site]['country']}]", justify="left", variable=settings.SITES[site]["enabled"], onvalue=True, offvalue=False, command=UpdateSelectedSiteWidgets)
        SiteCheckbox.pack()

def search(queryLV, queryEN, time):
    pass


DescriptionLabel = tk.Label(root, text="Ziņu analizators", font=('Verdana', 18))
DescriptionLabel.pack(padx=10, pady=10)

SearchGrid = tk.Frame(root)

SiteSelectionButton = tk.Button(SearchGrid, text="Izvēlēties mājaslapas", font=('Verdana', 14), command=SiteSelection)
SiteSelectionButton.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

SiteLabel = tk.Label(SearchGrid, text="Izvēlēto mājaslapu skaits: 0")
SiteLabel.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

SearchLabelLV = tk.Label(SearchGrid, text="Meklējamais teksts (bez garumzīmēm) LV mājaslapās:")
SearchLabelLV.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

SearchEntryLV = tk.Entry(SearchGrid, width=50, state="disabled")
SearchEntryLV.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

SearchLabelEN = tk.Label(SearchGrid, text="Meklējamais teksts EN mājaslapās:")
SearchLabelEN.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

SearchEntryEN = tk.Entry(SearchGrid, width=50, state="disabled")
SearchEntryEN.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

TimeLabel = tk.Label(SearchGrid, text="Meklējamais laika periods:")
TimeLabel.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

TimeCombo = ttk.Combobox(SearchGrid, state="readonly", values=settings.TIMEPERIODS)
TimeCombo.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

SearchGrid.pack(padx=10, pady=10)

SearchButton = tk.Button(root, text="Meklēt", font=('Verdana', 14), command=lambda: lp.openLoadingPage(SearchEntryLV.get(), SearchEntryEN.get(), TimeCombo.get()))
SearchButton.pack(padx=5, pady=5)

root.mainloop()