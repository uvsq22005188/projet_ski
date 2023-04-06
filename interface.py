import tkinter as tk
from tkinter import Scrollbar


class MainApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Création d'un Canvas
        self.width = 1280
        self.height = 720
        self.canvas = tk.Canvas(
            self, width=self.width, height=self.height, scrollregion=(0, 0, 3600, 3000))

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

        # Ajout d'un bouton pour placer des points d'intersection
        self.button = tk.Button(
            self, text="Placer un point", command=self.place_intersection_point)
        self.button.pack(side="left")

        # Ajout d'une variable pour stocker les points d'intersection
        self.intersection_points = []

        # Bind du clic gauche sur le canvas pour ajouter des points d'intersection
        self.canvas.bind("<Button-1>", self.add_intersection_point)

    def place_intersection_point(self):
        # Permet à l'utilisateur de cliquer sur le canvas pour placer un point
        self.canvas.config(cursor="plus")

    def add_intersection_point(self, event):
        # Ajoute un point d'intersection à la liste
        self.intersection_points.append(
            (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)))

        # Dessine un petit cercle pour représenter le point d'intersection
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="red")


root = tk.Tk()
app = MainApplication(master=root)
app.mainloop()
