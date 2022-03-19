import os
import tkinter
from tkinter.filedialog import askopenfilename
from math import ceil, floor



# On change le répertoire courant avec celui de ce script
chemin = os.path.dirname(__file__)
os.chdir(chemin)

# On masque la fenêtre inutile Tkinter
root = tkinter.Tk()
root.withdraw()
root.update()

# On demande l'image
print("Choix de l'image... ")
while True:
    f = askopenfilename()
    fichier = open(f, "r", errors="ignore")
    contenu = fichier.read()
    fichier.close()
    # On vérifie si le contenu de l'image commence par "P2"
    if not contenu.startswith("P2"):
        print("Veuillez choisir une image PGM... ")
    else:
        break

# On récupère le contenu de l'image dans une liste de ses éléments
contenu = contenu.split("\n")
contenu = [x for x in contenu if x != "" and not x.startswith("#")]
contenu = " ".join(contenu).split()
intensite = int(contenu.pop(3))
hauteur = int(contenu.pop(2))
longueur = int(contenu.pop(1))
contenu.pop(0)
# On récupère les pixels de l'image dans une liste
liste_pixels = [int(x) for x in contenu]

def saisie_traitement():
    """Demande à l'utilisateur le type de retouche souhaité puis renvoie le numéro (nombre entier) choisi"""
    print("""Traitements d'image disponibles:
    1 Noir et blanc
    2 Négatif
    3 Miroir
    4 Flou
    5 Rotation horaire de 90 degrés
    6 Zoom x4""")
    while True:
        try:
            nombre = int(input("Numéro : "))
        except ValueError:
            print("Erreur, veuillez choisir un numéro.")
            continue
        if not 1 <= nombre <= 6:
            print("Erreur, le numéro doit être compris entre 1 et 6.")
            continue
        return nombre

def saisie_nom():
    """Demande à l'utilisateur le nom de la nouvelle image puis renvoie le nom choisi (string) avec l'extension"""
    while True:
        nouveau_nom = str(input("Nom de la nouvelle image : "))
        if not nouveau_nom:
            print("Erreur, le nom ne doit pas être vide.")
            continue
        if os.path.exists(nouveau_nom + ".pgm"):
            print("Erreur, ce nom est déjà attribué.")
            continue
        return nouveau_nom + ".pgm"

def creation(texte, l, h, nom):
    """Créer la nouvelle image transformée"""
    nouveau_fichier = open(nom, "w")
    texte = f"P2\n{l} {h}\n{intensite}\n" + texte
    nouveau_fichier.write(texte)
    nouveau_fichier.close()
    print("Nouvelle image PGM créée : " + nom)


def noir_et_blanc(pixels):
    """Renvoie l'ensemble (string) des pixels de l'image en noir et blanc"""
    resultat = ""
    for pixel in pixels:
        if pixel >= 127:
            # Si la couleur du pixel est plus proche de 255
            resultat += "255 "
        else:
            # Sinon la couleur du pixel est plus proche de 0
            resultat += "0 "
    return resultat, str(longueur), str(hauteur)

def negatif(pixels):
    """Renvoie l'ensemble (string) des pixels de l'image en negatif"""
    resultat = ""
    for pixel in pixels:
        # On prend la couleur opposée du pixel
        resultat += str(255 - pixel) + " "
    return resultat, str(longueur), str(hauteur)

def miroir(pixels):
    """Renvoie l'ensemble (string) des pixels de l'image en miroir (symétrie verticale de l’image)"""
    resultat = ""
    # matrice des pixels de l'image
    matrice = [[pixels[x + y * longueur] for x in range(longueur)][:] for y in range(hauteur)]
    for ligne in matrice:
        for pixel in reversed(ligne): # on utilise les pixels de la ligne inversée
            resultat += str(pixel) + " "
    return resultat, str(longueur), str(hauteur)

def flouter(pixels):
    """Renvoie l'ensemble (string) des pixels de l'image en flou"""
    intensite_flou = 9 # plus c'est grand, plus le traitement sera long
    resultat = ""
    for y in range(hauteur): # ordonnée de l'image
        for x in range(longueur): # abscisse de l'image
            nb = []
            for a in range(-1 * floor(intensite_flou / 2), ceil(intensite_flou / 2)): # ordonnée de la zone : un carré de longueur intensite_flou avec le pixel comme centre
                for b in range(-1 * floor(intensite_flou / 2), ceil(intensite_flou / 2)): # abscisse de la zone
                    if 0 <= x + a < longueur and 0 <= y + b < hauteur: # on vérifie si le pixel se trouve bien dans la zone
                        nb.append(pixels[(y + b) * longueur + x + a]) # ajout du pixel grâce à sa position dans la liste par rapport aux coordonnées
            moyenne = int(sum(nb) / len(nb)) # moyenne des pixels de la zone
            resultat += str(moyenne) + " "
    return resultat, str(longueur), str(hauteur)

def rotation(pixels):
    """Renvoie l'ensemble (string) des pixels de l'image avec une rotation horaire de 90°"""
    resultat = ""
    for x in range(longueur, 0, -1):
        for y in range(hauteur, 0, -1):
            resultat += str(pixels[y * longueur - x]) + " " # ajout du pixel via sa position
    return resultat, str(hauteur), str(longueur)

def zoom_4x(pixels):
    """Renvoie l'ensemble (string) des pixels de l'image en zoomée (4 fois plus grande)"""
    resultat = ""
    for y in range(hauteur):
        for _ in range(2): # on le fait 2 fois
            for x in range(longueur):
                for _ in range(2): # on le fait 2 fois
                    resultat += str(pixels[y * longueur + x]) + " " # ajout du pixel via sa position
    return resultat, str(longueur * 2), str(hauteur * 2)



# Main : boucle infinie
while True:
    choix = saisie_traitement()
    print("Traitement en cours... ")
    if choix == 1:
        texte, l, h = noir_et_blanc(liste_pixels)
    elif choix == 2:
        texte, l, h = negatif(liste_pixels)
    elif choix == 3:
        texte, l, h = miroir(liste_pixels)
    elif choix == 4:
        texte, l, h = flouter(liste_pixels)
    elif choix == 5:
        texte, l, h = rotation(liste_pixels)
    elif choix == 6:
        texte, l, h = zoom_4x(liste_pixels)
    creation(texte, l, h, saisie_nom())
    input("\nAppuyez sur Entrée pour continuer ou fermez le programme... ")
