#!/usr/bin/env python3
"""Enrichit l'export HTML PICO-8 (index.html) en une page vitrine complete
pour GitHub Pages : charte graphique LFI / Union Populaire, jaquette sur
l'ecran d'accueil du lecteur, guide des commandes clavier/manette/mobile,
presentation des 4 classes militantes, galerie et telechargement du .p8.png.
"""
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent.parent
HTML_PATH = ROOT / "index.html"

HEAD_EXTRA = """<meta charset="utf-8">
<title>L'Avenir en commun RPG — Pour la 6e République (Jeu PICO-8)</title>
<meta name="description" content="RPG rétro PICO-8 : incarnez un militant insoumis, convainquez le pays avec L'Avenir en commun, brisez les 4 grands monopoles et instaurez la 6e République !">
<meta property="og:title" content="L'Avenir en commun RPG — Pour la 6e République">
<meta property="og:description" content="Un RPG rétro 8-bit complet jouable dans le navigateur (PC, Mobile, Manette) autour de L'Avenir en commun.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://boblefrag.github.io/union-populaire-rpg/">
<meta property="og:image" content="https://boblefrag.github.io/union-populaire-rpg/label_preview.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="L'Avenir en commun RPG — Pour la 6e République">
<meta name="twitter:description" content="RPG rétro PICO-8 jouable en 1 clic dans le navigateur : 4 classes militantes, 5 bastions, L'Avenir en commun !">
<meta name="twitter:image" content="https://boblefrag.github.io/union-populaire-rpg/label_preview.png">
<link rel="icon" type="image/png" href="label_preview.png">
"""

CUSTOM_CSS = """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: radial-gradient(circle at top, #1d2b53 0%, #0b1021 70%, #050811 100%) !important;
    color: #fff1e8 !important;
    line-height: 1.5;
}
.up-wrap {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px 16px 48px;
}
.up-header {
    text-align: center;
    margin-bottom: 18px;
}
.up-badge {
    display: inline-block;
    background: #ff004d;
    color: #fff1e8;
    font-weight: 800;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 8px;
    box-shadow: 0 2px 10px rgba(255, 0, 77, 0.4);
}
.up-title {
    font-size: clamp(1.8rem, 4vw, 2.7rem);
    font-weight: 900;
    margin: 4px 0;
    letter-spacing: -0.02em;
    color: #fff1e8;
    text-shadow: 0 3px 0 #1d2b53, 0 0 20px rgba(41, 173, 255, 0.35);
}
.up-title span {
    color: #29adff;
}
.up-sub {
    font-size: 1.02rem;
    color: #c2c3c7;
    max-width: 640px;
    margin: 6px auto 12px;
}
.up-hint {
    display: inline-block;
    background: rgba(41, 173, 255, 0.14);
    border: 1px solid rgba(41, 173, 255, 0.45);
    color: #ffec27;
    font-size: 0.9rem;
    font-weight: 600;
    padding: 6px 14px;
    border-radius: 8px;
}
#p8_frame_0 {
    border: 3px solid #29adff;
    border-radius: 12px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.65), 0 0 24px rgba(41, 173, 255, 0.22);
    background: #000;
    overflow: hidden;
}
.p8_start_button {
    background: url("label_preview.png") center center / contain no-repeat #000 !important;
    image-rendering: pixelated;
}
.up-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
    gap: 16px;
    margin-top: 24px;
}
.up-card {
    background: rgba(29, 43, 83, 0.55);
    border: 1px solid rgba(41, 173, 255, 0.3);
    border-radius: 10px;
    padding: 16px 18px;
}
.up-card h2 {
    font-size: 1.15rem;
    margin: 0 0 10px;
    color: #ffec27;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid rgba(255, 241, 232, 0.12);
    padding-bottom: 6px;
}
.up-controls {
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 0.93rem;
}
.up-controls li {
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}
.kbd {
    background: #0b1021;
    border: 1px solid #29adff;
    color: #29adff;
    padding: 2px 8px;
    border-radius: 5px;
    font-family: monospace;
    font-weight: 700;
    font-size: 0.85rem;
    white-space: nowrap;
}
.kbd-red {
    border-color: #ff004d;
    color: #ff77a8;
}
.up-classes {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    margin-top: 12px;
}
.up-class {
    background: rgba(11, 16, 33, 0.65);
    border-left: 4px solid #29adff;
    border-radius: 6px;
    padding: 10px 12px;
    font-size: 0.9rem;
}
.up-class strong {
    display: block;
    font-size: 0.98rem;
    margin-bottom: 3px;
}
.up-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
    gap: 12px;
    margin-top: 12px;
}
.up-gallery figure {
    margin: 0;
    background: #0b1021;
    border: 1px solid rgba(255, 241, 232, 0.15);
    border-radius: 8px;
    padding: 8px;
    text-align: center;
}
.up-gallery img {
    width: 100%;
    height: auto;
    image-rendering: pixelated;
    border-radius: 4px;
}
.up-gallery figcaption {
    font-size: 0.8rem;
    color: #c2c3c7;
    margin-top: 6px;
}
.up-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
    margin-top: 22px;
}
.up-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #ff004d;
    color: #fff1e8;
    text-decoration: none;
    font-weight: 700;
    padding: 10px 18px;
    border-radius: 8px;
    transition: transform 0.12s ease, background 0.12s ease;
}
.up-btn:hover {
    transform: translateY(-1px);
    background: #ff2466;
}
.up-btn-secondary {
    background: #29adff;
    color: #0b1021;
}
.up-btn-secondary:hover {
    background: #54beff;
}
.up-footer {
    text-align: center;
    margin-top: 28px;
    font-size: 0.85rem;
    color: #83769c;
}
"""

