import tkinter as tk

#Izveido un konfigurē galveno logu
root = tk.Tk()
root.geometry("850x500")
root.title("News Analyzer")

#Mājaslapu opcijas
SITES = {
    "delfi": {
        "name": "Delfi (meklē no 1.1.24)",
        "country": "lv",
        "enabled": tk.Variable(root, False)
        },
    "lsm": {
        "name": "LSM",
        "country": "lv",
        "enabled": tk.Variable(root, False)
    },
    "tvnet": {
        "name": "TVNET",
        "country": "lv",
        "enabled": tk.Variable(root, False)
    },
    "apollo": {
        "name": "Apollo",
        "country": "lv",
        "enabled": tk.Variable(root, False)
    },
    "apnews": {
        "name": "Associated Press",
        "country": "en",
        "enabled": tk.Variable(root, False)
    },
    "reuters": {
        "name": "Reuters",
        "country": "en",
        "enabled": tk.Variable(root, False)
    }
}

#Meklēšanas perioda izvēles
TIMEPERIODS = ["Šodien", "Pēdējās 7 dienas", "Pēdējās 30 dienas"]