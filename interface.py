import tkinter as tk
import pickle
import math
from tkinter import Scrollbar
from tkinter.filedialog import asksaveasfile, askopenfile
from graphe import Noeud, Graphe


class MainApplication(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack()
        self.create_widgets()

        self.taille = 15
        self.debut_x, self.debut_y = None, None
        self.ligne = None
        self.current = None
        self.noeud1, self.noeud2 = None, None
        self.pile_retour = []

    def create_widgets(self):
        # Création d'un Canvas
        self.width = 1280
        self.height = 720
        self.canvas = tk.Canvas(
            self, width=self.width, height=self.height, scrollregion=(0, 0, 3600, 3000))

        # Creation bouttons

        self.b_sauvegarder = tk.Button(
            root, text="Sauvegarder Points", command=self.sauver_points)
        self.b_charger = tk.Button(
            root, text="Charger Points", command=self.charger_points)
        self.b_sauvegarder.pack()
        self.b_charger.pack()

        # Creation scrollbar x

        self.hbar = Scrollbar(self, orient="horizontal")
        self.hbar.pack(side="bottom", fill="x")
        self.hbar.config(command=self.canvas.xview)

        self.canvas.config(xscrollcommand=self.hbar.set)
        # Creation scrollbar y

        self.vbar = Scrollbar(self, orient="vertical")
        self.vbar.pack(side="right", fill="y")
        self.vbar.config(command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.vbar.set)
        self.canvas.pack()

        # Ajout de l'image en arrière-plan
        self.background_img = tk.PhotoImage(file="plan_piste.png")
        self.canvas.create_image(
            1800, 1500, image=self.background_img, anchor="center")

        # Ajout d'une variable pour stocker les points d'intersection
        self.liste_noeuds = []

        # Bind du clic gauche sur le canvas pour ajouter des points d'intersection
        self.canvas.bind("<Button-1>", self.ajouter_noeud)
        self.canvas.bind("<ButtonPress-3>", self.debut_ligne)
        self.canvas.bind("<ButtonRelease-3>", self.tracer_ligne)
        self.root.bind("<Control-z>", self.retour_arriere)

    def sauver_points(self):
        file = asksaveasfile(defaultextension='.pkl', mode="wb")
        if file:
            pickle.dump(self.liste_noeuds, file)

    def charger_points(self):
        file = askopenfile(defaultextension='.pkl', mode="rb")
        if file:
            self.liste_noeuds = pickle.load(file)
            print(self.liste_noeuds)
            print(self.liste_noeuds[0].id)
            self.afficher_points()

    def afficher_points(self):
        """
        """
        self.canvas.delete("noeud")
        for noeud in self.liste_noeuds:
            (x, y) = noeud.coords
            noeud_canvas = self.canvas.create_oval(
                x-self.taille, y-self.taille, x+self.taille, y+self.taille, fill="red", tags='noeud')

    def retour_arriere(self):
        """

        """
        print("ctrl-z")
        if self.pile_retour:
            dernier_noeud = self.pile_retour.pop()
            self.canvas.delete(dernier_noeud.id)
            del self.liste_noeuds[-1]
            print(self.liste_noeuds)

    def trouver_nom_noeud(self, id):
        """
        """
        for key, value in enumerate(self.liste_noeuds):
            if value.id == id:
                print(value)
                return value

    def trouver_noeud_proche(self, event):

        self.current = self.canvas.find_closest(
            self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

        tag = self.canvas.gettags(self.current)

        nom = self.trouver_nom_noeud(self.current[0])
        coords = self.canvas.coords(self.current)

        if "noeud" in tag:
            return nom, coords

    def debut_ligne(self, event):

        nom, coords = self.trouver_noeud_proche(event)
        try:
            self.noeud1 = nom
            self.debut_x, self.debut_y = coords[0], coords[1]

        except:
            print("Pas de noeud")

    def tracer_ligne(self, event):

        nom, coords = self.trouver_noeud_proche(event)

        try:

            self.noeud2 = nom
            self.ligne = self.canvas.create_line(
                self.debut_x+self.taille, self.debut_y+self.taille, coords[2]-self.taille, coords[3]-self.taille)

            self.canvas.itemconfig(self.ligne, width=3)

            self.retour_liste.append(self.ligne)

            self.calcul_distance()

            print(nom.id)
        except:
            pass

    def calcul_distance(self):

        x1, y1 = self.noeud1.coords
        x2, y2 = self.noeud2.coords
        print(x1, x2, y1, y2)
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        print(distance)
        return distance

    def calcul_poids(self):
        pass

    def ajouter_arete(self, event):
        pass

    def ajouter_noeud(self, event):

        # Dessine un petit cercle pour représenter le point d'intersection
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        noeud_canvas = self.canvas.create_oval(
            x-self.taille, y-self.taille, x+self.taille, y+self.taille, fill="red", tags='noeud')

        # Recupere ID du noeud
        noeud_canvas_id = self.canvas.find_withtag(noeud_canvas)[0]

        # Ajoute a liste_noeuds le nouveau point
        noeud = Noeud(nom=chr(63+noeud_canvas_id), voisins={},
                      id=noeud_canvas_id, coords=(x, y))

        self.liste_noeuds.append(noeud)

        self.pile_retour.append(noeud)

        print(f'noeud_canvas_id: {noeud_canvas_id}')
        print(self.liste_noeuds)


root = tk.Tk()
app = MainApplication(root=root)
app.mainloop()
