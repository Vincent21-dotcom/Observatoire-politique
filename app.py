
import json
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).parent / "data.json"

st.set_page_config(
    page_title="Observatoire des programmes politiques",
    page_icon="🗳️",
    layout="wide",
)

@st.cache_data
def load_data():
    with DATA_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    propositions = pd.DataFrame(data["propositions"])
    acteurs = pd.DataFrame(data["acteurs"])
    themes = pd.DataFrame(data["themes"])
    sources = pd.DataFrame(data["sources"])
    return data, propositions, acteurs, themes, sources

DATA, PROPOSITIONS, ACTEURS, THEMES, SOURCES = load_data()

def badge_type_source(value):
    mapping = {
        "Programme électoral": "📘",
        "Programme de coalition": "📘",
        "Programme de référence en réactualisation": "🛠️",
        "Position programmatique officielle": "📄",
        "Plan programmatique officiel": "📄",
    }
    return mapping.get(value, "🔎")

def render_proposition(row, show_actor=True):
    with st.container(border=True):
        cols = st.columns([4, 1])
        with cols[0]:
            st.markdown(f"### {row['titre']}")
            if show_actor:
                st.caption(f"🏛️ {row['acteur']} · {row['election_concernee']}")
        with cols[1]:
            st.caption(f"{badge_type_source(row['type_source_position'])} {row['type_source_position']}")
        st.write(row["resume"])
        st.markdown(
            f"**Thème :** {row['theme']}  \n"
            f"**Sous-thème :** {row['sous_theme']}  \n"
            f"**Statut 2027 :** {row['statut_2027']}"
        )
        st.link_button("Voir la source", row["source_url"], use_container_width=False)

