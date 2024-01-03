import settings
from datetime import date, timedelta
from tkinter import messagebox

import Scraper.delfi as delfi
import Scraper.lsm as lsm
import Scraper.tvnet as tvnet
import Scraper.apollo as apollo

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
    if settings.SITES["lsm"]["enabled"].get() == True:
        results["lsm"] = lsm.LsmScraper(query, starttime, date.today())
        if results["lsm"] == {}:
            messagebox.showwarning(title="LSM", message="Mājaslapā LSM nekas netika atrasts!")
    if settings.SITES["tvnet"]["enabled"].get() == True:
        results["tvnet"] = tvnet.TvnetScraper(query, starttime, date.today())
        if results["tvnet"] == {}:
            messagebox.showwarning(title="TVNET", message="Mājaslapā TVNET nekas netika atrasts!")
    if settings.SITES["apollo"]["enabled"].get() == True:
        results["apollo"] = apollo.ApolloScraper(query, starttime, date.today())
        if results["apollo"] == {}:
            messagebox.showwarning(title="Apollo", message="Mājaslapā Apollo nekas netika atrasts!")
    print(results)