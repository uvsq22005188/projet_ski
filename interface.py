import tkinter as tk
import pickle
import math
from tkinter import Button, Scrollbar, Menu, StringVar, Radiobutton
from tkinter.filedialog import asksaveasfile, askopenfile
from graphe import Noeud, Graphe, dijkstra


class MainApplication(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        # self.root.attributes("-fullscreen", True)
        self.pack()
        self.create_widgets()

        self.taille = 15
        self.compteur_noeud = 0
        self.debut_x, self.debut_y = None, None
        self.ligne = None
        self.current = None
        self.noeud1, self.noeud2 = None, None
        self.pile_retour = []
        self.graphe = None
        self.couleur = None
        self.utilisateur_experimente = False
        self.liste_couleur = ["green", "blue", "red", "black"]
        self.couleur_point = "red"
        self.depart, self.arrivee = None, None

    def couleur_piste(self):
        """
        Retourne la couleur du bouton qui est presse
        """
        return self.v.get()

    def choix_point(self):
        """
        Definit la couleur du point selon le bouton qui est presse
        """
        if self.v.get() == "intersection":
            self.couleur_point = "green"
        else:
            self.couleur_point = "red"

    def choix_niveau_skieur(self):
        """
        Definit le niveau du skieur selon le bouton qui est presse
        """
        if self.v_niveau.get() == "0":
            self.utilisateur_experimente = True
        else:
            self.utilisateur_experimente = False

    def delete_graph_widgets(self):
        """
        supprime de l'ecran tout les widget en rapport avec la creation du graphe et unbind les touches
        """
        self.b_vert.forget()
        self.b_bleu.forget()
        self.b_rouge.forget()
        self.b_noir.forget()
        self.b_teleski.forget()
        self.b_telesiege.forget()
        self.b_telecabine.forget()

        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonPress-3>")
        self.canvas.unbind("<ButtonRelease-3>")
        self.root.unbind("<Control-z>")

    def create_graph_widgets(self):
        """
        Creer et ajoute a l'ecran tout les widget en rapport avec la creation du graphe et bind les touches

        """
        self.v = StringVar()

        # Dictionary to create multiple buttons

        self.b_vert = Radiobutton(self.root, text="Piste Verte", variable=self.v,
                                  value="green", indicator=0,
                                  background="green", command=self.couleur_piste)
        self.b_bleu = Radiobutton(self.root, text="Piste Bleue", variable=self.v,
                                  value="blue", indicator=0,
                                  background="blue", command=self.couleur_piste)
        self.b_rouge = Radiobutton(self.root, text="Piste Rouge", variable=self.v,
                                   value="red", indicator=0,
                                   background="red", command=self.couleur_piste)
        self.b_noir = Radiobutton(self.root, text="Piste Noire", variable=self.v,
                                  value="black", indicator=0,
                                  background="gray", command=self.couleur_piste)
        self.b_teleski = Radiobutton(self.root, text="Téléski", variable=self.v,
                                     value="teleski", indicator=0,
                                     background="white", command=self.couleur_piste)

        self.b_telesiege = Radiobutton(self.root, text="Télésiège", variable=self.v,
                                       value="telesiege", indicator=0,
                                       background="white", command=self.couleur_piste)
        self.b_telecabine = Radiobutton(self.root, text="Télécabine", variable=self.v,
                                        value="telecabine", indicator=0,
                                        background="white", command=self.couleur_piste)

        self.b_station = Radiobutton(self.root, text="Point Station", variable=self.v,
                                     value="station", indicator=0,
                                     background="white", command=self.choix_point)
        self.b_intersection = Radiobutton(self.root, text="Point Intersection", variable=self.v,
                                          value="intersection", indicator=0,
                                          background="white", command=self.choix_point)

        self.b_station.pack(fill="x", ipady=5)
        self.b_intersection.pack(fill="x", ipady=5)

        self.b_vert.pack(fill="x", ipady=5)
        self.b_bleu.pack(fill="x", ipady=5)
        self.b_rouge.pack(fill="x", ipady=5)
        self.b_noir.pack(fill="x", ipady=5)
        self.b_teleski.pack(fill="x", ipady=5)
        self.b_telesiege.pack(fill="x", ipady=5)
        self.b_telecabine.pack(fill="x", ipady=5)

        # Bind du clic gauche sur le canvas pour ajouter des points d'intersection
        self.canvas.bind("<Button-1>", self.ajouter_noeud)
        self.canvas.bind("<ButtonPress-3>", self.debut_ligne)
        self.canvas.bind("<ButtonRelease-3>", self.tracer_ligne)
        self.root.bind("<Control-z>", self.retour_arriere)

    def delete_skieur_widget(self):
        """
        supprime de l'ecran tout les widget en rapport avec le skieur
        """
        self.b_skieur_debutant.forget()
        self.b_skieur_experimente.forget()

    def create_skieur_widget(self):
        """
        Creer et ajoute a l'ecran tout les widget en rapport avec le skieur
        """

        self.v_niveau = StringVar()

        self.b_skieur_experimente = Radiobutton(self.root, text="Skieur Expérimenté", variable=self.v_niveau,
                                                value=0, indicator=0,
                                                background="white", command=self.choix_niveau_skieur)
        self.b_skieur_debutant = Radiobutton(self.root, text="Skieur Débutant", variable=self.v_niveau,
                                             value=1, indicator=0, command=self.choix_niveau_skieur)

        self.b_skieur_experimente.pack(fill="x", ipady=5)
        self.b_skieur_debutant.pack(fill="x", ipady=5)

    def create_widgets(self):
        """
        Creation des widgets de base
        """
        # Création d'un Canvas
        self.width = 2440
        self.height = 1440
        self.canvas = tk.Canvas(
            self, width=self.width, height=self.height, scrollregion=(0, 0, 3600, 3000))

        self.canvas.bind('<Control-MouseWheel>',
                         lambda event: self.canvas.xview_scroll(-int(event.delta/120), 'units'))
        self.canvas.bind(
            '<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta/120), 'units'))

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

        # Creation menu

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.point_menu = Menu(self.menubar, tearoff=False)
        self.graphe_menu = Menu(self.menubar, tearoff=False)
        self.edition_menu = Menu(self.menubar, tearoff=False)
        self.skieur_menu = Menu(self.menubar, tearoff=False)

        self.menubar.add_cascade(
            label="Point",
            menu=self.point_menu
        )

        self.menubar.add_cascade(
            label="Graphe",
            menu=self.graphe_menu
        )

        self.menubar.add_cascade(
            label="Edition",
            menu=self.edition_menu
        )

        self.menubar.add_cascade(
            label="Skieur",
            menu=self.skieur_menu
        )

        self.edition_menu.add_command(
            label="Activer edition de graphe", command=self.create_graph_widgets)
        self.edition_menu.add_command(
            label="Désactiver edition de graphe", command=self.delete_graph_widgets)

        self.point_menu.add_command(
            label="Sauvegarder points", command=self.sauver_points)
        self.point_menu.add_command(
            label="Charger points", command=self.charger_points)

        self.graphe_menu.add_command(
            label="Sauvegarder graphe", command=self.sauver_graphe)
        self.graphe_menu.add_command(
            label="Charger graphe", command=self.charger_graphe)
        self.graphe_menu.add_command(
            label="Créer graphe", command=self.creer_graphe)

        self.skieur_menu.add_command(
            label="Activer edition skieur", command=self.create_skieur_widget)
        self.skieur_menu.add_command(
            label="Désactiver edition skieur", command=self.delete_skieur_widget)

        self.skieur_menu.add_command(
            label="Debut", command=self.choix_depart)
        self.skieur_menu.add_command(
            label="Fin", command=self.choix_fin)
        self.skieur_menu.add_command(
            label="Recherche chemin", command=self.recherche_chemin)

        # Ajout de l'image en arrière-plan
        self.background_img = tk.PhotoImage(file="plan_piste.png")
        self.canvas.create_image(
            1800, 1500, image=self.background_img, anchor="center")

        # Ajout d'une variable pour stocker les noeuds
        self.liste_noeuds = []

    def recherche_chemin(self):
        """
        recupere le chemin avec la fonction dijkstra et l'affiche a ecran
        """
        self.chemin = dijkstra(
            self.graphe, self.depart, self.fin, "debutant")
        self.afficher_chemin()

    def choix_depart(self):
        """
        bind clique gauche pour cliquer sur le point de depart
        """
        self.canvas.bind(
            "<Button-1>", self._choix_depart)

    def choix_fin(self):
        """
        bind clique gauche pour cliquer sur le point d'arrive
        """
        self.canvas.bind(
            "<Button-1>", self._choix_fin)

    def _choix_depart(self, event):
        """
        trouve le neoud le plus proche du clique et unbind la touche
        """
        self.depart = self.trouver_noeud_proche(event)[0]
        self.canvas.unbind("<Button-1>")

        print(self.depart)

    def _choix_fin(self, event):
        """
        trouve le neoud le plus proche du clique et unbind la touche
        """
        self.fin = self.trouver_noeud_proche(event)[0]
        self.canvas.unbind("<Button-1>")

        print(self.fin)

    def sauver_points(self):
        """
        Sauvegarde avec Pickle la liste des noeuds
        """
        file = asksaveasfile(defaultextension='.pkl', mode="wb")
        if file:
            pickle.dump(self.liste_noeuds, file)

    def sauver_graphe(self):
        """
        Sauvegarde avec Pickle le graphe
        """
        file = asksaveasfile(defaultextension='.pkl', mode="wb")
        if file:
            pickle.dump(self.graphe, file)

    def charger_points(self):
        """
        Charge avec Pickle la liste des noeuds
        """
        file = askopenfile(defaultextension='.pkl', mode="rb")
        if file:
            self.liste_noeuds = pickle.load(file)
            self.afficher_points()

    def charger_graphe(self):
        """
        Charge avec Pickle le graphe
        """
        file = askopenfile(defaultextension='.pkl', mode="rb")
        if file:
            self.graphe = pickle.load(file)
            self.liste_noeuds = self.graphe.noeuds

            # recupere le nombre de noeud pour remettre a jour le compteur de noeud
            self.compteur_noeud = len(self.liste_noeuds)

            self.afficher_graphe()

    def afficher_points(self):
        """
        Parcours la liste des noeuds, recupere leur coordonnes et affiche les noeuds a l'ecran
        """
        self.canvas.delete("noeud")
        for noeud in self.liste_noeuds:
            self.tag = noeud.id
            print(self.tag)
            (x, y) = noeud.coords

            nouveau_noeud = self.canvas.create_oval(
                x-self.taille, y-self.taille, x+self.taille, y+self.taille, fill="red", tags=self.tag)

            if noeud.station:
                self.canvas.itemconfig(nouveau_noeud, fill="red")

            else:
                self.canvas.itemconfig(nouveau_noeud, fill="green")

    def afficher_arretes(self):
        """
        Parcours la liste des noeuds, recupere les voisins et trace les arretes a l'ecran
        """
        for noeud in self.graphe.noeuds:
            x, y = noeud.coords
            dict_voisins = noeud.voisins.items()
            for noeud_tuple in dict_voisins:
                # instance du noeud (cle du dictionnaire)
                x1, y1 = noeud_tuple[0].coords
                # derniere valeur du tuple (valeur du dictionnaire)
                couleur = noeud_tuple[1][-1]

                ligne = self.canvas.create_line(
                    x, y, x1, y1)
                if couleur in self.liste_couleur:
                    self.canvas.itemconfig(ligne, width=5, fill=couleur)

                else:
                    self.canvas.itemconfig(
                        ligne, width=8, fill="black", dash=(5, 1))

    def afficher_graphe(self):
        """
        Affiche le graphe
        """
        self.canvas.delete("neoud")
        self.afficher_points()
        self.afficher_arretes()

    def creer_graphe(self):
        """
        Creer instance de l'objet graphe avec tout les points
        """
        self.graphe = Graphe(self.liste_noeuds)

    def retour_arriere(self, event):
        """
        Efface le dernier noeud creer
        """
        if self.pile_retour:
            dernier_noeud = self.pile_retour.pop()
            self.canvas.delete(dernier_noeud.id)
            del self.liste_noeuds[-1]

    def trouver_nom_noeud(self, id_noeud):
        """
        compare l'id du noeud a tout les noeud pour trouver le nom du noeud
        """
        for _, value in enumerate(self.liste_noeuds):
            print(value.id)
            if value.id == id_noeud:
                return value

    def trouver_noeud_proche(self, event):
        """
        trouve le noeud le plus proche par rapport au clique souris
        """

        self.current = self.canvas.find_closest(
            self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

        tag = self.canvas.gettags(self.current)[0]
        print(tag)

        nom = self.trouver_nom_noeud(tag)
        coords = self.canvas.coords(self.current)

        if "n-" in tag:
            return nom, coords

    def debut_ligne(self, event):
        """
        recupere les coordonnes et le nom du noeud
        """

        nom, coords = self.trouver_noeud_proche(event)
        try:
            self.noeud1 = nom
            self.debut_x, self.debut_y = coords[0], coords[1]

        except:
            print("Pas de noeud")

    def tracer_ligne(self, event):
        """
        recupere les coordonnes et le nom du 2eme noeud pour tracer une arrete entre les deux noeuds
        """

        nom, coords = self.trouver_noeud_proche(event)

        self.noeud2 = nom
        self.ligne = self.canvas.create_line(
            self.debut_x+self.taille, self.debut_y+self.taille, coords[2]-self.taille, coords[3]-self.taille)

        self.couleur = self.couleur_piste()

        if self.couleur in self.liste_couleur:
            self.canvas.itemconfig(self.ligne, width=5, fill=self.couleur)
        else:
            self.canvas.itemconfig(self.ligne, width=8,
                                   fill="black", dash=(5, 1))

        self.poids = self._calcul_distance()

        self.graphe.ajouter_arete(
            self.noeud1, self.noeud2, poids_d=self.poids, poids_e=self.poids, couleur=self.couleur)

    def _calcul_distance(self):
        """
        Calcul la distance entre les deux noeuds
        """

        x1, y1 = self.noeud1.coords
        x2, y2 = self.noeud2.coords
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return int(distance)

    def ajouter_noeud(self, event):
        """
        ajoute nouveau noeud a la liste des noeuds et l'affiche a l'ecran
        """

        self.tag = ("n-%d" % self.compteur_noeud, "noeud")

        # Dessine un petit cercle pour représenter le point d'intersection
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.canvas.create_oval(
            x-self.taille, y-self.taille, x+self.taille, y+self.taille, fill=self.couleur_point, tags=self.tag)

        # Ajoute a liste_noeuds le nouveau point
        if self.couleur_point == "red":
            noeud = Noeud(nom=f"Noeud{self.compteur_noeud}",
                          voisins={}, id=self.tag[0], coords=(x, y), station=True)

        else:
            noeud = Noeud(nom=f"Noeud{self.compteur_noeud}",
                          voisins={}, id=self.tag[0], coords=(x, y), station=False)

        self.compteur_noeud += 1

        self.liste_noeuds.append(noeud)

        self.pile_retour.append(noeud)

    def afficher_arrete_chemin(self):
        """
        surligne le chemin trouve
        """
        x1, y1 = self.noeud1.coords
        x2, y2 = self.noeud2.coords
        test = self.canvas.create_line(x1, y1, x2, y2, tag="chemin")
        self.canvas.itemconfig(test, width=20,
                               fill="black", dash=(5, 1))

    def blinking_on(self):
        """
        fait clignoter le chemin
        """
        self.liste_arretes_chemin = self.canvas.find_withtag("chemin")

        for arrete in self.liste_arretes_chemin:
            self.canvas.itemconfig(arrete, width=0)

        self.root.after(500, self.blinking_off)

    def blinking_off(self):
        """
        fait clignoter le chemin
        """
        for arrete in self.liste_arretes_chemin:
            self.canvas.itemconfig(arrete, width=20)

        self.root.after(500, self.blinking_on)

    def afficher_chemin(self):
        """
        affiche a l'ecran le chemin trouvé
        """
        print(self.chemin)
        self.distance = self.chemin[-1]
        self.parcours = self.chemin[0]
        for noeud in self.parcours:
            voisins = noeud.voisins
            print(voisins)
            self.noeud1 = noeud
            for noeud_voisin in voisins:
                if noeud_voisin in self.parcours:
                    self.noeud2 = noeud_voisin
                    self.afficher_arrete_chemin()
        self.blinking_on()


root = tk.Tk()
app = MainApplication(root=root)
app.mainloop()
