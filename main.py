import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint, choice
from collections import deque
import time
import matplotlib.pyplot as plt

def pieces_adjacentes_non_connectees(img, x, y):
    voisins = []
    for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < img.width and 0 <= ny < img.height:
            if img.getpixel((nx, ny)) == (128, 128, 128):
                voisins.append((nx, ny))
    return voisins

def creer_labyrinthe(w, h):
    img = Image.new("RGB", (w, h), (0, 0, 0))
    for i in range(1, w, 2):
        for j in range(1, h, 2):
            img.putpixel((i, j), (128, 128, 128))
    x, y = randint(0, w//2 - 1)*2 + 1, randint(0, h//2 - 1)*2 + 1
    img.putpixel((x, y), (255, 255, 255))
    chemin = []
    while True:
        voisins = pieces_adjacentes_non_connectees(img, x, y)
        if not voisins:
            if not chemin:
                break
            x, y = chemin.pop()
            continue
        vx, vy = choice(voisins)
        img.putpixel((vx, vy), (255, 255, 255))
        img.putpixel(((x + vx) // 2, (y + vy) // 2), (255, 255, 255))
        chemin.append((x, y))
        x, y = vx, vy
    entree = randint(0, w//2 - 1)*2 + 1
    sortie = randint(0, w//2 - 1)*2 + 1
    img.putpixel((entree, 0), (255, 255, 255))
    img.putpixel((sortie, h - 1), (255, 255, 255))
    return img

def voisins_non_visites(img, x, y):
    voisins = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < img.width and 0 <= ny < img.height:
            if img.getpixel((nx, ny)) == (255, 255, 255):
                voisins.append((nx, ny))
    return voisins

def trouver_depart(img):
    for x in range(img.width):
        if img.getpixel((x, 0)) == (255, 255, 255):
            return (x, 0)
    raise ValueError("Pas de départ trouvé.")

def dessiner_chemin(img, chemin):
    for x, y in chemin:
        img.putpixel((x, y), (255, 0, 0))

def resoudre(img, algo="BFS"):
    depart = trouver_depart(img)
    if algo == "BFS":
        file = deque([depart])
        origines = {}
        while file:
            n = file.popleft()
            img.putpixel(n, (128, 128, 128))
            if n[1] == img.height - 1:
                chemin = [n]
                while n in origines:
                    n = origines[n]
                    chemin.append(n)
                return list(reversed(chemin))
            for v in voisins_non_visites(img, *n):
                if v not in origines:
                    file.append(v)
                    origines[v] = n
        return None
    else:
        chemin = []
        noeud = depart
        while noeud[1] < img.height - 1:
            voisins = voisins_non_visites(img, *noeud)
            if not voisins:
                if not chemin:
                    return None
                noeud = chemin.pop()
                continue
            chemin.append(noeud)
            noeud = voisins[0]
            img.putpixel(noeud, (128, 128, 128))
        chemin.append(noeud)
        return chemin

class LabyrintheApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Explorateur de Labyrinthe")
        self.labyrinthe = None

        self._ajouter_formulaire()
        self._ajouter_boutons()
        self._ajouter_affichage()

    def _ajouter_formulaire(self):
        frm = tk.Frame(self.root)
        frm.pack(pady=10)

        tk.Label(frm, text="Largeur (impair)").grid(row=0, column=0)
        tk.Label(frm, text="Hauteur (impair)").grid(row=1, column=0)
        tk.Label(frm, text="Itérations/point (graph)").grid(row=2, column=0)

        self.entry_w = tk.Entry(frm); self.entry_w.insert(0, "51")
        self.entry_h = tk.Entry(frm); self.entry_h.insert(0, "51")
        self.entry_iter = tk.Entry(frm); self.entry_iter.insert(0, "5")

        self.entry_w.grid(row=0, column=1)
        self.entry_h.grid(row=1, column=1)
        self.entry_iter.grid(row=2, column=1)

    def _ajouter_boutons(self):
        frm = tk.Frame(self.root)
        frm.pack(pady=5)

        tk.Button(frm, text="Générer", command=self.generer).grid(row=0, column=0, padx=5)
        tk.Button(frm, text="Résoudre BFS", command=lambda: self.resoudre("BFS")).grid(row=0, column=1, padx=5)
        tk.Button(frm, text="Résoudre DFS", command=lambda: self.resoudre("DFS")).grid(row=0, column=2, padx=5)
        tk.Button(frm, text="Temps BFS vs DFS", command=self.comparer_temps).grid(row=1, column=0, columnspan=2, pady=5)
        tk.Button(frm, text="Graphe Temps vs Taille", command=self.graphe_temps_vs_taille).grid(row=1, column=2, pady=5)

    def _ajouter_affichage(self):
        self.label_img = tk.Label(self.root)
        self.label_img.pack(pady=10)

    def generer(self):
        try:
            w = int(self.entry_w.get())
            h = int(self.entry_h.get())
            if w % 2 == 0 or h % 2 == 0:
                raise ValueError
        except:
            messagebox.showerror("Erreur", "Dimensions invalides (impaire uniquement)")
            return

        self.labyrinthe = creer_labyrinthe(w, h)
        self.afficher(self.labyrinthe)
        messagebox.showinfo("Succès", f"Labyrinthe {w}x{h} généré.")

    def resoudre(self, methode):
        if not self.labyrinthe:
            messagebox.showwarning("Avertissement", "Générez un labyrinthe d'abord.")
            return

        copie = self.labyrinthe.copy()
        chemin = resoudre(copie, algo=methode)
        if chemin:
            dessiner_chemin(copie, chemin)
            self.afficher(copie)
        else:
            messagebox.showerror("Erreur", "Aucun chemin trouvé.")

    def comparer_temps(self):
        if not self.labyrinthe:
            messagebox.showerror("Erreur", "Veuillez d'abord générer un labyrinthe.")
            return

        img_bfs = self.labyrinthe.copy()
        t1 = time.time(); resoudre(img_bfs, "BFS"); t2 = time.time()

        img_dfs = self.labyrinthe.copy()
        t3 = time.time(); resoudre(img_dfs, "DFS"); t4 = time.time()

        temps = [t2 - t1, t4 - t3]
        plt.bar(["BFS", "DFS"], temps, color=["blue", "green"])
        plt.ylabel("Temps (secondes)")
        plt.title("Comparaison BFS vs DFS")
        plt.tight_layout()
        plt.show()

    def graphe_temps_vs_taille(self):
        try:
            n_iter = int(self.entry_iter.get())
            if n_iter < 1:
                raise ValueError
        except:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre d'itérations valide.")
            return

        tailles = [11, 21, 31, 41, 51]
        pixels, temps_bfs, temps_dfs = [], [], []

        for taille in tailles:
            total_bfs = 0
            total_dfs = 0
            for _ in range(n_iter):
                img = creer_labyrinthe(taille, taille)
                t1 = time.time(); resoudre(img.copy(), "BFS"); t2 = time.time()
                t3 = time.time(); resoudre(img.copy(), "DFS"); t4 = time.time()
                total_bfs += (t2 - t1)
                total_dfs += (t4 - t3)
            pixels.append(taille * taille)
            temps_bfs.append(total_bfs / n_iter)
            temps_dfs.append(total_dfs / n_iter)

        plt.plot(pixels, temps_bfs, marker='o', label="BFS", color='blue')
        plt.plot(pixels, temps_dfs, marker='o', label="DFS", color='green')
        plt.xlabel("Nombre de pixels")
        plt.ylabel("Temps moyen (s)")
        plt.title(f"Temps vs Taille ({n_iter} itérations)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def afficher(self, img):
        zoom = img.resize((img.width * 3, img.height * 3), Image.NEAREST)
        self.tk_img = ImageTk.PhotoImage(zoom)
        self.label_img.config(image=self.tk_img)
        self.label_img.image = self.tk_img

if __name__ == "__main__":
    root = tk.Tk()
    app = LabyrintheApp(root)
    root.mainloop()
