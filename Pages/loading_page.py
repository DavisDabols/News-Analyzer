import tkinter as tk

import Scraper.scraper as scraper
import Pages.results as res

def openLoadingPage(query, time):
    lp = tk.Toplevel()
    
    # Definē izmēru un atrašanās vietu (centrā)
    s_width = lp.winfo_screenwidth()
    s_height = lp.winfo_screenheight()
    x_cordinate = int((s_width/2) - 50)
    y_cordinate = int((s_height/2) - 25)
    lp.geometry(f"100x50+{x_cordinate}+{y_cordinate}")

    # Novieto logu virs visa un noņem augšējo uzdevumjoslu
    lp.attributes('-topmost', 'true')
    lp.lift()
    lp.overrideredirect(1)

    lp['background'] = '#b0d9bb'

    loadingLabel = tk.Label(lp, text="Lādējas", font=('Verdana', 10), background='#b0d9bb')
    loadingLabel.pack(expand=True)

    lp.update()

    results = scraper.Scraper(query, time)

    # Pēc Scrapper funkcijas izpildes iznīcina logu
    lp.destroy()
    lp.update()

    res.searchResults(results)

