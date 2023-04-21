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


def creer_graphe():
    # crée un graphe à 10 sommets avec différentes couleures et différents poids. ne les lie pas tous ensemble
    noeuds = []
    for i in range(10):
        noeuds.append(Noeud(chr(65+i), {}, i))
    graphe = Graphe(noeuds)
    graphe.ajouter_arete(graphe.get_noeud(
        "A"), graphe.get_noeud("B"), 1, 1, "bleu")
    graphe.ajouter_arete(graphe.get_noeud(
        "A"), graphe.get_noeud("C"), 2, 2, "rouge")
    graphe.ajouter_arete(graphe.get_noeud(
        "B"), graphe.get_noeud("C"), 5, 5, "bleu")
    graphe.ajouter_arete(graphe.get_noeud(
        "B"), graphe.get_noeud("D"), 6, 6, "rouge")
    graphe.ajouter_arete(graphe.get_noeud(
        "C"), graphe.get_noeud("D"), 8, 8, "télésiège")
    # graphe.ajouter_arete(graphe.get_noeud("C"), graphe.get_noeud("D"), 8, 8, "noir")
    graphe.ajouter_arete(graphe.get_noeud(
        "D"), graphe.get_noeud("E"), 10, 10, "rouge")

    return graphe


def dijkstra(graphe, depart, arrivee, niveau_skieur):
    # Initialisation
    noeuds = graphe.get_noeuds()
    for noeud in noeuds:
        noeud.cout = float("inf")
        noeud.precedent = None
    depart.cout = 0

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
                if couleur == "bleu":
                    cout_chemin = noeud.cout + poids_voisin*2
                elif couleur == "rouge":
                    cout_chemin = noeud.cout + poids_voisin*5
                elif couleur == "noir":
                    cout_chemin = noeud.cout + poids_voisin*8
                elif couleur == "télécabine":
                    cout_chemin = noeud.cout + poids_voisin*3
                elif couleur == "téléski":
                    cout_chemin = noeud.cout + poids_voisin*4
                elif couleur == "télésiège":
                    cout_chemin = noeud.cout + poids_voisin*5
                else:
                    cout_chemin = noeud.cout + poids_voisin
                # On regarde si le chemin est plus court
                if cout_chemin < voisin.cout:
                    voisin.cout = cout_chemin
                    voisin.precedent = noeud
        elif niveau_skieur == "expert":
            for voisin, (_, poids_voisin, couleur) in graphe.get_voisins(noeud).items():
                # On calcule le cout du chemin
                if couleur == "bleu":
                    cout_chemin = noeud.cout + poids_voisin*1.5
                elif couleur == "rouge":
                    cout_chemin = noeud.cout + poids_voisin*2
                elif couleur == "noir":
                    cout_chemin = noeud.cout + poids_voisin*3
                elif couleur == "télécabine":
                    cout_chemin = noeud.cout + poids_voisin*3
                elif couleur == "téléski":
                    cout_chemin = noeud.cout + poids_voisin*4
                elif couleur == "télésiège":
                    cout_chemin = noeud.cout + poids_voisin*5
                else:
                    cout_chemin = noeud.cout + poids_voisin
                # On regarde si le chemin est plus court
                if cout_chemin < voisin.cout:
                    voisin.cout = cout_chemin
                    voisin.precedent = noeud

    # On reconstruit le chemin
    chemin = []
    noeud = arrivee
    while noeud is not None:
        chemin.append(noeud)
        noeud = noeud.precedent
    chemin.reverse()
    return chemin, arrivee.cout


def main():
    graphe = creer_graphe()
    depart = graphe.get_noeud("A")
    arrivee = graphe.get_noeud("E")
    chemin = dijkstra(graphe, depart, arrivee, "debutant")
    print("Chemin le plus court de {} à {} :".format(depart.nom, arrivee.nom))
    print(chemin)


if __name__ == "__main__":
    main()
