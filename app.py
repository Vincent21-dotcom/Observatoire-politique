
import csv
import html
import io
import json
import math
import re
import unicodedata
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

APP_DIR = Path(__file__).parent
DATA_PATH = APP_DIR / "data.json"

st.set_page_config(
    page_title="Observatoire politique",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
<style>
:root {
    --bg: #090b0e;
    --panel: #101419;
    --panel2: #141920;
    --panel3: #181e26;
    --line: #262e39;
    --text: #f3f5f7;
    --muted: #98a3af;
    --soft: #cdd3da;
    --accent: #9ec5ff;
    --accent2: #d9e8ff;
    --good: #b6f2ce;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: #0c0f13;
    border-right: 1px solid var(--line);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.35rem;
    padding-bottom: 2.4rem;
}

h1 {
    font-size: 2.1rem !important;
    letter-spacing: -0.035em;
    margin-bottom: 0.1rem !important;
}

h2, h3 {
    letter-spacing: -0.02em;
}

a {
    color: var(--accent2);
}

.hero {
    background:
        radial-gradient(circle at 82% 20%, rgba(158,197,255,.10), transparent 24%),
        linear-gradient(135deg, #121720 0%, #0d1116 58%, #121820 100%);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 1.05rem 1.25rem;
    margin-bottom: .85rem;
}

.hero-kicker {
    color: var(--accent);
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .13em;
    text-transform: uppercase;
}

.hero-title {
    font-size: 2rem;
    line-height: 1.05;
    font-weight: 800;
    margin: .22rem 0 .35rem;
    letter-spacing: -.035em;
}

.hero-sub {
    color: var(--muted);
    margin: 0;
    max-width: 950px;
    line-height: 1.45;
}

.notice {
    border: 1px solid var(--line);
    background: var(--panel);
    border-radius: 12px;
    padding: .7rem .85rem;
    color: var(--soft);
    font-size: .86rem;
    margin: .45rem 0 .75rem;
}

.card {
    border: 1px solid var(--line);
    border-radius: 12px;
    background: var(--panel);
    padding: .64rem .8rem;
    margin: .34rem 0;
}

.card:hover {
    border-color: #354254;
}

.card-title {
    color: var(--text);
    font-weight: 750;
    font-size: .97rem;
    line-height: 1.25;
    margin-bottom: .22rem;
}

.meta {
    color: var(--muted);
    font-size: .74rem;
    line-height: 1.35;
}

.summary {
    color: #d9dee5;
    font-size: .86rem;
    line-height: 1.42;
    margin: .34rem 0 .28rem;
}

.badge {
    display: inline-block;
    border: 1px solid #334052;
    background: #17202b;
    color: #d4e4ff;
    border-radius: 999px;
    padding: .09rem .39rem;
    margin: .08rem .18rem .05rem 0;
    font-size: .65rem;
    font-weight: 700;
    line-height: 1.35;
}

.badge-muted {
    display: inline-block;
    border: 1px solid var(--line);
    background: #12161c;
    color: var(--muted);
    border-radius: 999px;
    padding: .09rem .39rem;
    margin: .08rem .18rem .05rem 0;
    font-size: .65rem;
    font-weight: 650;
}

.src a {
    color: var(--accent2) !important;
    text-decoration: none;
    font-size: .74rem;
    font-weight: 700;
}

.src a:hover {
    text-decoration: underline;
}

.section-head {
    color: var(--muted);
    font-size: .72rem;
    letter-spacing: .08em;
    text-transform: uppercase;
    font-weight: 800;
    margin-top: .3rem;
}

.mini-box {
    border: 1px solid var(--line);
    background: var(--panel);
    border-radius: 12px;
    padding: .7rem .8rem;
    min-height: 82px;
}

.mini-title {
    font-size: .77rem;
    color: var(--muted);
    margin-bottom: .15rem;
}

.mini-value {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text);
}

.flow {
    display: flex;
    gap: .45rem;
    align-items: stretch;
    flex-wrap: wrap;
    margin: .55rem 0 1rem;
}

.flow-step {
    flex: 1 1 140px;
    min-width: 140px;
    border: 1px solid var(--line);
    background: var(--panel);
    border-radius: 12px;
    padding: .65rem .75rem;
}

.flow-step b {
    display:block;
    color: var(--text);
    margin-bottom:.15rem;
}

.flow-step span {
    color: var(--muted);
    font-size:.76rem;
}

div[data-testid="stMetric"] {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: .45rem .65rem;
}

div[data-testid="stMetricValue"] {
    font-size: 1.35rem;
}

div[data-testid="stMetricLabel"] {
    color: var(--muted);
}

div[data-testid="stExpander"] {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 11px;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
}

div.stButton > button,
div.stDownloadButton > button {
    border-color: var(--line);
}

hr {
    border-color: var(--line) !important;
}

.small-note {
    color: var(--muted);
    font-size: .74rem;
}

@media (max-width: 800px) {
    .block-container {
        padding-left: .8rem;
        padding-right: .8rem;
    }
    .hero {
        padding: .9rem;
    }
    .hero-title {
        font-size: 1.65rem;
    }
    .card {
        padding: .6rem .68rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DONNÉES
# ============================================================

@st.cache_data
def load_data():
    with DATA_PATH.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    propositions = pd.DataFrame(raw.get("propositions", []))
    acteurs = pd.DataFrame(raw.get("acteurs", []))
    themes = pd.DataFrame(raw.get("themes", []))
    sources = pd.DataFrame(raw.get("sources", []))
    meta = raw.get("meta", {})

    if not propositions.empty:
        propositions["annee_num"] = pd.to_numeric(
            propositions.get("annee_source"), errors="coerce"
        )
    return raw, propositions, acteurs, themes, sources, meta


RAW, P, ACTEURS, THEMES, SOURCES, META = load_data()


SOURCE_LABELS = {
    "Programme électoral": "Programme officiel",
    "Programme de coalition": "Programme officiel de coalition",
    "Programme de référence en réactualisation": "Programme de référence en mise à jour",
    "Position programmatique officielle": "Position programmatique officielle",
    "Plan programmatique officiel": "Plan programmatique officiel",
}


def source_label(value):
    return SOURCE_LABELS.get(str(value), str(value))


def esc(value):
    return html.escape("" if value is None else str(value), quote=True)


def normalize_text(value):
    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.casefold()


def contains_query(df, query, columns):
    if not query:
        return pd.Series(True, index=df.index)
    q = normalize_text(query)
    result = pd.Series(False, index=df.index)
    for col in columns:
        if col in df.columns:
            result |= df[col].fillna("").map(normalize_text).str.contains(
                re.escape(q), regex=True
            )
    return result


def actor_options():
    if P.empty:
        return ["Tous les acteurs politiques"]
    return ["Tous les acteurs politiques"] + sorted(P["acteur"].dropna().unique().tolist())


def actor_filter(label="Acteur politique", key=None):
    return st.selectbox(label, actor_options(), key=key)


def apply_actor(df, actor):
    if actor == "Tous les acteurs politiques":
        return df
    return df[df["acteur"] == actor]


def csv_bytes(df):
    export_cols = [
        c
        for c in [
            "acteur",
            "election_concernee",
            "theme",
            "sous_theme",
            "titre",
            "resume",
            "type_source_position",
            "statut_2027",
            "source_titre",
            "source_url",
            "annee_source",
        ]
        if c in df.columns
    ]
    return df[export_cols].to_csv(index=False).encode("utf-8-sig")


def unique_sorted(df, col):
    if col not in df.columns:
        return []
    return sorted(df[col].dropna().astype(str).unique().tolist())


# ============================================================
# COMPOSANTS
# ============================================================

def page_header(title, subtitle):
    st.title(title)
    st.caption(subtitle)


def compact_card(row, show_actor=True, show_details=True):
    actor_text = f"{esc(row.get('acteur'))} · " if show_actor else ""
    source_type = source_label(row.get("type_source_position", "Source"))
    url = esc(row.get("source_url", ""))
    source_title = esc(row.get("source_titre", "Consulter la source"))
    year = esc(row.get("annee_source", ""))
    election = esc(row.get("election_concernee", ""))
    theme = esc(row.get("theme", ""))
    subtheme = esc(row.get("sous_theme", ""))

    st.markdown(
        f"""
<div class="card">
  <div class="card-title">{esc(row.get("titre", ""))}</div>
  <div class="meta">{actor_text}{theme} → {subtheme} · {election}</div>
  <div class="summary">{esc(row.get("resume", ""))}</div>
  <div>
    <span class="badge">{esc(source_type)}</span>
    <span class="badge-muted">{year}</span>
    <span class="src">↗ <a href="{url}" target="_blank" rel="noopener noreferrer">{source_title}</a></span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if show_details:
        with st.expander("Détails et traçabilité", expanded=False):
            st.markdown(f"**Acteur :** {row.get('acteur', '')}")
            st.markdown(f"**Corpus / version :** {row.get('version_programme', '')}")
            st.markdown(f"**Statut pour 2027 :** {row.get('statut_2027', '')}")
            st.markdown(f"**Validation :** {row.get('validation', '')}")
            st.link_button(
                "Ouvrir la source",
                str(row.get("source_url", "")),
                use_container_width=False,
            )


def compact_metrics(df):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Propositions", len(df))
    c2.metric("Acteurs / coalitions", df["acteur"].nunique() if not df.empty else 0)
    c3.metric("Thèmes", df["theme"].nunique() if not df.empty else 0)
    c4.metric(
        "Sources distinctes",
        df["source_url"].nunique() if "source_url" in df.columns and not df.empty else 0,
    )


def base_warning():
    st.markdown(
        """
<div class="notice">
<strong>Base pilote non exhaustive.</strong>
Une absence de proposition dans cette application signifie uniquement qu'aucune proposition correspondante
n'est encore enregistrée dans la base. Elle ne permet pas de conclure qu'un acteur politique n'a pas de position.
</div>
""",
        unsafe_allow_html=True,
    )


def filters_programmes():
    top1, top2, top3 = st.columns([1.15, 1, 1])
    with top1:
        actor = actor_filter("Acteur politique", "program_actor")
    with top2:
        theme = st.selectbox(
            "Thème",
            ["Tous les thèmes"] + unique_sorted(P, "theme"),
            key="program_theme",
        )
    theme_df = P if theme == "Tous les thèmes" else P[P["theme"] == theme]
    with top3:
        subtheme = st.selectbox(
            "Sous-thème",
            ["Tous les sous-thèmes"] + unique_sorted(theme_df, "sous_theme"),
            key="program_subtheme",
        )

    q = st.text_input(
        "Recherche dans les propositions",
        placeholder="Ex. retraite, hôpital, immigration, TVA, nucléaire…",
        key="program_search",
    )

    with st.expander("Filtres avancés", expanded=False):
        a, b, c = st.columns(3)
        with a:
            source_type = st.selectbox(
                "Nature de la source",
                ["Toutes les natures"] + unique_sorted(P, "type_source_position"),
                key="program_source_type",
            )
        with b:
            election = st.selectbox(
                "Élection / corpus",
                ["Tous les corpus"] + unique_sorted(P, "election_concernee"),
                key="program_election",
            )
        with c:
            year = st.selectbox(
                "Année de la source",
                ["Toutes les années"] + unique_sorted(P, "annee_source"),
                key="program_year",
            )

    return actor, theme, subtheme, q, source_type, election, year


def apply_program_filters(df, values):
    actor, theme, subtheme, q, source_type, election, year = values
    out = apply_actor(df.copy(), actor)

    if theme != "Tous les thèmes":
        out = out[out["theme"] == theme]
    if subtheme != "Tous les sous-thèmes":
        out = out[out["sous_theme"] == subtheme]
    if source_type != "Toutes les natures":
        out = out[out["type_source_position"] == source_type]
    if election != "Tous les corpus":
        out = out[out["election_concernee"] == election]
    if year != "Toutes les années":
        out = out[out["annee_source"].astype(str) == str(year)]

    mask = contains_query(
        out,
        q,
        ["titre", "resume", "theme", "sous_theme", "acteur", "source_titre"],
    )
    return out[mask]


def sort_df(df, mode):
    if df.empty:
        return df
    if mode == "Année de source — récente d'abord":
        return df.sort_values(["annee_num", "acteur", "theme"], ascending=[False, True, True])
    if mode == "Année de source — ancienne d'abord":
        return df.sort_values(["annee_num", "acteur", "theme"], ascending=[True, True, True])
    if mode == "Acteur politique":
        return df.sort_values(["acteur", "theme", "titre"])
    if mode == "Thème":
        return df.sort_values(["theme", "sous_theme", "acteur"])
    return df


def data_checks():
    checks = {}

    checks["Identifiants de propositions dupliqués"] = (
        int(P["id_proposition"].duplicated().sum())
        if "id_proposition" in P.columns
        else 0
    )

    checks["Propositions sans URL de source"] = (
        int(P["source_url"].fillna("").eq("").sum())
        if "source_url" in P.columns
        else len(P)
    )

    checks["Propositions sans année de source"] = (
        int(P["annee_source"].fillna("").eq("").sum())
        if "annee_source" in P.columns
        else len(P)
    )

    checks["Propositions sans statut de validation"] = (
        int(P["validation"].fillna("").eq("").sum())
        if "validation" in P.columns
        else len(P)
    )

    if {"acteur", "titre"}.issubset(P.columns):
        checks["Couples acteur + titre dupliqués"] = int(
            P.duplicated(subset=["acteur", "titre"]).sum()
        )
    else:
        checks["Couples acteur + titre dupliqués"] = 0

    return checks


# ============================================================
# PAGES
# ============================================================

def page_home():
    st.markdown(
        """
<div class="hero">
  <div class="hero-kicker">Observatoire sourcé · V2</div>
  <div class="hero-title">Programmes et positions politiques</div>
  <p class="hero-sub">
    Explorer, comparer et suivre des propositions politiques à partir de sources identifiées,
    avec une distinction explicite entre programmes historiques, corpus actuels et futures évolutions.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    actor = actor_filter("Afficher", "home_actor")
    df = apply_actor(P.copy(), actor)

    compact_metrics(df)

    q = st.text_input(
        "Rechercher dans la base",
        placeholder="Ex. retraites, santé, logement, Europe…",
        key="home_search",
    )

    if q:
        df = df[
            contains_query(
                df,
                q,
                ["titre", "resume", "theme", "sous_theme", "acteur", "source_titre"],
            )
        ]

    base_warning()

    left, right = st.columns([1.55, 1])

    with left:
        st.subheader("Explorer les propositions")
        st.caption(f"{len(df)} résultat(s) dans la sélection actuelle")
        for _, row in df.head(7).iterrows():
            compact_card(row, show_actor=(actor == "Tous les acteurs politiques"))
        if len(df) > 7:
            st.caption("Les 7 premiers résultats sont affichés ici. La page Programmes donne accès à l'ensemble de la base.")

    with right:
        st.subheader("Répartition de la base")
        if not df.empty:
            chart = (
                df["theme"]
                .value_counts()
                .head(10)
                .rename_axis("Thème")
                .to_frame("Propositions")
            )
            st.bar_chart(chart, height=300)
            st.caption(
                "Nombre de propositions enregistrées par thème. Ce graphique décrit la base, "
                "pas l'importance politique accordée à chaque sujet."
            )

        st.subheader("Repères")
        st.markdown(
            f"""
<div class="mini-box">
  <div class="mini-title">Version de la base</div>
  <div class="mini-value">{esc(META.get("version", "pilote"))}</div>
  <div class="small-note">Créée le {esc(META.get("date_creation", "—"))}</div>
</div>
""",
            unsafe_allow_html=True,
        )


def page_programmes():
    page_header(
        "Programmes",
        "Recherche multicritère dans toutes les propositions actuellement enregistrées.",
    )

    values = filters_programmes()
    df = apply_program_filters(P, values)

    tool1, tool2, tool3 = st.columns([1.2, 1, 1])
    with tool1:
        sort_mode = st.selectbox(
            "Trier",
            [
                "Année de source — récente d'abord",
                "Année de source — ancienne d'abord",
                "Acteur politique",
                "Thème",
            ],
            key="program_sort",
        )
    with tool2:
        page_size = st.selectbox("Résultats par page", [10, 25, 50, 100], index=1)
    with tool3:
        st.download_button(
            "Exporter les résultats en CSV",
            data=csv_bytes(df),
            file_name="observatoire_resultats_filtres.csv",
            mime="text/csv",
            use_container_width=True,
        )

    df = sort_df(df, sort_mode)
    st.caption(f"{len(df)} proposition(s) correspondant aux filtres")

    if df.empty:
        st.warning(
            "Aucun résultat n'est enregistré dans la base pour cette sélection. "
            "Cela ne signifie pas qu'aucune position politique n'existe."
        )
        return

    total_pages = max(1, math.ceil(len(df) / page_size))
    if total_pages > 1:
        page_number = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
        )
    else:
        page_number = 1

    start = (int(page_number) - 1) * page_size
    end = start + page_size
    current = df.iloc[start:end]

    # Accordéons fermés par défaut.
    for theme_name in current["theme"].dropna().unique():
        part = current[current["theme"] == theme_name]
        with st.expander(f"{theme_name} · {len(part)}", expanded=False):
            for _, row in part.iterrows():
                compact_card(
                    row,
                    show_actor=(values[0] == "Tous les acteurs politiques"),
                    show_details=True,
                )

    if total_pages > 1:
        st.caption(f"Page {int(page_number)} sur {total_pages}")


def page_themes():
    page_header(
        "Fiches thématiques",
        "Comparer ce qui est actuellement documenté sur un même sujet, sans déduire de position absente.",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        actor = actor_filter("Acteur politique", "themes_actor")
    with c2:
        theme = st.selectbox(
            "Thème",
            ["Tous les thèmes"] + unique_sorted(P, "theme"),
            key="themes_theme",
        )

    theme_df = P if theme == "Tous les thèmes" else P[P["theme"] == theme]
    with c3:
        subtheme = st.selectbox(
            "Sous-thème",
            ["Tous les sous-thèmes"] + unique_sorted(theme_df, "sous_theme"),
            key="themes_subtheme",
        )

    df = apply_actor(theme_df.copy(), actor)
    if subtheme != "Tous les sous-thèmes":
        df = df[df["sous_theme"] == subtheme]

    compact_metrics(df)

    if df.empty:
        st.warning(
            "Aucune proposition n'est enregistrée pour cette sélection. "
            "L'absence de résultat ne permet pas de conclure à une absence de position."
        )
        return

    if theme == "Tous les thèmes":
        groups = sorted(df["theme"].dropna().unique())
    else:
        groups = [theme]

    for theme_name in groups:
        subset = df[df["theme"] == theme_name]
        st.subheader(theme_name)
        by_actor = subset.groupby("acteur", sort=True)

        for actor_name, actor_df in by_actor:
            with st.expander(f"{actor_name} · {len(actor_df)} proposition(s)", expanded=False):
                for _, row in actor_df.iterrows():
                    compact_card(row, show_actor=False)

    st.caption(
        "Les fiches sont générées directement à partir des propositions et de leurs sources enregistrées dans la base."
    )


def page_actors():
    page_header(
        "Acteurs politiques",
        "Voir le corpus actuellement associé à chaque parti ou coalition dans la base.",
    )

    actor = actor_filter("Acteur politique", "actors_actor")
    selected = ACTEURS.copy()

    if actor != "Tous les acteurs politiques":
        selected = selected[selected["nom"] == actor]

    for _, ar in selected.iterrows():
        name = ar.get("nom", "")
        actor_df = P[P["acteur"] == name]

        st.subheader(name)
        cols = st.columns([1.6, 1])
        with cols[0]:
            st.markdown(f"**Type :** {ar.get('type', '')}")
            st.markdown(
                f"**Statut programmatique dans la base :** {ar.get('statut_programmatique_2027', '')}"
            )
            st.link_button("Site officiel", str(ar.get("site_officiel", "")))
        with cols[1]:
            st.metric("Propositions enregistrées", len(actor_df))
            st.metric("Thèmes documentés", actor_df["theme"].nunique())

        if not actor_df.empty:
            chart = (
                actor_df["theme"]
                .value_counts()
                .head(10)
                .rename_axis("Thème")
                .to_frame("Propositions")
            )
            st.bar_chart(chart, height=220)
            st.caption(
                "Répartition des propositions présentes dans la base pour cet acteur ; "
                "ce n'est pas une mesure de priorité politique."
            )
        st.divider()


def page_compare():
    page_header(
        "Comparer",
        "Mettre côte à côte les propositions enregistrées sur un même sujet, sans score ni classement.",
    )

    all_actors = sorted(P["acteur"].dropna().unique().tolist())

    mode = st.selectbox(
        "Périmètre des acteurs",
        ["Tous les acteurs politiques", "Sélection personnalisée"],
        key="compare_mode",
    )

    if mode == "Tous les acteurs politiques":
        selected_actors = all_actors
    else:
        selected_actors = st.multiselect(
            "Acteurs à comparer",
            all_actors,
            default=all_actors[: min(3, len(all_actors))],
            key="compare_actors",
        )

    c1, c2 = st.columns(2)
    with c1:
        theme = st.selectbox(
            "Thème",
            unique_sorted(P, "theme"),
            key="compare_theme",
        )
    relevant = P[P["theme"] == theme]
    with c2:
        subtheme = st.selectbox(
            "Sous-thème",
            ["Tous les sous-thèmes"] + unique_sorted(relevant, "sous_theme"),
            key="compare_subtheme",
        )

    if not selected_actors:
        st.info("Sélectionnez au moins un acteur.")
        return

    df = P[
        (P["acteur"].isin(selected_actors))
        & (P["theme"] == theme)
    ].copy()
    if subtheme != "Tous les sous-thèmes":
        df = df[df["sous_theme"] == subtheme]

    # Jusqu'à 3 acteurs : comparaison directe en colonnes.
    if len(selected_actors) <= 3:
        columns = st.columns(len(selected_actors))
        for i, actor_name in enumerate(selected_actors):
            with columns[i]:
                st.subheader(actor_name)
                actor_df = df[df["acteur"] == actor_name]
                if actor_df.empty:
                    st.caption(
                        "Aucune proposition enregistrée dans la base pour cette sélection."
                    )
                for _, row in actor_df.iterrows():
                    compact_card(row, show_actor=False)
    else:
        # Au-delà : onglets plus lisibles et adaptés au mobile.
        tabs = st.tabs(selected_actors)
        for tab, actor_name in zip(tabs, selected_actors):
            with tab:
                actor_df = df[df["acteur"] == actor_name]
                if actor_df.empty:
                    st.caption(
                        "Aucune proposition enregistrée dans la base pour cette sélection."
                    )
                for _, row in actor_df.iterrows():
                    compact_card(row, show_actor=False)

    st.caption(
        "Une cellule vide ou un onglet vide signifie uniquement qu'aucune proposition correspondante n'est enregistrée dans la base."
    )


def page_evolutions():
    page_header(
        "Évolutions",
        "Séparer clairement la chronologie documentaire des véritables changements de position.",
    )

    c1, c2 = st.columns(2)
    with c1:
        actor = actor_filter("Acteur politique", "evol_actor")
    with c2:
        theme = st.selectbox(
            "Thème",
            ["Tous les thèmes"] + unique_sorted(P, "theme"),
            key="evol_theme",
        )

    df = apply_actor(P.copy(), actor)
    if theme != "Tous les thèmes":
        df = df[df["theme"] == theme]

    st.markdown(
        """
<div class="notice">
<strong>Principe méthodologique :</strong>
la présence de documents de plusieurs années ne suffit pas à prouver qu'une position a changé.
La V2 affiche donc une <strong>chronologie documentaire</strong>, mais ne qualifie une évolution
que lorsqu'un lien ancien → nouveau aura été documenté et validé.
</div>
""",
        unsafe_allow_html=True,
    )

    if df.empty:
        st.info("Aucun document correspondant n'est enregistré.")
        return

    chronology = (
        df.groupby(["annee_source", "acteur"], dropna=False)
        .size()
        .reset_index(name="Propositions documentées")
        .sort_values(["annee_source", "acteur"])
    )

    st.subheader("Chronologie documentaire")
    st.dataframe(
        chronology,
        hide_index=True,
        use_container_width=True,
    )

    st.subheader("Documents et propositions")
    for _, row in df.sort_values(["annee_num", "acteur", "theme"]).iterrows():
        compact_card(row, show_actor=True)

    st.info(
        "Aucune évolution de fond n'est encore publiée automatiquement dans la base pilote. "
        "Cette fonction sera alimentée par des liens entre positions anciennes et nouvelles validés humainement."
    )


def page_sources():
    page_header(
        "Sources & données",
        "Consulter les sources, mesurer la couverture de la base et contrôler son intégrité technique.",
    )

    actor = actor_filter("Acteur politique", "sources_actor")
    df = apply_actor(P.copy(), actor)

    st.subheader("Référentiel des sources")
    source_urls = set(df["source_url"].dropna().tolist())
    source_df = SOURCES[SOURCES["url"].isin(source_urls)].copy()

    if source_df.empty:
        st.info("Aucune source enregistrée pour cette sélection.")
    else:
        st.dataframe(
            source_df[["titre", "type_source", "organisme", "annee", "url"]],
            hide_index=True,
            use_container_width=True,
            column_config={
                "titre": "Source",
                "type_source": "Nature",
                "organisme": "Organisme",
                "annee": "Année",
                "url": st.column_config.LinkColumn(
                    "Lien",
                    display_text="Ouvrir ↗",
                ),
            },
        )
        st.download_button(
            "Exporter le référentiel des sources",
            data=source_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="observatoire_sources.csv",
            mime="text/csv",
        )

    st.subheader("Couverture de la base")
    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            actor_counts = (
                df["acteur"]
                .value_counts()
                .rename_axis("Acteur")
                .to_frame("Propositions")
            )
            st.bar_chart(actor_counts, height=280)
            st.caption("Nombre de propositions enregistrées par acteur.")
        with c2:
            type_counts = (
                df["type_source_position"]
                .map(source_label)
                .value_counts()
                .rename_axis("Nature")
                .to_frame("Propositions")
            )
            st.bar_chart(type_counts, height=280)
            st.caption("Répartition par nature de source.")

        pivot = pd.pivot_table(
            df,
            index="theme",
            columns="acteur",
            values="id_proposition",
            aggfunc="count",
            fill_value=0,
        )
        st.markdown("**Matrice de couverture thème × acteur**")
        st.dataframe(pivot, use_container_width=True)
        st.caption(
            "Cette matrice montre uniquement ce qui est présent dans la base ; elle ne mesure ni la qualité ni l'importance d'un programme."
        )

    st.subheader("Contrôles d'intégrité")
    checks = data_checks()
    c1, c2, c3 = st.columns(3)
    total_issues = sum(checks.values())
    c1.metric("Anomalies détectées", total_issues)
    c2.metric("Propositions contrôlées", len(P))
    c3.metric("Sources distinctes", P["source_url"].nunique() if not P.empty else 0)

    checks_df = pd.DataFrame(
        [{"Contrôle": key, "Nombre": value} for key, value in checks.items()]
    )
    st.dataframe(checks_df, hide_index=True, use_container_width=True)

    if total_issues == 0:
        st.success("Aucune anomalie simple détectée par ces contrôles automatiques.")
    else:
        st.warning(
            "Ces anomalies concernent la structure de la base et doivent être vérifiées avant d'étendre l'automatisation."
        )


def page_method():
    page_header(
        "Méthodologie",
        "Règles de publication destinées à privilégier la traçabilité plutôt que la quantité.",
    )

    st.markdown(
        """
<div class="flow">
  <div class="flow-step"><b>1 · Source</b><span>Document ou déclaration identifiable.</span></div>
  <div class="flow-step"><b>2 · Extraction</b><span>Proposition résumée sans extrapolation.</span></div>
  <div class="flow-step"><b>3 · Classement</b><span>Acteur, thème, sous-thème, date et nature.</span></div>
  <div class="flow-step"><b>4 · Validation</b><span>Contrôle humain avant publication sensible.</span></div>
  <div class="flow-step"><b>5 · Publication</b><span>Source accessible et statut temporel explicite.</span></div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
### Principes de publication

- **Une source identifiable par proposition.** Les liens doivent pouvoir être ouverts depuis l'application.
- **Le temps compte.** Une proposition issue de 2022 ou 2024 n'est pas automatiquement présentée comme une position pour 2027.
- **La nature du document est affichée.** Programme officiel, programme de coalition, position programmatique, etc.
- **Aucune absence n'est interprétée.** « Non enregistré dans la base » ne signifie pas « aucune position ».
- **Pas de notation politique.** Aucun score de proximité, de qualité, de cohérence ou de mérite n'est attribué.
- **Pas d'évolution déduite automatiquement.** Un changement doit être documenté par au moins deux états comparables et validé.
- **Les graphiques décrivent la base.** Ils ne servent pas à mesurer l'importance politique d'un thème.
- **Les doublons doivent être fusionnés.** Une même proposition peut avoir plusieurs sources sans être publiée plusieurs fois.
"""
    )

    st.subheader("Hiérarchie descriptive des sources")
    st.markdown(
        """
L'application ne donne pas de « score de fiabilité ». Elle distingue plutôt la **nature de la source** :
programme électoral ou de coalition, document officiel, communiqué, déclaration directe,
document parlementaire/institutionnel, puis éventuellement source journalistique lorsqu'elle est nécessaire pour documenter un fait ou une déclaration.
"""
    )

    st.subheader("Statut de cette base")
    st.info(
        f"{META.get('note', 'Base pilote non exhaustive.')} "
        f"Version {META.get('version', 'pilote')} — date de création : {META.get('date_creation', '—')}."
    )


# ============================================================
# NAVIGATION
# ============================================================

pages = {
    "Explorer": [
        st.Page(page_home, title="Accueil", default=True),
        st.Page(page_programmes, title="Programmes"),
        st.Page(page_themes, title="Thèmes"),
        st.Page(page_actors, title="Acteurs"),
        st.Page(page_compare, title="Comparer"),
        st.Page(page_evolutions, title="Évolutions"),
    ],
    "Transparence": [
        st.Page(page_sources, title="Sources & données"),
        st.Page(page_method, title="Méthodologie"),
    ],
}

st.navigation(pages).run()
