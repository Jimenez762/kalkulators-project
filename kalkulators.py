import tkinter as tk
from tkinter import messagebox

class Kalkulators:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulators")
        self.root.geometry("300x450") # Atbilst izšķirtspējas prasībām
        
        self.atmina = "0" # Funkcijai K6 un K8
        self.operacija = None
        self.pirmais_skaitlis = None
        self.jauns_ievads = True

        # 1. Lauks "Skaitlis"
        self.ekrans = tk.Entry(root, font=("Arial", 24), borderwidth=5, relief="flat", justify='right')
        self.ekrans.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.ekrans.insert(0, "0")

        # 2. Lauks "Saglabātā vērtība"
        self.atminas_labels = tk.Label(root, text="Iegaumēts: 0", anchor="w")
        self.atminas_labels.grid(row=1, column=0, columnspan=4, padx=10, sticky="w")

        # Pogu nosaukumi un to funkcijas atbilstoši PPS struktūrai
        pogas = [
            ('S', 2, 0, self.saglabat), ('I', 2, 1, self.ievadit_atminu), ('C', 2, 2, self.nodzest), ('/', 2, 3, lambda: self.set_operacija('/')),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('x', 3, 3, lambda: self.set_operacija('*')),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('-', 4, 3, lambda: self.set_operacija('-')),
            ('7', 5, 0), ('8', 5, 1), ('9', 5, 2), ('+', 5, 3, lambda: self.set_operacija('+')),
            ('+/-', 6, 0, self.mainit_zimi), ('0', 6, 1), (',', 6, 2, self.pielikt_komatu), ('=', 6, 3, self.aprekinat)
        ]

        for p in pogas:
            teksts = p[0]
            r = p[1]
            c = p[2]
            if len(p) > 3:
                komanda = p[3]
            else:
                komanda = lambda t=teksts: self.cipara_ievade(t)
            
            tk.Button(root, text=teksts, width=5, height=2, command=komanda).grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

    # K1: Ievadīt skaitli
    def cipara_ievade(self, cipars):
        pasreizejais = self.ekrans.get()
        
        # Pārbaude uz 7 simbolu limitu
        if len(pasreizejais.replace('-', '').replace(',', '')) >= 7 and not self.jauns_ievads:
            return

        if self.jauns_ievads:
            self.ekrans.delete(0, tk.END)
            self.ekrans.insert(0, cipars)
            self.jauns_ievads = False
        else:
            if pasreizejais == "0":
                self.ekrans.delete(0, tk.END)
                self.ekrans.insert(0, cipars)
            else:
                self.ekrans.insert(tk.END, cipars)

    # K7: Atgriezt sākuma vērtību
    def nodzest(self):
        self.ekrans.delete(0, tk.END)
        self.ekrans.insert(0, "0")
        self.jauns_ievads = True

    def pielikt_komatu(self):
        val = self.ekrans.get()
        if "," not in val: # PPS noteikums: ja satur komatu, otru nepievieno
            self.ekrans.insert(tk.END, ",")
            self.jauns_ievads = False

    def mainit_zimi(self):
        val = self.ekrans.get()
        if val != "0": # PPS: ja nulle, zīmi nemaina
            if val.startswith("-"):
                self.ekrans.delete(0, 1)
            else:
                self.ekrans.insert(0, "-")

    # K6: Iegaumēt vērtību
    def saglabat(self):
        self.atmina = self.ekrans.get()
        self.atminas_labels.config(text=f"Iegaumēts: {self.atmina}")
        self.nodzest()

    # K8: Ievadīt iegaumēto vērtību
    def ievadit_atminu(self):
        vertiba = self.atmina[:7] # PPS: garums jāsamazina līdz 7 simboliem
        self.ekrans.delete(0, tk.END)
        self.ekrans.insert(0, vertiba)
        self.jauns_ievads = False

    def set_operacija(self, op):
        self.pirmais_skaitlis = float(self.ekrans.get().replace(',', '.'))
        self.operacija = op
        self.jauns_ievads = True

    # K2-K5: Aritmētiskās operācijas
    def aprekinat(self):
        if self.operacija is None: return
        
        otrais = float(self.ekrans.get().replace(',', '.'))
        rezultats = 0
        
        try:
            if self.operacija == '+': rezultats = self.pirmais_skaitlis + otrais
            elif self.operacija == '-': rezultats = self.pirmais_skaitlis - otrais
            elif self.operacija == '*': rezultats = self.pirmais_skaitlis * otrais
            elif self.operacija == '/':
                if otrais == 0:
                    # K5: Dalīšanas ar nulli kļūdas
                    if self.pirmais_skaitlis == 0:
                        messagebox.showinfo("Informācija", "Bezgalība!")
                    else:
                        messagebox.showerror("Kļūda", "Kļūda: dalīt ar nulli nedrīkst!")
                    self.nodzest()
                    return
                rezultats = self.pirmais_skaitlis / otrais
            
            # Attēlošana
            res_str = str(round(rezultats, 4)).replace('.', ',')
            self.ekrans.delete(0, tk.END)
            self.ekrans.insert(0, res_str[:9]) # Ievērojot kopējo vizuālo limitu
            self.jauns_ievads = True
            self.operacija = None
        except:
            self.nodzest()

if __name__ == "__main__":
    root = tk.Tk()
    app = Kalkulators(root)
    root.mainloop()