import time


class Noeud:
    def __init__(self, nom, voisins, id, coords, station):
        """Constructeur de la class Noeud.

        Args:
            nom (str): nom du noeud
            voisins (dict): liste des noeud voisins
            id (int): identifien du noeud
            coords (tuple): Les coordonnées du noeud
            station (bool): Variable boolean pour savoir si le noeud est une station
        """        
        self.nom = nom
        self.voisins = voisins
        self.id = id
        self.coords = coords
        self.station = station

    def __str__(self):
        return self.nom

    def __repr__(self):
        return self.nom


class Graphe:
    """_summary_
    """
    def __init__(self, noeuds):
        self.noeuds = noeuds

    def __str__(self):
        return str(self.noeuds)

    def __repr__(self):
        return str(self.noeuds)

    def ajouter_noeud(self, noeud):
        """ajoute un noeud à la liste

        Args:
            noeud (Node): noeud a ajouter
        """
        self.noeuds.append(noeud)

    def ajouter_arete(self, noeud1, noeud2, poids_d, poids_e, couleur):
        """Ajoute une arête entre deux noeuds

        Args:
            noeud1 (Node): Noeud de départ
            noeud2 (Node): Noeud d'arrivée
            poids_d (int): Poids du noeud de départ
            poids_e (int): Poids du noeuds d'arrivé
            couleur (str): couleur de la piste
        """
        self.noeuds[self.noeuds.index(noeud1)].voisins[noeud2] = (
            poids_d, poids_e, couleur)

    def supprimer_noeud(self, noeud):
        """Supprime un noeud de la liste

        Args:
            noeud (Node): Noeud à supprimer 
        """
        self.noeuds.remove(noeud)

    def supprimer_arete(self, noeud1, noeud2):
        """Supprime une arête de la liste

        Args:
            noeud1 (Node): Noeud de départ de l'arête 
            noeud2 (Node): Noeud d'arrivé de la liste
        """
        del self.noeuds[noeud1.id].voisins[noeud2]

    def get_noeud(self, nom):
        """Retourne un noeud selon son nom 

        Args:
            nom (str): Nom du noeud 

        Returns:
            Node: Le noeud correspondant au nom
        """
        for noeud in self.noeuds:
            if noeud.nom == nom:
                return noeud

    def get_noeuds(self):
        """Renvoie la liste des noeuds

        Returns:
            lst: liste des noeuds  
        """
        return self.noeuds

    def get_voisins(self, noeud):
        """Renvoie un dictionnaire des noeuds voisins à un noeuds spécifique

        Args:
            noeud (Node): Noeud sélectionné

        Returns:
            dict: Voisins du noeud sélectionné
        """
        return self.noeuds[self.noeuds.index(noeud)].voisins
        # return self.noeuds[noeud.id].voisins

    def get_couleur(self, noeud):
        """_summary_

        Args:
            noeud (Node): Noeud sélectionné

        Returns:
            str: Renvoie la couleur du noeud
        """
        return self.noeuds[noeud.id].couleur

    def get_noeuds_couleur(self, couleur):
        """_summary_

        Args:
            couleur (str): couelur du noeud

        Returns:
            lst: liste de noeud
        """
        noeuds = []
        for noeud in self.noeuds:
            if noeud.couleur == couleur:
                noeuds.append(noeud)
        return noeuds


def dijkstra(graphe, depart, arrivee, niveau_skieur):
    """Algorithme permettant de trouver le plus court chemin entre deux noeuds d'un graphe en fonction du niveau du skieur

    Args:
        graphe (Graphe): Graphe où l'algorithme est appliqué
        depart (Node): Noeud de départ
        arrivee (Node): Noeud d'arrivé
        niveau_skieur (str): Le niveau du skieur

    Returns:
        lst*int: chemin*cout du chemin
    """
    t = time.time()

    # Initialisation
    noeuds = graphe.get_noeuds()
    initialisation(noeuds, depart, "dijkstra")

    # Boucle principale
    noeuds_a_traiter = noeuds.copy()
    while len(noeuds_a_traiter) > 0:
        # On prend le noeud avec le cout le plus faible
        noeud = min(noeuds_a_traiter, key=lambda x: x.cout)
        # On le retire de la liste des noeuds à traiter
        noeuds_a_traiter.remove(noeud)
        # On regarde les voisins du noeud
        if niveau_skieur == "debutant":
            for voisin, (poids_voisin, _, couleur) in graphe.get_voisins(noeud).items():
                # On calcule le cout du chemin
                cout_chemin = plus_court_chemin(
                    noeud, poids_voisin, couleur, "d")
                # On regarde si le chemin est plus court
                verif_plus_court_chemin(
                    noeud, voisin, cout_chemin, arrivee, "dijkstra")
        elif niveau_skieur == "expert":
            for voisin, (_, poids_voisin, couleur) in graphe.get_voisins(noeud).items():
                # On calcule le cout du chemin
                cout_chemin = plus_court_chemin(
                    noeud, poids_voisin, couleur, "d")
                # On regarde si le chemin est plus court
                verif_plus_court_chemin(
                    noeud, voisin, cout_chemin, arrivee, "dijkstra")

    # On reconstruit le chemin
    chemin = reconstruction_chemin(arrivee)
    print("Chemin le plus court de {} à {} :".format(depart.nom, arrivee.nom))
    print(chemin, '---------------')
    print("Temps d'execution : {} secondes".format(time.time() - t))
    return chemin, arrivee.cout


