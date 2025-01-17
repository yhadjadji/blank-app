import streamlit as st

# Fonction pour calculer les droits de donation
def calcul_droits_donation(part_taxable):
    bareme = [
        (8072, 0.05),
        (12009 - 8072, 0.10),
        (15932 - 12009, 0.15),
        (552324 - 15932, 0.20),
        (902838 - 552324, 0.30),
        (1805677 - 902838, 0.40),
        (float("inf"), 0.45),
    ]

    droits = 0
    for tranche, taux in bareme:
        if part_taxable > tranche:
            droits += tranche * taux
            part_taxable -= tranche
        else:
            droits += part_taxable * taux
            break

    return droits

# Fonction principale pour calculer la donation et les droits
def calcul_donation(valeur_bien, ages_usufruitiers):
    nb_donateurs = len(ages_usufruitiers)  # Le nombre de donateurs est égal au nombre d'usufruitiers
    abattement_par_donateur = 100000  # Abattement légal fixe par donateur

    # Déterminer le pourcentage moyen d'usufruit selon les âges
    pourcentages_usufruit = []
    for age in ages_usufruitiers:
        if age < 21:
            pourcentage = 90
        elif 21 <= age <= 30:
            pourcentage = 80
        elif 31 <= age <= 40:
            pourcentage = 70
        elif 41 <= age <= 50:
            pourcentage = 60
        elif 51 <= age <= 60:
            pourcentage = 50
        elif 61 <= age <= 70:
            pourcentage = 40
        elif 71 <= age <= 80:
            pourcentage = 30
        elif 81 <= age <= 90:
            pourcentage = 20
        else:
            pourcentage = 10
        pourcentages_usufruit.append(pourcentage)

    pourcentage_usufruit_final = sum(pourcentages_usufruit) / len(ages_usufruitiers)

    # Calcul des valeurs
    valeur_usufruit = (pourcentage_usufruit_final / 100) * valeur_bien
    valeur_nue_propriete = valeur_bien - valeur_usufruit

    # Répartition entre donateurs
    part_par_donateur = valeur_bien / nb_donateurs
    part_taxable = max(0, (part_par_donateur / 2) - abattement_par_donateur)
    droits_donation = calcul_droits_donation(part_taxable)

    return {
        "Pourcentage Usufruit": f"{pourcentage_usufruit_final:.2f}%",
        "Valeur Usufruit (€)": valeur_usufruit,
        "Valeur Nue-Propriété (€)": valeur_nue_propriete,
        "Part par Donateur (€)": part_par_donateur,
        "Part Taxable par Donateur (€)": part_taxable,
        "Droits de Donation par Donateur (€)": droits_donation,
    }

# Interface utilisateur Streamlit
st.set_page_config(page_title="Simulation de Donation", layout="centered")
st.title("💡 Simulation de Donation - Usufruit et Droits by TontonYaya")

# Entrées utilisateur
st.sidebar.header("Paramètres de la simulation")
valeur_bien = st.sidebar.number_input("Valeur totale du bien (€)", min_value=0, value=500000, step=1000)
ages_input = st.sidebar.text_input("Âges des usufruitiers (séparés par des virgules)", "50, 60")

# Conversion des âges en liste
try:
    ages_usufruitiers = [int(age.strip()) for age in ages_input.split(",")]
except ValueError:
    st.error("Veuillez entrer des âges valides, séparés par des virgules.")
    st.stop()

# Calcul des résultats
if st.sidebar.button("Calculer"):
    resultats = calcul_donation(valeur_bien, ages_usufruitiers)

    # Affichage des résultats
    st.subheader("Résultats de la simulation")
    for cle, valeur in resultats.items():
        if "Pourcentage" in cle:
            st.write(f"**{cle} :** {valeur}")
        else:
            st.write(f"**{cle} :** {valeur:,.2f} €")

# Ajouter des éléments de design
st.markdown("---")
st.markdown(
    "<style>div.row-widget.stRadio > div {flex-direction:row;}</style>", unsafe_allow_html=True
)
st.info("Ce calcul est basé sur le barème fiscal français. Consultez un expert pour valider les chiffres.")
