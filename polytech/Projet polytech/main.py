from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class PolytechApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        self.add_widget(Label(text="Calculateur de Métabolisme (Mifflin-St Jeor)"))
        
        # Saisie des données
        self.poids = TextInput(hint_text="Poids (kg)", input_filter='float')
        self.add_widget(self.poids)
        
        self.taille = TextInput(hint_text="Taille (cm)", input_filter='float')
        self.add_widget(self.taille)
        
        self.age = TextInput(hint_text="Âge", input_filter='int')
        self.add_widget(self.age)
        
        # Bouton de calcul
        self.btn = Button(text="Calculer mon MB", background_color=(0, 1, 0, 1))
        self.btn.bind(on_press=self.calculer_mb)
        self.add_widget(self.btn)
        
        self.resultat = Label(text="Résultat : -- kcal")
        self.add_widget(self.resultat)

    def calculer_mb(self, instance):
        try:
            p = float(self.poids.text)
            t = float(self.taille.text)
            a = int(self.age.text)
            # Formule pour Femme par défaut (votre groupe est majoritairement féminin)
            mb = (10 * p) + (6.25 * t) - (5 * a) - 161 # [cite: 83]
            self.resultat.text = f"Votre MB est de : {mb:.2f} kcal"
        except:
            self.resultat.text = "Erreur : Remplissez tous les champs"

class MyApp(App):
    def build(self):
        return PolytechApp()

if __name__ == '__main__':
    MyApp().run()