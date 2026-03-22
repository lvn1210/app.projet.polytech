import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Simulateur Énergétique Polytech", layout="wide")

st.title("📊 Simulateur de Dépense et Besoin Énergétique")
st.write("Projet Biométrie et Santé - Groupe : Livane, Clara D, Clara V, Emie, Eloïse")

# --- ZONE A : PROFIL BIOMÉTRIQUE ---
st.sidebar.header("👤 Profil de l'individu")
sexe = st.sidebar.selectbox("Sexe", ["Femme", "Homme"])
poids = st.sidebar.number_input("Poids (kg)", value=60.0)
taille = st.sidebar.number_input("Taille (cm)", value=165.0)
age = st.sidebar.number_input("Âge", value=20)

# Calcul du MB (Formule Mifflin-St Jeor) [cite: 82, 83]
if sexe == "Homme":
    mb = (10 * poids) + (6.25 * taille) - (5 * age) + 5
else:
    mb = (10 * poids) + (6.25 * taille) - (5 * age) - 161

dej_repos = mb * 1.2 # [cite: 78]

# --- ZONE B : CALCULS DES ACTIVITÉS ---
st.header("🏃 Choix de l'activité physique")
tab1, tab2, tab3 = st.tabs(["Course à pied", "Tabata", "Sauna"])

with tab1:
    st.subheader("Analyse de la Course")
    methode_course = st.radio("Méthode de calcul", ["Fréquence Cardiaque", "Vitesse (VO2)"])
    duree_course = st.number_input("Durée (min)", value=30)
    
    if methode_course == "Fréquence Cardiaque":
        fc_moy = st.number_input("FC moyenne (bpm)", value=150)
        # Formule simplifiée citée dans votre document [cite: 106]
        depense_course = ((-20.4022 + (0.4472 * fc_moy) - (0.1263 * poids) + (0.074 * age)) / 4.184) * duree_course
    else:
        vitesse = st.number_input("Vitesse (km/h)", value=8.0)
        # Logique VO2 relative -> absolue -> kcal [cite: 90, 93]
        depense_course = (vitesse * 3.5) * poids / 200 * duree_course # Approximation standard

with tab2:
    st.subheader("Analyse Tabata (Haute Intensité)")
    st.info("Le Tabata est estimé à 12 MET [cite: 114]")
    # Formule MET : MET * Poids * Durée(h) * 1.05 [cite: 109]
    depense_tabata = 12 * poids * (11/60) * 1.05

with tab3:
    st.subheader("Analyse Sauna (Thermodynamique)")
    delta_t = st.number_input("Variation de température corporelle (°C)", value=1.5)
    masse_perdue = st.number_input("Masse d'eau perdue (kg)", value=0.5)
    
    # Q = m*c*dT + m_perdue*Lv [cite: 123, 128]
    q_abs = poids * 3.5 * delta_t # 3.5 kJ/kg.K est une constante bio plus précise
    q_evap = masse_perdue * 2260
    depense_sauna = (q_abs + q_evap) / 4.184 # Conversion kJ en kcal [cite: 130]

# --- ZONE C : RÉSULTATS ET SYNTHÈSE ---
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.metric("Métabolisme de Base (MB)", f"{mb:.0f} kcal")
    st.metric("Dépense au Repos (DEJ)", f"{dej_repos:.0f} kcal")

with col2:
    activite_choisie = st.selectbox("Sélectionnez l'activité réalisée pour le bilan", ["Aucune", "Course", "Tabata", "Sauna"])
    extra = 0
    if activite_choisie == "Course": extra = depense_course
    if activite_choisie == "Tabata": extra = depense_tabata
    if activite_choisie == "Sauna": extra = depense_sauna
    
    besoin_total = (dej_repos + extra) * 1.1 # Inclusion thermogénèse [cite: 138]
    st.metric("Besoin Énergétique Total (BEJ)", f"{besoin_total:.0f} kcal")

# --- ZONE D : ANALYSE DES ÉCARTS ---
st.header("⚠️ Analyse de la fiabilité")
montre_kcal = st.number_input("Calories affichées par la montre connectée", value=besoin_total)
ecart = abs((montre_kcal - besoin_total) / besoin_total) * 100
st.warning(f"L'écart entre le modèle théorique et la montre est de {ecart:.1f}% [cite: 166]")