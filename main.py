import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import settings
import Scraper.scraper as scraper

#Paņem galveno logu no iestatījumu faila
root = settings.root

#Funkcija SiteLabel teksta atjaunošanai
def UpdateSelectedSiteCount():
    SELECTEDSITECOUNT = sum(settings.SITES[site]["enabled"].get() == True for site in settings.SITES)
    SiteLabel.configure(text=f"Izvēlēto mājaslapu skaits: {SELECTEDSITECOUNT}")

#Funkcija mājaslapu izvēles logam
def SiteSelection():
    ss = tk.Toplevel()
    ss.title("Izvēlēties")
    ss.geometry("400x400")
    
    DescriptionLabel = tk.Label(ss, text="Izvēlēties mājaslapas", font=('Verdana', 18))
    DescriptionLabel.pack(padx=10, pady=10)

    #Izvada visas mājaslapas kā checkbox
    for site in settings.SITES:
        SiteCheckbox = tk.Checkbutton(ss, text=settings.SITES[site]["name"], variable=settings.SITES[site]["enabled"], onvalue=True, offvalue=False, command=UpdateSelectedSiteCount)
        SiteCheckbox.pack()

DescriptionLabel = tk.Label(root, text="Ziņu analizators", font=('Verdana', 18))
DescriptionLabel.pack(padx=10, pady=10)

SearchGrid = tk.Frame(root)

SiteSelectionButton = tk.Button(SearchGrid, text="Izvēlēties mājaslapas", font=('Verdana', 14), command=SiteSelection)
SiteSelectionButton.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

SiteLabel = tk.Label(SearchGrid, text="Izvēlēto mājaslapu skaits: 0")
SiteLabel.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

SearchLabel = tk.Label(SearchGrid, text="Meklējamais teksts (bez garumzīmēm):")
SearchLabel.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

SearchEntry = tk.Entry(SearchGrid, width=50)
SearchEntry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

TimeLabel = tk.Label(SearchGrid, text="Meklējamais laika periods:")
TimeLabel.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

TimeCombo = ttk.Combobox(SearchGrid, state="readonly", values=settings.TIMEPERIODS)
TimeCombo.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

SearchGrid.pack(padx=10, pady=10)

SearchButton = tk.Button(root, text="Meklēt", font=('Verdana', 14), command=lambda: scraper.Scraper(SearchEntry.get(), TimeCombo.get()))
SearchButton.pack(padx=5, pady=5)

root.mainloop()