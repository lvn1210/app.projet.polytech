import flet as ft
import json
import os
from datetime import datetime

FICHIER_PROFIL = "profils.json"

def charger_profils():
    if os.path.exists(FICHIER_PROFIL):
        with open(FICHIER_PROFIL, "r") as f:
            return json.load(f)
    return []

def sauvegarder_profil(nouveau):
    profils = charger_profils()
    for i, p in enumerate(profils):
        if p["prenom"].lower() == nouveau["prenom"].lower():
            profils[i] = nouveau
            break
    else:
        profils.append(nouveau)
    with open(FICHIER_PROFIL, "w") as f:
        json.dump(profils, f, indent=2)

def calc_metabolisme(poids, taille, age):
    return round(10 * poids + 6.25 * taille - 5 * age + 5)

def calc_course(poids, duree, fc):
    return max(0, round(duree * (0.6309 * fc - 0.1988 * poids - 55) / 4.184))

def calc_tabata(tours):
    return tours * 4 * 13

def calc_sauna(poids, duree):
    return round(0.17 * poids * duree)

def main(page: ft.Page):
    page.title = "CalcForme"
    page.bgcolor = "#F5F5F3"
    page.window.width = 480
    page.window.height = 620

    BLEU = "#1A3A8F"
    ROUGE = "#CC3333"

    profil = {"prenom": "", "age": 0, "poids": 0.0, "taille": 0.0, "activites": []}

    def ajouter_activite(type_activite, details, kcal):
        """Ajoute une activité à l'historique et sauvegarde."""
        entree = {
            "type": type_activite,
            "details": details,
            "kcal": kcal,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }
        profil["activites"].append(entree)
        sauvegarder_profil(profil)

    def btn(texte, action):
        return ft.Button(
            texte, on_click=action,
            bgcolor=BLEU, color="white",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
            width=300, height=50,
        )

    def retour(action):
        return ft.TextButton("← Retour", on_click=action, style=ft.ButtonStyle(color=BLEU))

    def changer_ecran(contenu):
        page.controls.clear()
        page.add(contenu)
        page.update()


    def ecran_accueil():
        profils = charger_profils()
        elements = [ft.Row([]), ft.Text("CalcForme", size=40, weight="bold", color="#111111")]

        if profils:
            elements.append(ft.Text("Choisissez un profil :", size=14, color="#555555"))
        
        # Une seule boucle pour tout gérer proprement
            for p in profils:
            # Capturer les données du profil actuel pour les fonctions
                nom_actuel = p["prenom"]
                donnees_p = p

            # Fonction pour sélectionner le profil
                def choisir(e, d=donnees_p):
                    profil["prenom"] = d["prenom"]
                    profil["age"] = d["age"]
                    profil["poids"] = d["poids"]
                    profil["taille"] = d["taille"]
                    profil["activites"] = d.get("activites", [])
                    ecran_choix()

            
                def supprimer_click(e, nom=nom_actuel):
                    
                    liste = charger_profils()
                    nouvelle_liste = [pr for pr in liste if pr["prenom"] != nom]
                    import json
                    with open("profils.json", "w") as f:
                        json.dump(nouvelle_liste, f)
                    ecran_accueil()
                
                    

            
                elements.append(
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text=f"{p['prenom']} — {p['age']} ans, {p['poids']} kg",
                                on_click=choisir,
                                bgcolor=BLEU,
                                color="white",
                                width=300,
                                height=50,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
                            ),
                        ]
                    )
                )
                           

            elements.append(ft.TextButton(
                "+ Créer un nouveau profil",
                on_click=lambda e: ecran_bienvenue(),
                style=ft.ButtonStyle(color=BLEU)
            ))
        
        else:
            elements.append(btn("Ajouter un profil", lambda e: ecran_bienvenue()))

        changer_ecran(ft.Column(
            elements,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True, 
            spacing=12,
        ))

    def ecran_bienvenue():
        prenom = ft.TextField(label="Prénom", border_color=BLEU, focused_border_color=BLEU, width=300)
        age = ft.TextField(label="Âge", border_color=BLEU, focused_border_color=BLEU, width=300)
        poids = ft.TextField(label="Poids (kg)", border_color=BLEU, focused_border_color=BLEU, width=300)
        taille = ft.TextField(label="Taille (cm)", border_color=BLEU, focused_border_color=BLEU, width=300)
        erreur = ft.Text("", color="red")

        def valider(e):
            try:
                profil["prenom"] = prenom.value
                profil["age"] = int(age.value)
                profil["poids"] = float(poids.value)
                profil["taille"] = float(taille.value)
                profil["activites"] = []
                sauvegarder_profil(profil)
                ecran_choix()
            except ValueError:
                erreur.value = "Remplissez bien tous les champs !"
                page.update()

        changer_ecran(ft.Column(
            [
                ft.Row([retour(lambda e: ecran_accueil())]),
                ft.Text("Bienvenue", size=28, weight="bold"),
                ft.Text("Saisissez vos informations", size=14, color="#555555"),
                prenom, age, poids, taille, erreur,
                btn("Valider", valider),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True, spacing=12,
        ))

    def ecran_choix():
        changer_ecran(ft.Column(
            [
                ft.Row([retour(lambda e: ecran_accueil())]),
                ft.Text("Que souhaitez-vous calculer ?", size=20, weight="bold"),
                btn("Métabolisme",  lambda e: ecran_metabolisme()),
                btn("Dépense liée à une activité", lambda e: ecran_activites()),
                ft.Divider(),
                btn("Historique des activités",lambda e: ecran_historique()),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True, spacing=20,
        ))

    def ecran_metabolisme():
        mb = calc_metabolisme(profil["poids"], profil["taille"], profil["age"])
        result = ft.Text("", size=16, color=BLEU, weight="bold")

        facteurs = [ ("Sédentaire", 1.2), ("Légèrement actif", 1.375), ("Modérément actif", 1.55), ("Très actif", 1.725), ("Extrêmement actif", 1.9)]

        def make_cmd(f_val):
            def cmd(e):
                result.value = f"{round(mb * f_val)} kcal / jour"
                page.update()
            return cmd

        boutons_activite = [
            ft.Button(
                nom, on_click=make_cmd(fact),
                bgcolor=BLEU, color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                width=260, height=40,
            )
            for nom, fact in facteurs
        ]

        changer_ecran(ft.Column(
            [
                ft.Row([retour(lambda e: ecran_choix())]),
                ft.Text("Métabolisme", size=24, weight="bold"),
                ft.Text("Métabolisme de base :", size=13, weight="bold"),
                ft.Text(f"{mb} kcal", size=13),
                ft.Divider(),
                ft.Text("Besoin journalier — choisissez votre niveau :", size=13, weight="bold"),
                *boutons_activite,
                result,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True, spacing=8,
        ))

    def ecran_activites():
        changer_ecran(ft.Column(
            [
                ft.Row([retour(lambda e: ecran_choix())]),
                ft.Text("Dépense liée à une activité", size=22, weight="bold"),
                btn("Course", lambda e: ecran_course()),
                btn("Tabata", lambda e: ecran_tabata()),
                btn("Sauna", lambda e: ecran_sauna()),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True, spacing=20,
        ))

    def ecran_course():
        duree = ft.TextField(label="Durée (minutes)", border_color=BLEU, focused_border_color=BLEU, width=300)
        fc = ft.TextField(label="Fréquence cardiaque moyenne", border_color=BLEU, focused_border_color=BLEU, width=300)
        erreur = ft.Text("", color="red")
        result = ft.Text("", size=22, weight="bold", color=BLEU)

        def valider(e):
            try:
                kcal = calc_course(profil["poids"], float(duree.value), float(fc.value))
                result.value = f"{kcal} kcal"
                erreur.value = ""
                ajouter_activite("Course", f"{duree.value} min, FC {fc.value}", kcal)
            except ValueError:
                erreur.value = "Remplissez les deux champs !"
            page.update()

        changer_ecran(ft.Column(
            [
                ft.Row([retour(lambda e: ecran_activites())]),
                ft.Text("Course", size=24, weight="bold"),
                duree, fc, erreur,
                btn("Valider", valider),
                result,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True, spacing=12,
        ))

    def ecran_tabata():
        tours = ft.TextField(label="Nombre de tours (1 tour = 4 min)", border_color=BLEU, focused_border_color=BLEU, width=300)
        erreur = ft.Text("", color="red")
        result = ft.Text("", size=22, weight="bold", color=BLEU)

        def valider(e):
            try:
                kcal = calc_tabata(int(tours.value))
                result.value = f"{kcal} kcal"
                erreur.value = ""
                ajouter_activite("Tabata", f"{tours.value} tours", kcal)
            except ValueError:
                erreur.value = "Entrez un nombre entier !"
            page.update()

        changer_ecran(ft.Column(
            [
                ft.Row([retour(lambda e: ecran_activites())]),
                ft.Text("Tabata", size=24, weight="bold"),
                ft.Text("1 tour = 8 × 20s effort / 10s repos", size=11, color="#888888"),
                tours, erreur,
                btn("Valider", valider),
                result,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True, spacing=12,
        ))

    def ecran_sauna():
        duree = ft.TextField(label="Durée (minutes)", border_color=BLEU, focused_border_color=BLEU, width=300)
        erreur = ft.Text("", color="red")
        result = ft.Text("", size=22, weight="bold", color=BLEU)

        def valider(e):
            try:
                kcal = calc_sauna(profil["poids"], float(duree.value))
                result.value = f"{kcal} kcal"
                erreur.value = ""
                ajouter_activite("Sauna", f"{duree.value} min", kcal)
            except ValueError:
                erreur.value = "Entrez une durée valide !"
            page.update()

        changer_ecran(ft.Column(
            [
                ft.Row([retour(lambda e: ecran_activites())]),
                ft.Text("Sauna", size=24, weight="bold"),
                duree, erreur,
                btn("Valider", valider),
                result,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True, spacing=12,
        ))

    def ecran_historique():
        liste = ft.Column(scroll="auto", spacing=8, expand=True)

        def construire_liste():
            liste.controls.clear()
            if not profil["activites"]:
                liste.controls.append(
                    ft.Text("Aucune activité enregistrée.", color="#888888", size=13)
                )
            else:
                for i, a in enumerate(reversed(profil["activites"])):
                    index_reel = len(profil["activites"]) - 1 - i

                    def supprimer(e, idx=index_reel):
                        profil["activites"].pop(idx)
                        sauvegarder_profil(profil)
                        construire_liste()
                        page.update()

                    ligne = ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(f"{a['type']}  —  {a['kcal']} kcal", size=13, weight="bold"),
                                    ft.Text(f"{a['details']}  ·  {a['date']}", size=11, color="#666666"),
                                ],
                                expand=True, spacing=2,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ROUGE,
                                tooltip="Supprimer",
                                on_click=supprimer,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                    liste.controls.append(ligne)
                    liste.controls.append(ft.Divider(height=1))
            page.update()

        construire_liste()

        changer_ecran(ft.Column(
            [
                ft.Row([retour(lambda e: ecran_choix())]),
                ft.Text("Historique des activités", size=22, weight="bold"),
                ft.Text(f"Profil : {profil['prenom']}", size=13, color="#555555"),
                ft.Divider(),
                liste,
            ],
            expand=True, spacing=10,
        ))

    ecran_accueil()

ft.app(target=main)