import tkinter as tk
from tkinter.filedialog import asksaveasfile, askopenfile
import sys
import graphe
import pickle
import math


class App(tk.Tk):
    def __init__(self, title, size):

        # Configuration principale

        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # Configuration variables des bouttons

        self.var_piste = tk.StringVar()
        self.var_point = tk.StringVar()
        self.var_skieur = tk.StringVar()
        self.var_algorithme = tk.StringVar()

        # Creation d'un graphe vide

        self.graphe = graphe.Graphe(noeuds=[])

        # Frame

        self.frame_canvas = FrameCanvas(self)
        self.dessin = Dessin(self, self.frame_canvas)
        self.frame_graphe = FrameGraphe(self, self.frame_canvas, self.dessin)
        self.frame_skieur = FrameSkieur(self, self.frame_canvas)
        self.fichier = Fichier(self, self.dessin)

        # Menu

        self.menubar = MenuBar(
            self, self.frame_graphe, self.frame_canvas, self.frame_skieur,
            self.fichier)
        self.config(menu=self.menubar)

        # Boucle principale

        self.mainloop()


class Dessin():
    def __init__(self, parent, frame_canvas):
        self.parent = parent
        self.frame_canvas = frame_canvas
        self.canvas = self.frame_canvas.canvas
        self.taille = 15
        self.liste_couleur = ["green", "blue", "red", "black"]
        self.noeud1, self.noeud2 = None, None

    def get_noeuds(self):
        return self.parent.graphe.get_noeuds()

    def afficher_graphe(self):
        """
        Affiche le graphe
        """
        self.canvas.delete("noeud")
        self.afficher_aretes()
        self.afficher_points()

    def afficher_points(self):
        """
        Parcours la liste des noeuds, recupere leur coordonnes et
        affiche les noeuds a l'ecran
        """
        self.canvas.delete("noeud")
        liste_noeuds = self.get_noeuds()

        for noeud in liste_noeuds:
            tag = noeud.id
            (x, y) = noeud.coords

            nouveau_noeud = self.canvas.create_oval(
                x-self.taille, y-self.taille,
                x+self.taille, y+self.taille,
                fill="red", tags=tag, activefill="black")

            if noeud.station:
                self.canvas.itemconfig(nouveau_noeud, fill="red")

            else:
                self.canvas.itemconfig(nouveau_noeud, fill="green")

            print(noeud)

    def afficher_aretes(self):
        """
        Parcours la liste des noeuds, recupere les voisins et trace
        les aretes a l'ecran
        """
        liste_noeuds = self.get_noeuds()
        for noeud in liste_noeuds:
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

    def ajouter_noeud(self, event):  # FIXME
        """
        ajoute nouveau noeud a la liste des noeuds et l'affiche a l'ecran
        """
        nombre_de_noeuds = len(self.get_noeuds())
        tag = ("n-%d" % nombre_de_noeuds, "noeud")

        var_point = self.parent.var_point.get()

        # Dessine un petit cercle pour représenter le point d'intersection
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        point = self.canvas.create_oval(
            x-self.taille, y-self.taille, x+self.taille, y+self.taille, fill='red', tags=tag, activefill="black")

        if var_point == 'station':
            self.canvas.itemconfig(point, fill="red")
            noeud = graphe.Noeud(nom=f"Noeud{nombre_de_noeuds}",
                                 voisins={}, id=tag[0], coords=(x, y),
                                 station=True)
        else:
            self.canvas.itemconfig(point, fill="green")
            noeud = graphe.Noeud(nom=f"Noeud{nombre_de_noeuds}",
                                 voisins={}, id=tag[0], coords=(x, y),
                                 station=False)

        self.parent.graphe.ajouter_noeud(noeud)

        # self.pile_retour.append(noeud) #FIXME

    def debut_arete(self, event):
        self.noeud1 = self.frame_canvas.trouver_noeud_proche(event)

    def fin_arete(self, event):
        self.noeud2 = self.frame_canvas.trouver_noeud_proche(event)
        if self.noeud1 and self.noeud2:
            self.tracer_arete()

    def tracer_arete(self):
        x1, y1 = self.noeud1.coords
        x2, y2 = self.noeud2.coords

        arete = self.canvas.create_line(
            x1, y1, x2, y2)

        self.modifier_arete(arete)

    def modifier_arete(self, arete):
        couleur = self.parent.var_piste.get()
        if couleur in self.liste_couleur:
            self.canvas.itemconfig(arete, width=5, fill=couleur)
        else:
            self.canvas.itemconfig(arete, width=8,
                                   fill="black", dash=(5, 1))

        self.ajouter_arete(couleur)

    def ajouter_arete(self, couleur):
        """
        """

        poids = self.calcule_distance(self.noeud1, self.noeud2)

        self.parent.graphe.ajouter_arete(
            self.noeud1, self.noeud2, poids_d=poids, poids_e=poids,
            couleur=couleur)

    def calcule_distance(self, noeud1, noeud2):
        """
        """
        noeud1_x, noeud1_y = noeud1.coords
        noeud2_x, noeud2_y = noeud2.coords
        return math.sqrt((noeud1_x - noeud2_x) ** 2 + (noeud1_y - noeud2_y) ** 2)


