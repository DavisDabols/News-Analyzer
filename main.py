import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#Izveido galveno logu un konfigurē to
root = tk.Tk()

root.geometry("850x500")
root.title("News Analyzer")

#Mājaslapu opcijas
SITES = {
    "Delfi": tk.Variable(root, False),
    "LSM": tk.Variable(root, False)
}

#Funkcija SiteLabel teksta atjaunošanai
def UpdateSelectedSiteCount():
    SELECTEDSITECOUNT = sum(SITES[site].get() == True for site in SITES)
    SiteLabel.configure(text=f"Izvēlēto mājaslapu skaits: {SELECTEDSITECOUNT}")

#Funkcija mājaslapu izvēles logam
def SiteSelection():
    ss = tk.Toplevel()
    ss.title("Izvēlēties")
    ss.geometry("400x400")
    
    DescriptionLabel = tk.Label(ss, text="Izvēlēties mājaslapas", font=('Verdana', 18))
    DescriptionLabel.pack(padx=10, pady=10)

    #Izvada visas mājaslapas kā checkbox
    for site in SITES:
        SiteCheckbox = tk.Checkbutton(ss, text=site, variable=SITES[site], onvalue=True, offvalue=False, command=UpdateSelectedSiteCount)
        SiteCheckbox.pack()

DescriptionLabel = tk.Label(root, text="Ziņu analizators", font=('Verdana', 18))
DescriptionLabel.pack(padx=10, pady=10)

SearchGrid = tk.Frame(root)

SiteSelectionButton = tk.Button(SearchGrid, text="Izvēlēties mājaslapas", font=('Verdana', 14), command=SiteSelection)
SiteSelectionButton.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

SiteLabel = tk.Label(SearchGrid, text="Izvēlēto mājaslapu skaits: 0")
SiteLabel.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

SearchLabel = tk.Label(SearchGrid, text="Meklējamais teksts:")
SearchLabel.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

SearchEntry = tk.Entry(SearchGrid, width=50)
SearchEntry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

SearchGrid.pack(padx=10, pady=10)

SearchButton = tk.Button(root, text="Meklēt", font=('Verdana', 14))
SearchButton.pack(padx=5, pady=5)

root.mainloop()