def page_accueil():
    st.title("🗳️ Observatoire des programmes et positions politiques")
    st.write(
        "Prototype destiné à explorer, comparer et sourcer des propositions politiques. "
        "Cette première base est volontairement limitée à 30 mesures afin de tester l'architecture."
    )

    st.info(
        "Important : les mesures de 2022 ou 2024 sont conservées comme positions historiques. "
        "Elles ne sont pas automatiquement présentées comme des positions pour 2027."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Propositions", len(PROPOSITIONS))
    c2.metric("Acteurs / coalitions", PROPOSITIONS["acteur"].nunique())
    c3.metric("Thèmes", PROPOSITIONS["theme"].nunique())

    st.subheader("Explorer rapidement")
    recherche = st.text_input(
        "Rechercher dans les propositions",
        placeholder="Ex. retraite, logement, nucléaire, immigration…",
    )

    if recherche:
        mask = (
            PROPOSITIONS["titre"].str.contains(recherche, case=False, na=False)
            | PROPOSITIONS["resume"].str.contains(recherche, case=False, na=False)
            | PROPOSITIONS["theme"].str.contains(recherche, case=False, na=False)
            | PROPOSITIONS["sous_theme"].str.contains(recherche, case=False, na=False)
        )
        resultats = PROPOSITIONS[mask]
        st.caption(f"{len(resultats)} résultat(s)")
        for _, row in resultats.iterrows():
            render_proposition(row)
    else:
        st.subheader("Quelques mesures de la base pilote")
        for _, row in PROPOSITIONS.head(6).iterrows():
            render_proposition(row)

def page_programmes():
    st.title("📚 Programmes")
    st.write("Consulter les mesures enregistrées pour un acteur ou une coalition.")

    acteur = st.selectbox(
        "Choisir un acteur",
        sorted(PROPOSITIONS["acteur"].unique()),
    )

    subset = PROPOSITIONS[PROPOSITIONS["acteur"] == acteur].copy()
    actor_row = ACTEURS[ACTEURS["nom"] == acteur]

    if not actor_row.empty:
        a = actor_row.iloc[0]
        with st.container(border=True):
            st.subheader(a["nom"])
            st.write(a["statut_programmatique_2027"])
            st.link_button("Site officiel / source principale", a["site_officiel"])

    st.caption(f"{len(subset)} mesure(s) dans la base pilote")

    themes = sorted(subset["theme"].unique())
    for theme in themes:
        with st.expander(f"{theme} ({len(subset[subset['theme'] == theme])})", expanded=True):
            for _, row in subset[subset["theme"] == theme].iterrows():
                render_proposition(row, show_actor=False)

def page_themes():
    st.title("🧭 Thèmes")
    st.write(
        "Cette page préfigure les futures fiches thématiques générées automatiquement "
        "à partir de toutes les propositions présentes dans la base."
    )

    theme = st.selectbox(
        "Thème",
        sorted(PROPOSITIONS["theme"].unique()),
    )

    sous_themes = sorted(
        PROPOSITIONS.loc[PROPOSITIONS["theme"] == theme, "sous_theme"].dropna().unique()
    )
    choix_st = st.selectbox(
        "Sous-thème",
        ["Tous les sous-thèmes"] + sous_themes,
    )

    subset = PROPOSITIONS[PROPOSITIONS["theme"] == theme].copy()
    if choix_st != "Tous les sous-thèmes":
        subset = subset[subset["sous_theme"] == choix_st]

    st.subheader(f"{theme}" + (f" → {choix_st}" if choix_st != "Tous les sous-thèmes" else ""))
    st.caption(f"{len(subset)} mesure(s) trouvée(s)")

    acteurs = subset["acteur"].nunique()
    st.write(f"**Acteurs représentés dans la base :** {acteurs}")

    for _, row in subset.sort_values(["acteur", "titre"]).iterrows():
        render_proposition(row)

    st.divider()
    st.caption(
        "À terme, cette page contiendra aussi une synthèse automatique neutre, "
        "l'historique des positions et toutes les sources associées."
    )

def page_comparer():
    st.title("⚖️ Comparer")
    st.write("Comparer plusieurs acteurs sur un même thème ou sous-thème, sans notation ni classement.")

    acteurs_dispo = sorted(PROPOSITIONS["acteur"].unique())
    acteurs = st.multiselect(
        "Acteurs à comparer",
        acteurs_dispo,
        default=acteurs_dispo,
    )

    theme = st.selectbox(
        "Thème",
        sorted(PROPOSITIONS["theme"].unique()),
    )

    st_values = sorted(
        PROPOSITIONS.loc[PROPOSITIONS["theme"] == theme, "sous_theme"].dropna().unique()
    )
    sous_theme = st.selectbox(
        "Sous-thème",
        ["Tous les sous-thèmes"] + st_values,
    )

    subset = PROPOSITIONS[
        PROPOSITIONS["acteur"].isin(acteurs)
        & (PROPOSITIONS["theme"] == theme)
    ].copy()

    if sous_theme != "Tous les sous-thèmes":
        subset = subset[subset["sous_theme"] == sous_theme]

    if subset.empty:
        st.warning("Aucune proposition de la base pilote ne correspond à cette sélection.")
        return

    cols = st.columns(max(1, len(acteurs)))
    for idx, acteur in enumerate(acteurs):
        actor_subset = subset[subset["acteur"] == acteur]
        with cols[idx]:
            st.subheader(acteur)
            if actor_subset.empty:
                st.caption("Aucune mesure enregistrée dans la base pilote.")
            else:
                for _, row in actor_subset.iterrows():
                    render_proposition(row, show_actor=False)

def page_sources():
    st.title("🔗 Sources & méthodologie")
    st.write(
        "La V1 privilégie les sources officielles et conserve explicitement "
        "l'élection et la version du programme auxquelles une mesure se rattache."
    )

    st.subheader("Sources enregistrées")
    display = SOURCES[["titre", "type_source", "organisme", "annee", "url"]].copy()
    st.dataframe(
        display,
        hide_index=True,
        use_container_width=True,
        column_config={
            "url": st.column_config.LinkColumn("Lien"),
            "titre": "Source",
            "type_source": "Type",
            "organisme": "Organisme",
            "annee": "Année",
        },
    )

    st.subheader("Principes du prototype")
    st.markdown(
        """
- aucune mesure sans source identifiable ;
- distinction entre acteur, coalition et personnalité ;
- distinction entre programme historique et programme 2027 ;
- thème → sous-thème ;
- pas de note, de classement ni de recommandation politique ;
- les évolutions et doublons seront ajoutés dans une prochaine version ;
- les futures mises à jour automatiques passeront par une zone de validation.
        """
    )

# Navigation moderne Streamlit
pages = {
    "Explorer": [
        st.Page(page_accueil, title="Accueil", icon="🏠", default=True),
        st.Page(page_programmes, title="Programmes", icon="📚"),
        st.Page(page_themes, title="Thèmes", icon="🧭"),
        st.Page(page_comparer, title="Comparer", icon="⚖️"),
    ],
    "Références": [
        st.Page(page_sources, title="Sources & méthodologie", icon="🔗"),
    ],
}

pg = st.navigation(pages)
pg.run()
