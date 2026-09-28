import html
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).parent
DATA_PATH = APP_DIR / "data.json"
CONTENT_PATH = APP_DIR / "content.json"

st.set_page_config(
    page_title="Observatoire politique",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
:root{
  --bg:#090b0e; --panel:#101419; --panel2:#151a21; --line:#29313b;
  --text:#f5f7f9; --muted:#9ca7b3; --soft:#d9dee4;
  --accent:#a9cbff; --accent2:#dce9ff;
}
.stApp{background:var(--bg);color:var(--text)}
[data-testid="stSidebar"]{background:#0c0f13;border-right:1px solid var(--line)}
.block-container{max-width:1460px;padding-top:1.25rem;padding-bottom:2rem}
h1{font-size:2rem!important;letter-spacing:-.035em;margin-bottom:.15rem!important}
h2,h3{letter-spacing:-.02em}
a{color:var(--accent2)}
.page-intro{color:var(--muted);max-width:1050px;line-height:1.5;margin:-.05rem 0 .75rem}
.hero{border:1px solid var(--line);border-radius:18px;padding:1rem 1.15rem;background:radial-gradient(circle at 85% 15%,rgba(169,203,255,.15),transparent 28%),linear-gradient(135deg,#121821,#0e1217 60%,#131a22);margin-bottom:.85rem}
.hero-k{font-size:.7rem;letter-spacing:.13em;text-transform:uppercase;color:var(--accent);font-weight:800}
.hero-t{font-size:2rem;font-weight:850;letter-spacing:-.04em;margin:.16rem 0 .28rem}
.hero-s{color:var(--muted);line-height:1.45;max-width:980px}
.tip{border-left:3px solid var(--accent);background:#111720;padding:.52rem .7rem;border-radius:8px;color:#cfd6df;font-size:.81rem;margin:.45rem 0 .8rem}
.notice{border:1px solid var(--line);background:var(--panel);border-radius:12px;padding:.68rem .8rem;color:var(--soft);font-size:.83rem;line-height:1.45;margin:.45rem 0 .8rem}
.card{border:1px solid var(--line);background:var(--panel);border-radius:12px;padding:.62rem .78rem;margin:.34rem 0}
.card:hover{border-color:#3d4958}
.card-title{font-weight:760;font-size:.95rem;line-height:1.25}
.meta{font-size:.72rem;color:var(--muted);line-height:1.35;margin-top:.1rem}
.summary{font-size:.85rem;color:#dce1e7;line-height:1.42;margin:.28rem 0}
.badge{display:inline-block;border:1px solid #334254;background:#17212d;color:#d9e8ff;border-radius:999px;padding:.07rem .36rem;font-size:.63rem;font-weight:700;margin-right:.15rem}
.badge2{display:inline-block;border:1px solid var(--line);background:#12171d;color:var(--muted);border-radius:999px;padding:.07rem .36rem;font-size:.63rem;font-weight:650;margin-right:.15rem}
.src a{font-size:.72rem;font-weight:700;text-decoration:none;color:var(--accent2)!important}
.actor-head{border:1px solid var(--line);background:linear-gradient(135deg,#111821,#101419);border-radius:16px;padding:.9rem 1rem;margin-bottom:.7rem}
.actor-name{font-size:1.42rem;font-weight:850;margin-bottom:.12rem}
.actor-note{color:var(--muted);font-size:.81rem;line-height:1.4}
.bar-row{display:grid;grid-template-columns:minmax(190px,34%) 1fr 38px;align-items:center;gap:.55rem;margin:.33rem 0}
.bar-label{font-size:.77rem;color:#dfe4ea;white-space:normal;line-height:1.25}
.bar-track{background:#161c23;border:1px solid var(--line);border-radius:999px;height:10px;overflow:hidden}
.bar-fill{height:100%;background:linear-gradient(90deg,#769ed8,#a9cbff);border-radius:999px}
.bar-val{font-size:.72rem;color:var(--muted);text-align:right}
.news-card{display:grid;grid-template-columns:150px 1fr;border:1px solid var(--line);background:var(--panel);border-radius:14px;overflow:hidden;margin:.45rem 0}
.news-img{min-height:112px;background:linear-gradient(135deg,#1b2532,#11161d);display:flex;align-items:center;justify-content:center;color:#7e8c9d;font-size:.74rem}
.news-body{padding:.72rem .82rem}
.news-title{font-size:.99rem;font-weight:800;line-height:1.25;margin-bottom:.16rem}
.news-meta{font-size:.7rem;color:var(--muted)}
.news-summary{font-size:.82rem;color:#d7dde4;line-height:1.4;margin-top:.3rem}
.agenda-card{display:grid;grid-template-columns:72px 1fr;border:1px solid var(--line);background:var(--panel);border-radius:12px;overflow:hidden;margin:.38rem 0}
.agenda-date{background:#141b24;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:.55rem}
.agenda-day{font-size:1.23rem;font-weight:850}.agenda-month{font-size:.66rem;color:var(--muted);text-transform:uppercase}
.agenda-body{padding:.6rem .72rem}.agenda-title{font-weight:760}.agenda-meta{font-size:.71rem;color:var(--muted)}
.compare-wrap{display:grid;grid-template-columns:1fr 64px 1fr;gap:.55rem;align-items:stretch;margin:.6rem 0}
.before,.after{border:1px solid var(--line);background:var(--panel);border-radius:12px;padding:.75rem}
.arrow{display:flex;align-items:center;justify-content:center;color:var(--accent);font-size:1.55rem;font-weight:800}
.ba-label{font-size:.68rem;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);font-weight:800}
.ba-title{font-size:.92rem;font-weight:760;margin:.2rem 0}.ba-text{font-size:.81rem;color:#d8dee5;line-height:1.4}
.evo-change{border-left:3px solid var(--accent);background:#111720;border-radius:8px;padding:.58rem .7rem;margin:.45rem 0;color:#dbe2ea;font-size:.82rem}
div[data-testid="stMetric"]{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:.45rem .62rem}
div[data-testid="stMetricValue"]{font-size:1.3rem}
div[data-testid="stMetricLabel"]{color:var(--muted)}
div[data-testid="stExpander"]{border:1px solid var(--line);background:var(--panel);border-radius:11px}
div[data-testid="stExpander"] summary{font-size:.76rem!important;color:#cbd3dc!important}
div[data-testid="stExpander"] p,div[data-testid="stExpander"] li{font-size:.81rem!important}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:12px;overflow:hidden}
hr{border-color:var(--line)!important}
@media(max-width:800px){
  .block-container{padding-left:.75rem;padding-right:.75rem}
  .hero-t{font-size:1.58rem}
  .news-card{grid-template-columns:1fr}
  .news-img{min-height:92px}
  .compare-wrap{grid-template-columns:1fr}
  .arrow{transform:rotate(90deg);min-height:34px}
  .bar-row{grid-template-columns:minmax(125px,42%) 1fr 30px}
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    with DATA_PATH.open(encoding="utf-8") as f:
        d = json.load(f)
    with CONTENT_PATH.open(encoding="utf-8") as f:
        c = json.load(f)
    return d, c, pd.DataFrame(d.get("propositions", [])), pd.DataFrame(d.get("acteurs", [])), pd.DataFrame(d.get("sources", []))

RAW, CONTENT, P, ACTEURS, SOURCES = load_data()

SOURCE_LABELS = {
    "Programme électoral": "Programme officiel",
    "Programme de coalition": "Programme officiel de coalition",
    "Programme de référence en réactualisation": "Programme de référence en mise à jour",
}

def esc(x): return html.escape("" if x is None else str(x), quote=True)
def source_label(x): return SOURCE_LABELS.get(str(x), str(x))

def normalize(x):
    s = unicodedata.normalize("NFKD", str(x))
    return "".join(c for c in s if not unicodedata.combining(c)).casefold()

def search_mask(df, q, cols):
    if not q: return pd.Series(True, index=df.index)
    nq = normalize(q); m = pd.Series(False, index=df.index)
    for col in cols:
        if col in df.columns:
            m |= df[col].fillna("").map(normalize).str.contains(re.escape(nq), regex=True)
    return m

def actor_options():
    return ["Tous les acteurs politiques"] + sorted(P["acteur"].dropna().unique().tolist())

def actor_select(label, key): return st.selectbox(label, actor_options(), key=key)
def filter_actor(df, actor): return df if actor == "Tous les acteurs politiques" else df[df["acteur"] == actor]
def unique_values(df, col): return sorted(df[col].dropna().astype(str).unique().tolist()) if col in df.columns else []

def page_intro(text, how=None):
    st.markdown(f'<div class="page-intro">{esc(text)}</div>', unsafe_allow_html=True)
    if how:
        st.markdown(f'<div class="tip"><strong>Comment lire cette page ?</strong> {esc(how)}</div>', unsafe_allow_html=True)

def horizontal_bars(series, title=None):
    if title: st.markdown(f"**{title}**")
    if series is None or len(series) == 0:
        st.caption("Pas assez de données pour afficher ce graphique."); return
    mx = max(series.max(), 1); rows = []
    for label, value in series.items():
        width = max(4, round((value / mx) * 100, 1))
        rows.append(f'<div class="bar-row"><div class="bar-label">{esc(label)}</div><div class="bar-track"><div class="bar-fill" style="width:{width}%"></div></div><div class="bar-val">{int(value)}</div></div>')
    st.markdown("".join(rows), unsafe_allow_html=True)

def proposal_card(r, show_actor=True):
    actor_prefix = f"{esc(r.get('acteur'))} · " if show_actor else ""
    st.markdown(f"""
<div class="card">
  <div class="card-title">{esc(r.get('titre',''))}</div>
  <div class="meta">{actor_prefix}{esc(r.get('theme',''))} → {esc(r.get('sous_theme',''))} · {esc(r.get('election_concernee',''))}</div>
  <div class="summary">{esc(r.get('resume',''))}</div>
  <span class="badge">{esc(source_label(r.get('type_source_position','Source')))}</span>
  <span class="badge2">{esc(r.get('annee_source',''))}</span>
  <span class="src">↗ <a href="{esc(r.get('source_url',''))}" target="_blank" rel="noopener noreferrer">{esc(r.get('source_titre','Source'))}</a></span>
</div>
""", unsafe_allow_html=True)
    with st.expander("＋ Source et détails", expanded=False):
        st.markdown(f"**Source utilisée :** [{r.get('source_titre','Source')}]({r.get('source_url','')})")
        st.markdown(f"**Document / version :** {r.get('version_programme','')}")
        status = str(r.get("statut_2027", "")).strip()
        if status: st.markdown(f"**Situation pour 2027 :** {status}")
        st.caption("Cette fiche décrit ce qui est enregistré dans la base. Elle ne garantit pas, à elle seule, qu'il s'agit de la position la plus récente.")

def metrics(df):
    c = st.columns(4)
    c[0].metric("Propositions", len(df))
    c[1].metric("Acteurs / coalitions", df["acteur"].nunique() if len(df) else 0)
    c[2].metric("Thèmes", df["theme"].nunique() if len(df) else 0)
    c[3].metric("Sources distinctes", df["source_url"].nunique() if len(df) else 0)

def empty_dynamic(kind):
    st.markdown(f'<div class="notice"><strong>{esc(kind)} :</strong> la structure est prête, mais aucune donnée n’est publiée automatiquement pour l’instant. Cette rubrique sera alimentée à partir de sources datées et validées lors de la mise en place de la veille.</div>', unsafe_allow_html=True)

def news_card(item):
    img = item.get("image_url")
    style = f"background-image:url('{esc(img)}');background-size:cover;background-position:center;" if img else ""
    image_text = "" if img else "IMAGE SOURCÉE"
    st.markdown(f"""
<div class="news-card"><div class="news-img" style="{style}">{image_text}</div><div class="news-body">
<div class="news-title">{esc(item.get('titre',''))}</div><div class="news-meta">{esc(item.get('date',''))} · {esc(item.get('source',''))}</div>
<div class="news-summary">{esc(item.get('resume',''))}</div><div class="src">↗ <a href="{esc(item.get('url',''))}" target="_blank" rel="noopener noreferrer">Lire la source</a></div>
</div></div>
""", unsafe_allow_html=True)

def home():
    st.markdown("""
<div class="hero"><div class="hero-k">Observatoire politique · V2.1</div><div class="hero-t">Comprendre les programmes, les positions et leurs évolutions</div><div class="hero-s">Un observatoire conçu pour remonter aux sources, distinguer les périodes et comparer sans notation ni classement.</div></div>
""", unsafe_allow_html=True)
    st.subheader("À la une")
    actus = CONTENT.get("actualites", [])
    if actus:
        for item in actus[:3]: news_card(item)
    else: empty_dynamic("Actualités politiques")
    st.subheader("Prochains rendez-vous")
    agenda = CONTENT.get("agenda", [])
    if agenda:
        for event in agenda[:4]: st.write(event)
    else: st.caption("L’agenda sera activé avec la veille sourcée : débats, meetings, échéances et publications annoncées.")
    st.divider()
    page_intro("Commencez par rechercher un sujet ou choisissez un acteur. L’accueil donne une vue rapide ; les pages spécialisées permettent ensuite d’aller plus loin.", "Les compteurs et graphiques décrivent uniquement ce que contient la base, pas l’importance politique d’un thème.")
    actor = actor_select("Afficher", "home_actor")
    df = filter_actor(P.copy(), actor)
    metrics(df)
    q = st.text_input("Rechercher", placeholder="Ex. hôpital, retraites, logement, nucléaire…", key="home_q")
    if q: df = df[search_mask(df, q, ["titre","resume","theme","sous_theme","acteur","source_titre"])]
    left, right = st.columns([1.55, 1])
    with left:
        st.subheader("Propositions enregistrées"); st.caption(f"{len(df)} résultat(s)")
        for _, r in df.head(6).iterrows(): proposal_card(r, show_actor=(actor == "Tous les acteurs politiques"))
        if len(df) > 6: st.caption("Les 6 premiers résultats sont affichés. Utilisez Programmes ou Thèmes pour explorer davantage.")
    with right:
        st.subheader("Répartition par thème"); horizontal_bars(df["theme"].value_counts().head(10)); st.caption("Nombre de fiches actuellement présentes dans la base par thème.")

def programmes():
    st.title("Programmes")
    page_intro("Cette page répond à la question : « Que propose cet acteur politique dans les corpus que nous suivons ? »", "Choisissez un acteur. La fiche repère donne le contexte du corpus ; les propositions sont ensuite classées par thème.")
    actor = st.selectbox("Choisir un acteur", sorted(P["acteur"].unique()), key="prog_actor")
    df = P[P["acteur"] == actor].copy(); ar = ACTEURS[ACTEURS["nom"] == actor]
    st.markdown(f'<div class="actor-head"><div class="actor-name">{esc(actor)}</div><div class="actor-note">Fiche repère : contexte du corpus, couverture de la base et accès aux propositions sourcées.</div></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1.35, 1])
    with c1:
        if not ar.empty:
            row = ar.iloc[0]
            st.markdown(f"**Type d’acteur :** {row.get('type','')}")
            st.markdown(f"**Corpus suivi :** {row.get('statut_programmatique_2027','')}")
            if row.get("site_officiel"): st.link_button("Site officiel", str(row.get("site_officiel")))
        st.markdown("**Comment comprendre cette fiche ?**")
        st.caption("Elle synthétise les documents présents dans l’observatoire. Elle ne prétend pas résumer toute l’activité ou toute l’histoire du parti.")
    with c2:
        cc = st.columns(2); cc[0].metric("Propositions", len(df)); cc[1].metric("Thèmes documentés", df["theme"].nunique()); st.metric("Sources distinctes", df["source_url"].nunique())
    horizontal_bars(df["theme"].value_counts().head(12), "Thèmes documentés dans la base")
    st.caption("La longueur des barres correspond au nombre de fiches enregistrées, pas à une priorité politique.")
    st.subheader("Chronologie des corpus présents")
    timeline = df.groupby(["annee_source","election_concernee"], dropna=False).size().reset_index(name="Fiches").sort_values("annee_source")
    st.dataframe(timeline, hide_index=True, use_container_width=True)
    st.subheader("Parcourir les propositions")
    theme = st.selectbox("Filtrer par thème", ["Tous les thèmes"] + unique_values(df,"theme"), key="prog_theme")
    q = st.text_input("Rechercher dans ce programme", placeholder="Ex. retraites, sécurité, santé…", key="prog_q")
    view = df.copy()
    if theme != "Tous les thèmes": view = view[view["theme"] == theme]
    if q: view = view[search_mask(view,q,["titre","resume","theme","sous_theme"])]
    for th in view["theme"].dropna().unique():
        part = view[view["theme"] == th]
        with st.expander(f"{th} · {len(part)}", expanded=False):
            for _, r in part.iterrows(): proposal_card(r, show_actor=False)

def themes():
    st.title("Thèmes")
    page_intro("Cette page répond à la question : « Que proposent les différents acteurs sur un même sujet ? »", "Choisissez un thème puis, si besoin, un sous-thème. Les acteurs sont présentés séparément pour faciliter la lecture comparative.")
    c = st.columns(3)
    with c[0]: theme = st.selectbox("Thème", sorted(P["theme"].unique()), key="th_theme")
    base = P[P["theme"] == theme]
    with c[1]: sub = st.selectbox("Sous-thème", ["Tous les sous-thèmes"] + unique_values(base,"sous_theme"), key="th_sub")
    with c[2]: actor = actor_select("Acteur", "th_actor")
    df = base.copy()
    if sub != "Tous les sous-thèmes": df = df[df["sous_theme"] == sub]
    df = filter_actor(df, actor)
    st.markdown(f"### {theme}" + (f" → {sub}" if sub != "Tous les sous-thèmes" else "")); st.caption(f"{len(df)} proposition(s) actuellement enregistrée(s).")
    if df.empty:
        st.warning("Aucune proposition n’est enregistrée pour cette sélection. Cela ne signifie pas qu’aucune position n’existe."); return
    for actor_name in sorted(df["acteur"].unique()):
        st.markdown(f"#### {actor_name}")
        for _, r in df[df["acteur"] == actor_name].iterrows(): proposal_card(r, show_actor=False)

def acteurs():
    st.title("Acteurs")
    page_intro("Retrouvez ici les acteurs suivis par l’observatoire et le périmètre de données disponible pour chacun.", "Les portraits pourront être ajoutés lorsque leur origine et leurs droits d’utilisation seront documentés.")
    actor = actor_select("Acteur politique", "actors_sel")
    selected = ACTEURS if actor == "Tous les acteurs politiques" else ACTEURS[ACTEURS["nom"] == actor]
    for _, ar in selected.iterrows():
        name = ar.get("nom", ""); df = P[P["acteur"] == name]
        st.markdown(f'<div class="actor-head"><div class="actor-name">{esc(name)}</div><div class="actor-note">{esc(ar.get("type",""))}</div></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1.4, 1])
        with c1:
            st.markdown(f"**Corpus suivi :** {ar.get('statut_programmatique_2027','')}")
            if ar.get("site_officiel"): st.link_button("Site officiel", str(ar.get("site_officiel")))
        with c2:
            st.metric("Propositions enregistrées", len(df)); st.metric("Thèmes documentés", df["theme"].nunique())
        horizontal_bars(df["theme"].value_counts().head(10)); st.divider()

def comparer():
    st.title("Comparer")
    page_intro("Cette page met plusieurs acteurs côte à côte sur un même sujet.", "Une absence de fiche signifie seulement que notre base ne contient pas encore de proposition correspondante.")
    all_actors = sorted(P["acteur"].unique())
    mode = st.selectbox("Acteurs", ["Tous les acteurs politiques", "Sélection personnalisée"], key="cmp_mode")
    selected = all_actors if mode == "Tous les acteurs politiques" else st.multiselect("Choisir", all_actors, default=all_actors[:min(3,len(all_actors))])
    c1, c2 = st.columns(2)
    with c1: theme = st.selectbox("Thème", sorted(P["theme"].unique()), key="cmp_theme")
    rel = P[P["theme"] == theme]
    with c2: sub = st.selectbox("Sous-thème", ["Tous les sous-thèmes"] + unique_values(rel,"sous_theme"), key="cmp_sub")
    df = P[(P["acteur"].isin(selected)) & (P["theme"] == theme)]
    if sub != "Tous les sous-thèmes": df = df[df["sous_theme"] == sub]
    if len(selected) <= 3 and selected:
        cols = st.columns(len(selected))
        for i, actor in enumerate(selected):
            with cols[i]:
                st.subheader(actor); ad = df[df["acteur"] == actor]
                if ad.empty: st.caption("Aucune fiche enregistrée pour cette sélection.")
                for _, r in ad.iterrows(): proposal_card(r, False)
    elif selected:
        tabs = st.tabs(selected)
        for tab, actor in zip(tabs, selected):
            with tab:
                ad = df[df["acteur"] == actor]
                if ad.empty: st.caption("Aucune fiche enregistrée pour cette sélection.")
                for _, r in ad.iterrows(): proposal_card(r, False)

def evolutions():
    st.title("Évolutions")
    page_intro("Cette page répond à la question : « Qu’est-ce qui a changé dans la position d’un acteur ? »", "Chaque évolution publiée relie un état « Avant » à un état « Après », avec les deux sources et une explication courte du changement.")
    c1, c2 = st.columns(2)
    with c1: actor = actor_select("Acteur politique", "evo_actor")
    with c2: theme = st.selectbox("Thème", ["Tous les thèmes"] + sorted(P["theme"].unique()), key="evo_theme")
    evols = []
    for e in CONTENT.get("evolutions", []):
        if actor != "Tous les acteurs politiques" and e.get("acteur") != actor: continue
        if theme != "Tous les thèmes" and e.get("theme") != theme: continue
        evols.append(e)
    if not evols:
        st.markdown('<div class="notice"><strong>Aucune évolution validée n’est encore publiée.</strong> La page n’affiche volontairement pas de changement tant qu’une position « avant » et une position « après » n’ont pas été reliées et vérifiées.</div>', unsafe_allow_html=True)
        st.subheader("Exemple de lecture")
        st.markdown('''<div class="compare-wrap"><div class="before"><div class="ba-label">Avant</div><div class="ba-title">Position antérieure documentée</div><div class="ba-text">Résumé court de l’ancienne position, avec date et source.</div></div><div class="arrow">→</div><div class="after"><div class="ba-label">Après</div><div class="ba-title">Nouvelle position documentée</div><div class="ba-text">Résumé court de la position plus récente, avec date et source.</div></div></div><div class="evo-change"><strong>Ce qui change :</strong> explication factuelle et concise de la différence entre les deux états.</div>''', unsafe_allow_html=True)
        st.caption("Cet exemple montre uniquement le format d’affichage et ne décrit aucun acteur réel.")
    else:
        for e in evols:
            st.subheader(f"{e.get('acteur','')} — {e.get('theme','')}")
            st.markdown(f'''<div class="compare-wrap"><div class="before"><div class="ba-label">Avant · {esc(e.get('avant_date',''))}</div><div class="ba-title">{esc(e.get('avant_titre',''))}</div><div class="ba-text">{esc(e.get('avant_resume',''))}</div></div><div class="arrow">→</div><div class="after"><div class="ba-label">Après · {esc(e.get('apres_date',''))}</div><div class="ba-title">{esc(e.get('apres_titre',''))}</div><div class="ba-text">{esc(e.get('apres_resume',''))}</div></div></div><div class="evo-change"><strong>Ce qui change :</strong> {esc(e.get('commentaire',''))}</div>''', unsafe_allow_html=True)
            st.markdown(f"[Source avant]({e.get('avant_url','')}) · [Source après]({e.get('apres_url','')})")

def actualites():
    st.title("Actualités")
    page_intro("Cette page rassemblera les actualités utiles pour comprendre l’évolution des programmes, positions et campagnes.", "Chaque carte doit afficher sa date, sa source et son lien. Une accusation, une enquête ou une polémique est attribuée à sa source et n’est pas présentée comme un fait établi.")
    tabs = st.tabs(["Actualités politiques", "Agenda", "Mises à jour de l’observatoire"])
    with tabs[0]:
        actus = CONTENT.get("actualites", [])
        if not actus: empty_dynamic("Actualités politiques")
        else:
            for item in actus: news_card(item)
    with tabs[1]:
        agenda = CONTENT.get("agenda", [])
        if not agenda: empty_dynamic("Agenda")
        else:
            for item in agenda:
                st.markdown(f'<div class="agenda-card"><div class="agenda-date"><div class="agenda-day">{esc(item.get("jour",""))}</div><div class="agenda-month">{esc(item.get("mois",""))}</div></div><div class="agenda-body"><div class="agenda-title">{esc(item.get("titre",""))}</div><div class="agenda-meta">{esc(item.get("heure",""))} · {esc(item.get("lieu",""))}</div></div></div>', unsafe_allow_html=True)
    with tabs[2]: st.info("Cette rubrique affichera les nouvelles propositions ajoutées, les sources mises à jour et les évolutions validées dans l’observatoire.")

def sources_page():
    st.title("Sources & données")
    page_intro("Cette page permet de vérifier d’où viennent les informations et de voir ce que la base couvre réellement.", "Les graphiques décrivent la base elle-même ; ils ne jugent pas les acteurs ni leurs programmes.")
    actor = actor_select("Acteur politique", "src_actor"); df = filter_actor(P.copy(), actor)
    urls = set(df["source_url"].dropna())
    s = SOURCES[SOURCES["url"].isin(urls)] if not SOURCES.empty and "url" in SOURCES.columns else SOURCES.copy()
    if not s.empty:
        cols = [c for c in ["titre","type_source","organisme","annee","url"] if c in s.columns]
        cfg = {"url": st.column_config.LinkColumn("Lien", display_text="Ouvrir ↗")} if "url" in cols else None
        st.dataframe(s[cols], hide_index=True, use_container_width=True, column_config=cfg)
        st.download_button("Exporter les sources en CSV", s.to_csv(index=False).encode("utf-8-sig"), "observatoire_sources.csv", "text/csv")
    st.subheader("Couverture de la base")
    c1, c2 = st.columns(2)
    with c1: horizontal_bars(df["acteur"].value_counts(), "Fiches par acteur")
    with c2: horizontal_bars(df["type_source_position"].map(source_label).value_counts(), "Fiches par nature de source")
    pivot = pd.pivot_table(df, index="theme", columns="acteur", values="id_proposition", aggfunc="count", fill_value=0)
    st.markdown("**Matrice thème × acteur**"); st.dataframe(pivot, use_container_width=True)
    st.caption("Un zéro signifie seulement qu’aucune fiche correspondante n’est enregistrée dans la base actuelle.")

def methodo():
    st.title("Méthodologie")
    page_intro("Cette page explique comment une information entre dans l’observatoire et quelles précautions sont prises avant sa publication.", "Elle aide à distinguer une source, une proposition, une actualité et une évolution.")
    st.markdown('''### Chaîne de traitement
**1. Source** → **2. Extraction** → **3. Classement** → **4. Vérification** → **5. Publication**

### Principes
- Chaque proposition renvoie vers une **source identifiable**.
- Une mesure ancienne n’est pas automatiquement présentée comme une position actuelle.
- Une absence dans la base n’est jamais interprétée comme une absence de position.
- Aucun score, classement ou note politique n’est produit.
- Une évolution nécessite un **« avant » et un « après » comparables et sourcés**.
- Les actualités distinguent faits, déclarations, enquêtes, accusations et réactions.
- Les images devront avoir une origine documentée et un usage compatible avec leurs droits.
''')

pages = {
    "Explorer": [
        st.Page(home, title="Accueil", default=True),
        st.Page(programmes, title="Programmes"),
        st.Page(themes, title="Thèmes"),
        st.Page(acteurs, title="Acteurs"),
        st.Page(comparer, title="Comparer"),
        st.Page(evolutions, title="Évolutions"),
        st.Page(actualites, title="Actualités"),
    ],
    "Transparence": [
        st.Page(sources_page, title="Sources & données"),
        st.Page(methodo, title="Méthodologie"),
    ],
}
st.navigation(pages).run()