def astar(graphe, depart, arrivee, niveau_skieur):
    t = time.time()
    # Initialisation
    noeuds = graphe.get_noeuds()
    initialisation(noeuds, depart, "astar")

    # Boucle principale
    noeuds_a_traiter = noeuds.copy()
    while len(noeuds_a_traiter) > 0:
        # On prend le noeud avec le cout le plus faible
        noeud = min(noeuds_a_traiter, key=lambda x: x.cout_estime)
        # On le retire de la liste des noeuds à traiter
        noeuds_a_traiter.remove(noeud)
        # On regarde les voisins du noeud
        if niveau_skieur == "debutant":
            for voisin, (poids_voisin, _, couleur) in graphe.get_voisins(noeud).items():
                # On calcule le cout du chemin
                cout_chemin = plus_court_chemin(
                    noeud, poids_voisin, couleur, "d")
                # On regarde si le chemin est plus court
                verif_plus_court_chemin(
                    noeud, voisin, cout_chemin, arrivee, "astar")
        elif niveau_skieur == "expert":
            for voisin, (_, poids_voisin, couleur) in graphe.get_voisins(noeud).items():
                # On calcule le cout du chemin
                cout_chemin = plus_court_chemin(
                    noeud, poids_voisin, couleur, "e")
                # On regarde si le chemin est plus court
                verif_plus_court_chemin(
                    noeud, voisin, cout_chemin, arrivee, "astar")

    # On reconstruit le chemin
    chemin = reconstruction_chemin(arrivee)
    print("Chemin le plus court de {} à {} :".format(depart.nom, arrivee.nom))
    print(chemin, '---------------')
    print("Temps d'execution : {} secondes".format(time.time() - t))
    return chemin, arrivee.cout


def initialisation(noeuds, depart, algo):
    """Initialisation pour l'algorithme d'astar

    Args:
        noeuds (node): Noeud actuel
        depart (Node): Noeud de départ
        algo (str): algorrithme
    """
    for noeud in noeuds:
        noeud.cout = float("inf")
        if algo == "astar":
            noeud.cout_estime = float("inf")
        noeud.precedent = None
    depart.cout = 0
    if algo == "astar":
        depart.cout_estime = 0


def plus_court_chemin(noeud, poids_voisin, couleur, niveau_skieur):
    """Permet de choisir le niveau du skieur

    Args:
        noeud (node): Noeud actuel
        poids_voisin (int): Poids entre le noeud actuel et son noeud voisin
        couleur (str): type de piste de ski
        niveau_skieur (str): Niveau du skieur

    Returns:
        int: Poids du chemin
    """
    if niveau_skieur == "d":
        if couleur == "bleu":
            cout_chemin = noeud.cout + poids_voisin*2
        elif couleur == "rouge":
            cout_chemin = noeud.cout + poids_voisin*5
        elif couleur == "noir":
            cout_chemin = noeud.cout + poids_voisin*8
        elif couleur == "téléphérique":
            cout_chemin = noeud.cout + poids_voisin*3
        elif couleur == "téléski":
            cout_chemin = noeud.cout + poids_voisin*4
        elif couleur == "télésiège":
            cout_chemin = noeud.cout + poids_voisin*5
        else:
            cout_chemin = noeud.cout + poids_voisin
    else:
        if couleur == "bleu":
            cout_chemin = noeud.cout + poids_voisin*1.5
        elif couleur == "rouge":
            cout_chemin = noeud.cout + poids_voisin*2
        elif couleur == "noir":
            cout_chemin = noeud.cout + poids_voisin*3
        elif couleur == "téléphérique":
            cout_chemin = noeud.cout + poids_voisin*3
        elif couleur == "téléski":
            cout_chemin = noeud.cout + poids_voisin*4
        elif couleur == "télésiège":
            cout_chemin = noeud.cout + poids_voisin*5
        else:
            cout_chemin = noeud.cout + poids_voisin
    return cout_chemin


def verif_plus_court_chemin(noeud, voisin, cout_chemin, arrivee, algo):
    """Vérifie que le chemin choisie est le plus court

    Args:
        noeud (Node): Noeud choisie
        voisin (Node): Noeud voisin
        cout_chemin (int): Poids du noeud
        arrivee (Node): Noeud d'arrivé 
        algo (str): algorithme chosit 
    """
    if cout_chemin < voisin.cout:
        voisin.cout = cout_chemin
        voisin.precedent = noeud
        if algo == "astar":
            voisin.cout_estime = cout_chemin + \
                abs(voisin.coords[0] - arrivee.coords[0]) + \
                abs(voisin.coords[1] - arrivee.coords[1])


def reconstruction_chemin(arrivee):
    """_summary_

    Args:
        arrivee (Node): Noeud d'arrivé

    Returns:
        lst: Liste de noeud correspondant au chemin
    """
    chemin = []
    noeud = arrivee
    while noeud is not None:
        chemin.append(noeud)
        noeud = noeud.precedent
    chemin.reverse()
    return chemin
