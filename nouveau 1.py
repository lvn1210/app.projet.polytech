import flet as ft

def main(page: ft.Page):
    page.title = "Sport & Santé"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 800
    
    # Stockage des informations
    user = {"nom": "", "age": 0, "poids": 0.0, "taille": 0.0, "mb": 0.0}
    

def main(page: ft.Page):
    page.add(ft.ElevatedButton("Si tu vois ce bouton, l'app marche !"))
    page.update()

ft.app(target=main)

    def navigation(route):
        page.views.clear()
        
        # PAGE 1 & 2 : ACCUEIL ET PROFIL [cite: 60, 62]
        if page.route == "/":
            nom_in = ft.TextField(label="Prénom")
            age_in = ft.TextField(label="Age", keyboard_type="number")
            poids_in = ft.TextField(label="Poids (en kg)", keyboard_type="number")
            taille_in = ft.TextField(label="Taille (en cm)", keyboard_type="number")

            def valider_profil(e):
                user["nom"] = nom_in.value
                user["age"] = int(age_in.value)
                user["poids"] = float(poids_in.value)
                user["taille"] = float(taille_in.value)
                # Formule de Mifflin-St Jeor (Femme)
                user["mb"] = (10 * user["poids"]) + (6.25 * user["taille"]) - (5 * user["age"]) - 161
                page.go("/choix")

            page.views.append(ft.View("/", [
                ft.Text("BIENVENUE", size=30, weight="bold"),
                ft.Text("Saisissez vos informations"),
                nom_in, age_in, poids_in, taille_in,
                ft.ElevatedButton("Valider", on_click=valider_profil, bgcolor="blue", color="white")
            ], horizontal_alignment="center"))

        # PAGE 3 : MENU DE SÉLECTION [cite: 70]
        elif page.route == "/choix":
            page.views.append(ft.View("/choix", [
                ft.Text("QUE SOUHAITEZ-VOUS CALCULER?", text_align="center", weight="bold"),
                ft.ElevatedButton("Métabolisme", on_click=lambda _: page.go("/metabolisme"), width=250),
                ft.ElevatedButton("Dépense liée à une activité", on_click=lambda _: page.go("/activite_menu"), width=250),
                ft.TextButton("Retour", on_click=lambda _: page.go("/"))
            ], horizontal_alignment="center", vertical_alignment="center"))
			
		page.update()

    page.on_route_change = navigation # Connecte la logique
    page.go("/")                      # Force l'affichage de la première page

# Correction de l'erreur TypeError
ft.app(target=main)