ABOVE_HTML = """
<div class="up-wrap">
  <header class="up-header">
    <div class="up-badge">φ Contribution Militante — La France Insoumise</div>
    <h1 class="up-title">L'UNION <span>POPULAIRE</span> — LE RPG</h1>
    <p class="up-sub">
      Parcourez le pays de <strong>Saint-Denis</strong> à <strong>Marseille</strong> en passant par <strong>Lille</strong>, <strong>Lyon</strong> et <strong>Le Bourget</strong>, débattez face aux éditorialistes et lobbyistes, débloquez les 4 piliers de <em>L'Avenir en Commun</em> et instaurez la <strong>6e République</strong> !
    </p>
    <div class="up-hint">▶ Cliquez sur la jaquette ci-dessous pour lancer le jeu (Clavier, Manette ou Mobile)</div>
  </header>
"""

BELOW_HTML = """
  <div class="up-grid">
    <section class="up-card">
      <h2>🎮 Commandes du jeu</h2>
      <ul class="up-controls">
        <li>
          <span>Se déplacer / Naviguer</span>
          <span class="kbd">⬅️ ⬆️ ⬇️ ➡️</span>
        </li>
        <li>
          <span><strong>Bouton 🅾️</strong> — Valider / Convaincre</span>
          <span class="kbd kbd-red">Z / C / N</span>
        </li>
        <li>
          <span><strong>Bouton ❎</strong> — Menu Terrain / Annuler</span>
          <span class="kbd">X / V / M</span>
        </li>
        <li>
          <span>Pause / Options PICO-8</span>
          <span class="kbd">Entrée / P</span>
        </li>
        <li>
          <span>Manette USB / Bluetooth</span>
          <span class="kbd">Automatique</span>
        </li>
        <li>
          <span>Smartphone / Tablette</span>
          <span class="kbd">Tactile intégré</span>
        </li>
      </ul>
    </section>

    <section class="up-card">
      <h2>📕 Astuces de Campagne</h2>
      <ul class="up-controls" style="display:block;">
        <li style="display:block; margin-bottom:8px;">
          🏛️ <strong>QG Militants (Villes)</strong> : Reposez votre équipe pour sauvegarder la stratégie, versez les dons de soutien et équipez vos tracts, mégaphones et gilets citoyens.
        </li>
        <li style="display:block; margin-bottom:8px;">
          🔓 <strong>Les 4 Verrous</strong> : Chaque bastion vaincu (*Tour des Médias*, *Banque Offshore*, *Tour d'Austérité*, *Lobby Central*) inscrit une mesure phare au programme et ouvre de nouveaux passages sur la carte.
        </li>
        <li style="display:block;">
          💡 <strong>Boîte d'aide intégrée</strong> : Dans chaque menu, une fenêtre explicative vous détaille l'effet de l'action ou du matériel sélectionné.
        </li>
      </ul>
    </section>
  </div>

  <section class="up-card" style="margin-top:16px;">
    <h2>✊ Les 4 Profils Militants</h2>
    <div class="up-classes">
      <div class="up-class" style="border-left-color:#ff004d;">
        <strong style="color:#ff004d;">Militant</strong>
        Militant LFI de terrain : haute conviction et grande force d'argumentation directe en débat et porte-à-porte.
      </div>
      <div class="up-class" style="border-left-color:#29adff;">
        <strong style="color:#29adff;">Streamer</strong>
        Spécialiste de la mobilisation médiatique : <em>Débat en direct</em>, <em>Tribune libre</em>, <em>Onde populaire</em>.
      </div>
      <div class="up-class" style="border-left-color:#fff1e8;">
        <strong style="color:#fff1e8;">Street Medic</strong>
        Soutien solidaire (<em>Sérum phy</em>, <em>Services publics</em>, <em>Bouclier social</em>) jusqu'à <em>La Constituante</em>.
      </div>
      <div class="up-class" style="border-left-color:#00e436;">
        <strong style="color:#00e436;">Fact-checker</strong>
        Agilité maximale et <em>Recul médiatique</em> permettant d'esquiver une polémique et de contrer x3.
      </div>
    </div>
  </section>

  <section class="up-card" style="margin-top:16px;">
    <h2>📸 Aperçus du Jeu &amp; Cartouche PICO-8</h2>
    <div class="up-gallery">
      <figure>
        <img src="gameplay_4_monde.png" alt="Exploration en vue du dessus sur la carte">
        <figcaption>Carte du monde (vue du dessus)</figcaption>
      </figure>
      <figure>
        <img src="gameplay_1_ville.png" alt="QG Militant en ville (Marseille)">
        <figcaption>En ville : QG Militant</figcaption>
      </figure>
      <figure>
        <img src="gameplay_2_combat_ext.png" alt="Débat en extérieur">
        <figcaption>Débat en extérieur</figcaption>
      </figure>
      <figure>
        <img src="gameplay_3_combat_donjon.png" alt="Débat dans un bastion face au Monarque">
        <figcaption>Bastion : Face au Monarque</figcaption>
      </figure>
      <figure>
        <img src="label_preview.png" alt="Jaquette L'Avenir en commun RPG">
        <figcaption>Jaquette officielle (φ LFI)</figcaption>
      </figure>
      <figure>
        <img src="ending_1_election.png" alt="20h00 Victoire de LFI">
        <figcaption>20h00 : Victoire populaire !</figcaption>
      </figure>
      <figure>
        <img src="ending_4_programme.png" alt="L'Avenir en Commun en actes">
        <figcaption>L'Avenir en Commun en actes</figcaption>
      </figure>
      <figure>
        <img src="ending_7_victoire.png" alt="Place au Peuple">
        <figcaption>Place au Peuple !</figcaption>
      </figure>
    </div>

    <div class="up-actions">
      <a class="up-btn" href="union_populaire_rpg.p8.png" download="union_populaire_rpg.p8.png">
        💾 Télécharger la cartouche PICO-8 (.p8.png)
      </a>
      <a class="up-btn up-btn-secondary" href="https://github.com/boblefrag/union-populaire-rpg" target="_blank" rel="noopener">
        💻 Code source libre (GitHub)
      </a>
    </div>
  </section>

  <footer class="up-footer">
    L'Avenir en commun RPG — Conception &amp; développement : Yohann Gabory • Propulsé par PICO-8 • Licence libre AGPLv3
  </footer>
</div>
"""


