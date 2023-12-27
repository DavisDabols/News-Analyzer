import tkinter as tk

#Izveido un konfigurē galveno logu
root = tk.Tk()
root.geometry("850x500")
root.title("News Analyzer")

#Mājaslapu opcijas
SITES = {
    "Delfi": tk.Variable(root, False),
    "LSM": tk.Variable(root, False)
}

#Meklēšanas perioda izvēles
TIMEPERIODS = ["Šodien", "Pēdējās 7 dienas", "Pēdējās 30 dienas"]