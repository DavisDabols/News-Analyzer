import settings
from datetime import date, timedelta
from tkinter import messagebox

import Scraper.delfi as delfi

def Scraper(query, time):
    results = {}
    if time == "Šodien":
        starttime = date.today()
    elif time == "Pēdējās 7 dienas":
        starttime = date.today() - timedelta(days=7)
    elif time == "Pēdējās 30 dienas":
        starttime = date.today() - timedelta(days=30)
    else:
        messagebox.showerror(title="Error", message="Nepareizs laika periods")
        return 400
    if settings.SITES["delfi"]["enabled"].get() == True:
        results["delfi"] = delfi.DelfiScraper(query, starttime, date.today())
        if results["delfi"] == {}:
            messagebox.showwarning(title="Delfi", message="Mājaslapā delfi nekas netika atrasts!")
    print(results)