class Fichier():
    def __init__(self, parent, dessin):
        self.parent = parent
        self.dessin = dessin

    def charger_graphe(self):
        """
        Charge avec Pickle le graphe
        """
        file = askopenfile(defaultextension='.pkl', mode="rb")
        if file:
            self.parent.graphe = pickle.load(file)
            self.dessin.afficher_graphe()

    def sauvegarder_graphe(self):
        """
        """
        file = asksaveasfile(defaultextension='.pkl', mode="wb")
        if file:
            pickle.dump(self.parent.graphe, file)


class MenuBar(tk.Menu):
    def __init__(self, parent, frame_graphe, frame_canvas, frame_skieur, fichier):
        super().__init__(parent)
        self.parent = parent
        self.frame_graphe = frame_graphe
        self.frame_canvas = frame_canvas
        self.frame_skieur = frame_skieur
        self.fichier = fichier

        # File Menu

        fileMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", underline=0, menu=fileMenu)
        fileMenu.add_command(label="Sauvegarder Graphe",
                             underline=1,
                             command=self.fichier.sauvegarder_graphe)
        fileMenu.add_command(label="Charger Graphe",
                             underline=1,
                             command=self.fichier.charger_graphe)
        fileMenu.add_command(label="Exit",
                             underline=1, command=self.quit)

        # Graphe Menu

        grapheMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Graphe", underline=0, menu=grapheMenu)
        grapheMenu.add_command(label="Edition Graphe",
                               underline=1,
                               command=self.frame_graphe.affichage_frame)

        # Skieur Menu

        skieurMenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Skieur", underline=0, menu=skieurMenu)
        skieurMenu.add_command(label="Edition Skieur",
                               underline=1,
                               command=frame_skieur.affichage_frame)

    # Fonctions file

    def quit(self):
        sys.exit(0)

    # Fonctions graphe

    # Fonctions skieur


class FrameCanvas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.depart, self.arrivee = None, None
        self.grid(row=0, column=0, sticky='nsew')
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=10)
        self.canvas = tk.Canvas(self)
        self.canvas.configure(scrollregion=(0, 0, 3600, 3000))
        self.canvas.pack(fill='both', expand=True, anchor='n')

        # Bind souris

        self.canvas.bind('<Control-MouseWheel>',
                         lambda event: self.canvas.xview_scroll
                         (-int(event.delta/120),
                          'units'))
        self.canvas.bind('<MouseWheel>',
                         lambda event: self.canvas.yview_scroll
                         (-int(event.delta/120),
                          'units'))

        # Scrollbar X

        self.hbar = tk.Scrollbar(self.canvas, orient='horizontal')
        self.hbar.pack(side='bottom', fill='x')
        self.hbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.hbar.set)

        # Scrollbar Y

        self.vbar = tk.Scrollbar(self.canvas, orient='vertical')
        self.vbar.pack(side='right', fill='y')
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)
        # Plan de piste en arriere plan

        self.bg_image = tk.PhotoImage(file='plan_piste.png')
        self.canvas.create_image(0, 0,
                                 image=self.bg_image, anchor='nw')

    def infos_chemins(self):
        pass
        # label = tk.Label(
        #     self.canvas, text=f"Point de départ: {self.depart} \
        #         - Point d'arrivé: {self.arrivee} - Niveau: \
        #             {self.parent.var_skieur.get()}")
        # label.pack()

    def trouver_nom_noeud(self, id_noeud):
        """
        compare l'id du noeud a tout les noeud pour trouver le nom du noeud
        """
        liste_noeuds = self.parent.graphe.get_noeuds()

        for _, value in enumerate(liste_noeuds):
            if value.id == id_noeud:
                return value

    def trouver_noeud_proche(self, event):  # TODO
        """
        trouve le noeud le plus proche par rapport au clique souris
        """
        self.current = self.canvas.find_closest(
            self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

        tag = self.canvas.gettags(self.current)[0]

        noeud = self.trouver_nom_noeud(id_noeud=tag)

        if 'n-' in tag:
            return noeud

    def choix_depart_arrivee(self):
        self.canvas.bind("<Button-1>", self._choix_depart)

    def _choix_depart(self, event):
        """
        """
        self.depart = self.trouver_noeud_proche(event)
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self._choix_arrivee)

    def _choix_arrivee(self, event):
        """
        """
        self.arrivee = self.trouver_noeud_proche(event)
        self.canvas.unbind("<Button-1>")
        self.infos_chemins()

    def recherche_chemin(self):
        """
        """
        chemin = graphe.dijkstra(
            self.parent.graphe, self.depart, self.arrivee, "debutant")
        print(chemin)

    def afficher_chemin(self):
        chemin = self.recherche_chemin()


