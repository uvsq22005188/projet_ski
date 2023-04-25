import time


class Noeud:
    def __init__(self, nom, voisins, id, coords, station):
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
    def __init__(self, noeuds):
        self.noeuds = noeuds

    def __str__(self):
        return str(self.noeuds)

    def __repr__(self):
        return str(self.noeuds)

    def ajouter_noeud(self, noeud):
        self.noeuds.append(noeud)

    def ajouter_arete(self, noeud1, noeud2, poids_d, poids_e, couleur):
        self.noeuds[self.noeuds.index(noeud1)].voisins[noeud2] = (
            poids_d, poids_e, couleur)

    def supprimer_noeud(self, noeud):
        self.noeuds.remove(noeud)

    def supprimer_arete(self, noeud1, noeud2):
        del self.noeuds[noeud1.id].voisins[noeud2]

    def get_noeud(self, nom):
        for noeud in self.noeuds:
            if noeud.nom == nom:
                return noeud

    def get_noeuds(self):
        return self.noeuds

    def get_voisins(self, noeud):
        return self.noeuds[self.noeuds.index(noeud)].voisins
        # return self.noeuds[noeud.id].voisins

    def get_couleur(self, noeud):
        return self.noeuds[noeud.id].couleur

    def get_noeuds_couleur(self, couleur):
        noeuds = []
        for noeud in self.noeuds:
            if noeud.couleur == couleur:
                noeuds.append(noeud)
        return noeuds


def dijkstra(graphe, depart, arrivee, niveau_skieur):
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
    for noeud in noeuds:
        noeud.cout = float("inf")
        if algo == "astar":
            noeud.cout_estime = float("inf")
        noeud.precedent = None
    depart.cout = 0
    if algo == "astar":
        depart.cout_estime = 0


def plus_court_chemin(noeud, poids_voisin, couleur, niveau_skieur):
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
    if cout_chemin < voisin.cout:
        voisin.cout = cout_chemin
        voisin.precedent = noeud
        if algo == "astar":
            voisin.cout_estime = cout_chemin + \
                abs(voisin.coords[0] - arrivee.coords[0]) + \
                abs(voisin.coords[1] - arrivee.coords[1])


def reconstruction_chemin(arrivee):
    chemin = []
    noeud = arrivee
    while noeud is not None:
        chemin.append(noeud)
        noeud = noeud.precedent
    chemin.reverse()
    return chemin
