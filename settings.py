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