class FrameGraphe(tk.Frame):

    def __init__(self, parent, frame_canvas, dessin):
        super().__init__(parent)

        self.parent = parent
        self.frame_canvas = frame_canvas
        self.dessin = dessin

        self.compteur = 1

        self.configure(bg='red')

        parent.grid_rowconfigure(1, weight=1)

        for i in range(4):
            self.rowconfigure(i, weight=1)
        for i in range(3):
            self.columnconfigure(i, weight=1)

        self.creation_widget()
        self.placement_widget()

    def creation_widget(self):

        self.var = tk.StringVar()

        self.b_vert = tk.Radiobutton(self, text="Piste Verte",
                                     variable=self.var,
                                     value="green", indicator=0,
                                     background="green",
                                     command=self.couleur_piste)
        self.b_bleu = tk.Radiobutton(self, text="Piste Bleue",
                                     variable=self.var,
                                     value="blue", indicator=0,
                                     background="blue",
                                     command=self.couleur_piste)
        self.b_rouge = tk.Radiobutton(self, text="Piste Rouge",
                                      variable=self.var,
                                      value="red", indicator=0,
                                      background="red",
                                      command=self.couleur_piste)
        self.b_noir = tk.Radiobutton(self, text="Piste Noire",
                                     variable=self.var,
                                     value="black", indicator=0,
                                     background="gray",
                                     command=self.couleur_piste)
        self.b_teleski = tk.Radiobutton(self, text="Téléski",
                                        variable=self.var,
                                        value="teleski", indicator=0,
                                        background="white",
                                        command=self.couleur_piste)

        self.b_telesiege = tk.Radiobutton(self, text="Télésiège",
                                          variable=self.var,
                                          value="telesiege", indicator=0,
                                          background="white",
                                          command=self.couleur_piste)
        self.b_telecabine = tk.Radiobutton(self, text="Télécabine",
                                           variable=self.var,
                                           value="telecabine", indicator=0,
                                           background="white",
                                           command=self.couleur_piste)

        self.b_station = tk.Radiobutton(self, text="Point Station",
                                        variable=self.var,
                                        value="station", indicator=0,
                                        background="white",
                                        command=self.choix_point)
        self.b_intersection = tk.Radiobutton(self, text="Point Intersection",
                                             variable=self.var,
                                             value="intersection", indicator=0,
                                             background="white",
                                             command=self.choix_point)

    def placement_widget(self):
        self.b_station.grid(row=0, column=0, ipadx=5,
                            ipady=5, sticky='nsew')
        self.b_intersection.grid(
            row=0, column=1, ipadx=5, ipady=5, sticky='nsew')

        self.b_vert.grid(row=1, column=0, ipadx=5, ipady=5, sticky='nsew')
        self.b_bleu.grid(row=1, column=1, ipadx=5, ipady=5, sticky='nsew')
        self.b_rouge.grid(row=2, column=0, ipadx=5, ipady=5, sticky='nsew')
        self.b_noir.grid(row=2, column=1, ipadx=5, ipady=5, sticky='nsew')
        self.b_teleski.grid(row=3, column=0, ipadx=5,
                            ipady=5, sticky='nsew')
        self.b_telesiege.grid(row=3, column=1, ipadx=5,
                              ipady=5, sticky='nsew')
        self.b_telecabine.grid(row=3, column=2, ipadx=5,
                               ipady=5, sticky='nsew')

    def activer_bind(self):

        self.frame_canvas.canvas.bind("<Button-1>", self.dessin.ajouter_noeud)
        self.frame_canvas.canvas.bind(
            "<ButtonPress-3>", self.dessin.debut_arete)
        self.frame_canvas.canvas.bind(
            "<ButtonRelease-3>", self.dessin.fin_arete)

        self.parent.bind("<Control-z>", self.quit)

    def desactiver_bind(self):

        self.frame_canvas.canvas.unbind("<Button-1>")
        self.frame_canvas.canvas.unbind("<ButtonPress-3>")
        self.frame_canvas.canvas.unbind("<ButtonRelease-3>")

        self.parent.unbind("<Control-z>")

    def affichage_frame(self):
        if self.compteur % 2:
            self.grid(row=1, column=0, sticky='nsew')
            self.activer_bind()
        else:
            self.grid_forget()
            self.desactiver_bind()

        self.compteur += 1

    def choix_point(self):
        self.parent.var_point.set(self.var.get())

    def couleur_piste(self):
        self.parent.var_piste.set(self.var.get())