def main():
    html = HTML_PATH.read_text(encoding="utf-8")
    # 1. Remplace <title>PICO-8 Cartridge</title> par les meta complets
    html = html.replace("<title>PICO-8 Cartridge</title>", HEAD_EXTRA, 1)
    # 2. Injecte le CSS personnalise juste avant --></STYLE>
    html = html.replace("-->\n</STYLE>", CUSTOM_CSS + "\n-->\n</STYLE>", 1)
    # 3. Injecte l'en-tete au-dessus du lecteur
    html = html.replace("<!-- Add any content above the cart here -->", ABOVE_HTML, 1)
    # 4. Injecte les sections en dessous du lecteur
    html = html.replace("<!-- Add content below the cart here -->", BELOW_HTML, 1)
    # 5. Cache-busting pour forcer le rechargement du binaire JS sur mobile et web
    import time
    ts = int(time.time())
    html = html.replace('e.src = "index.js";', f'e.src = "index.js?v={ts}";', 1)

    HTML_PATH.write_text(html, encoding="utf-8")

    # Synchronise aussi union_populaire.html et union_populaire.js pour compatibilite des liens
    shutil.copyfile(ROOT / "index.js", ROOT / "union_populaire.js")
    up_html = html.replace(f'e.src = "index.js?v={ts}";', f'e.src = "union_populaire.js?v={ts}";')
    (ROOT / "union_populaire.html").write_text(up_html, encoding="utf-8")
    print("index.html et union_populaire.html enrichis avec succes !")


if __name__ == "__main__":
    main()