class FrameSkieur(tk.Frame):
    def __init__(self, parent, frame_canvas):
        super().__init__(parent)
        self.parent = parent
        self.frame_canvas = frame_canvas
        self.compteur = 1
        self.var_niveau = tk.StringVar()
        self.var_algorithme = tk.StringVar()
        for i in range(2):
            self.columnconfigure(i, weight=1)
        for i in range(3):
            self.rowconfigure(i, weight=1)

        self.creation_widget()
        self.placement_widget()

    def creation_widget(self):

        self.b_skieur_experimente = tk.Radiobutton(self,
                                                   text="Skieur Expérimenté",
                                                   variable=self.var_niveau,
                                                   value='experimente',
                                                   indicator=0,
                                                   command=self.choix_niveau)
        self.b_skieur_debutant = tk.Radiobutton(self,
                                                text="Skieur Débutant",
                                                variable=self.var_niveau,
                                                value='debutant', indicator=0,
                                                command=self.choix_niveau)

        self.b_dijkstra = tk.Radiobutton(self,
                                         text="Dijkstra",
                                         variable=self.var_algorithme,
                                         value='dijkstra', indicator=0,
                                         command=self.choix_niveau)
        self.b_astar = tk.Radiobutton(self,
                                      text="A*",
                                      variable=self.var_algorithme,
                                      value='astar', indicator=0,
                                      command=self.choix_niveau)
        self.b_depart = tk.Button(
            self, text="Départ/Arrivée",
            command=self.frame_canvas.choix_depart_arrivee)
        self.b_arrive = tk.Button(
            self, text="Afficher Chemin",
            command=self.frame_canvas.afficher_chemin)

    def placement_widget(self):
        self.b_skieur_debutant.grid(
            row=0, column=0, ipadx=5, ipady=5, sticky='nsew')
        self.b_skieur_experimente.grid(
            row=0, column=1, ipadx=5, ipady=5, sticky='nsew')
        self.b_dijkstra.grid(
            row=1, column=0, ipadx=5, ipady=5, sticky='nsew')
        self.b_astar.grid(
            row=1, column=1, ipadx=5, ipady=5, sticky='nsew')
        self.b_depart.grid(
            row=2, column=0, ipadx=5, ipady=5, sticky='nsew')
        self.b_arrive.grid(
            row=2, column=1, ipadx=5, ipady=5, sticky='nsew')

    def affichage_frame(self):
        if self.compteur % 2:
            self.grid(row=1, column=0, sticky='nsew')
        else:
            self.grid_forget()

        self.compteur += 1

    def choix_niveau(self):
        self.parent.var_skieur.set(self.var_niveau.get())

    def choix_algorithme(self):
        self.parent.var_algorithme.set(self.var_algorithme.get())


App('Projet Ski', (800, 800))