#!/usr/bin/env python3
"""Éditeur & Nettoyeur visuel de sprites PICO-8 dans le navigateur.

Lance un serveur web local léger et ouvre l'interface dans votre navigateur :
  python3 tools/sprite_cleaner.py [--port 8088]

Permet d'éditer pixel par pixel les sprites 16x16, 32x32 et 8x8 de tools/sprites.py,
avec prévisualisation en temps réel (échelle combat x3), palette PICO-8, raccourcis clavier,
détection des artefacts (pixels orphelins) et enregistrement direct dans le fichier source.
"""

import argparse
import http.server
import json
import re
import socketserver
import subprocess
import sys
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import sprites  # noqa: E402

PICO8_PAL = [
    "#000000", "#1D2B53", "#7E2553", "#008751",
    "#AB5236", "#5F574F", "#C2C3C7", "#FFF1E8",
    "#FF004D", "#FFA300", "#FFEC27", "#00E436",
    "#29ADFF", "#83769C", "#FF77A8", "#FFCCAA"
]

COLOR_NAMES = [
    "0 : Noir", "1 : Bleu nuit", "2 : Pourpre", "3 : Vert foncé",
    "4 : Marron", "5 : Gris foncé", "6 : Gris clair", "7 : Blanc",
    "8 : Rouge FI", "9 : Orange", "a : Jaune or", "b : Vert clair",
    "c : Cyan Phi", "d : Lavande", "e : Rose", "f : Peau / Chair"
]


def load_monster_names():
    names = {
        230: "Permanent QG (16x16)",
        128: "Boss 1 - Édito-Star (32x32)",
        132: "Boss 2 - L'Hydre financière (32x32)",
        136: "Boss 3 - L'Austéritaire (32x32)",
        140: "Boss 4 - L'Oligarque (32x32)",
        192: "Boss 5 - Le Monarque (32x32)",
    }
    data_file = ROOT / "src/data.lua"
    if data_file.exists():
        text = data_file.read_text(encoding="utf-8")
        m = re.search(r'mons=tbl\("([^"]+)"\)', text)
        if m:
            for entry in m.group(1).split("|"):
                parts = entry.split(",")
                if len(parts) >= 9:
                    try:
                        name = parts[0].strip().title()
                        sid = int(parts[8])
                        names[sid] = f"{name} (16x16)"
                    except ValueError:
                        pass
    return names


def get_all_sprites():
    m_names = load_monster_names()
    items = []

    # Monstres
    for sid, rows in sorted(sprites.MONSTERS.items()):
        name = m_names.get(sid, f"Opposant #{sid} (16x16)")
        items.append({
            "id": sid,
            "category": "Monstres (16x16)",
            "name": name,
            "size": 16,
            "rows": rows
        })

    # Boss
    for sid, rows in sorted(sprites.BOSSES.items()):
        name = m_names.get(sid, f"Boss #{sid} (32x32)")
        items.append({
            "id": sid,
            "category": "Boss (32x32)",
            "name": name,
            "size": 32,
            "rows": rows
        })

    # Tuiles
    tile_names = {
        1: "Eau profonde", 2: "Gué / Rivière", 3: "Plaine / Herbe",
        4: "Forêt", 5: "Ronces", 6: "Montagne", 7: "Col",
        8: "Chaîne", 9: "Sable / Plage", 10: "Région dévastée",
        16: "Donjon - Mur", 17: "Donjon - Sol", 18: "Donjon - Sortie",
        19: "Donjon - Coffre", 20: "QG - Table", 21: "QG - Lit",
        22: "QG - Étagère", 23: "QG - Affiche",
        32: "Héros (Immobile)", 33: "Héros (Marche)",
    }
    for sid, rows in sorted(sprites.TILES.items()):
        name = tile_names.get(sid, f"Tuile #{sid}")
        items.append({
            "id": sid,
            "category": "Tuiles & Décors (8x8)",
            "name": f"{name} (8x8)",
            "size": 8,
            "rows": rows
        })

    return items


def save_sprite_to_file(sprite_id, size, new_rows):
    sprites_file = ROOT / "tools/sprites.py"
    content = sprites_file.read_text(encoding="utf-8")

    pattern = rf'([ \t]+{sprite_id}:[ \t]*\[\n)(?:[ \t]*\"[^\"]+\",?\n)+([ \t]*\],?)'
    match = re.search(pattern, content)
    if not match:
        raise ValueError(f"Sprite #{sprite_id} introuvable dans tools/sprites.py")

    header = match.group(1)
    footer = match.group(2)

    indent = " " * 8
    body = "".join(f'{indent}"{r}",\n' for r in new_rows)
    replacement = f"{header}{body}{footer}"

    new_content = content[:match.start()] + replacement + content[match.end():]
    sprites_file.write_text(new_content, encoding="utf-8")

    # Recharger le module python en mémoire
    import importlib
    importlib.reload(sprites)

    # Reconstruire les cartouches PICO-8
    try:
        subprocess.run([sys.executable, str(ROOT / "tools/build.py"), "--reset-gfx"],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(f"Warning build.py: {e}")


HTML_PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Nettoyeur de Sprites PICO-8 — L'Union Populaire RPG</title>
<style>
  :root {
    --bg: #12141c;
    --panel: #1a1e2b;
    --border: #2a3147;
    --text: #e6e9f2;
    --muted: #8b93a7;
    --accent: #29adff;
    --danger: #ff004d;
    --success: #00e436;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
    display: flex;
    height: 100vh;
    overflow: hidden;
  }
  /* Sidebar */
  #sidebar {
    width: 290px;
    background: var(--panel);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
  }
  #search-box {
    padding: 12px;
    border-bottom: 1px solid var(--border);
  }
  #search-box input {
    width: 100%;
    padding: 8px 12px;
    background: #0f121a;
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    font-size: 13px;
  }
  #sprite-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px;
  }
  .category-title {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--muted);
    padding: 10px 8px 4px 8px;
    letter-spacing: 0.5px;
  }
  .sprite-item {
    display: flex;
    align-items: center;
    padding: 7px 10px;
    border-radius: 6px;
    cursor: pointer;
    margin-bottom: 2px;
    font-size: 13px;
    gap: 10px;
    transition: background 0.15s;
  }
  .sprite-item:hover { background: rgba(255,255,255,0.06); }
  .sprite-item.active { background: #26324b; color: var(--accent); font-weight: 600; }
  .sprite-thumb {
    width: 24px;
    height: 24px;
    image-rendering: pixelated;
    border: 1px solid rgba(255,255,255,0.1);
    background: #000;
    border-radius: 3px;
    flex-shrink: 0;
  }
  /* Main area */
  #main {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  #toolbar {
    height: 56px;
    background: var(--panel);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 20px;
    gap: 12px;
  }
  .btn {
    padding: 8px 14px;
    background: #252b3d;
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text);
    font-size: 13px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s;
  }
  .btn:hover { background: #323a52; border-color: #434e6e; }
  .btn-primary { background: #008751; border-color: #00e436; color: #fff; font-weight: 600; }
  .btn-primary:hover { background: #00a463; }
  .tool-btn.active { background: var(--accent); color: #000; border-color: var(--accent); font-weight: bold; }
  #workspace {
    flex: 1;
    display: flex;
    overflow: hidden;
  }
  #editor-pane {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    user-select: none;
    overflow: auto;
    padding: 20px;
  }
  #canvas-container {
    position: relative;
    border: 2px solid #3c445c;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    background: repeating-conic-gradient(#1c2130 0% 25%, #151824 0% 50%) 50% / 16px 16px;
  }
  canvas#editor-canvas {
    display: block;
    image-rendering: pixelated;
    cursor: crosshair;
  }
  /* Color Palette */
  #palette-bar {
    margin-top: 18px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    background: var(--panel);
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid var(--border);
  }
  .swatch {
    width: 32px;
    height: 32px;
    border-radius: 5px;
    cursor: pointer;
    border: 2px solid transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: bold;
    color: #fff;
    text-shadow: 0 1px 2px #000;
    transition: transform 0.1s;
  }
  .swatch:hover { transform: scale(1.1); }
  .swatch.active { border-color: #fff; box-shadow: 0 0 0 2px var(--accent); }
  .swatch-transparent {
    background: repeating-conic-gradient(#444 0% 25%, #222 0% 50%) 50% / 8px 8px !important;
  }
  /* Right preview panel */
  #preview-pane {
    width: 320px;
    background: var(--panel);
    border-left: 1px solid var(--border);
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow-y: auto;
  }
  .panel-section {
    background: #141722;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
  }
  .panel-title {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 12px;
  }
  #preview-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }
  .preview-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }
  .preview-box span { font-size: 11px; color: var(--muted); }
  .preview-canvas {
    image-rendering: pixelated;
    border: 1px solid #3c445c;
    border-radius: 4px;
  }
  /* Toast notification */
  #toast {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: #008751;
    color: #fff;
    padding: 12px 20px;
    border-radius: 8px;
    font-weight: 600;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.25s ease;
    pointer-events: none;
    z-index: 1000;
  }
  #toast.show { opacity: 1; transform: translateY(0); }
  .badge {
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 11px;
    background: rgba(255,255,255,0.1);
  }
</style>
</head>
<body>

<div id="sidebar">
  <div id="search-box">
    <input type="text" id="filter-input" placeholder="Rechercher un sprite...">
  </div>
  <div id="sprite-list"></div>
</div>

<div id="main">
  <div id="toolbar">
    <div style="font-weight:700; font-size:15px;" id="current-title">Sprite 64</div>
    <span class="badge" id="current-dim">16x16</span>
    <div style="flex:1"></div>
    <button class="btn tool-btn active" data-tool="pencil" title="Crayon (1)">✏️ Crayon</button>
    <button class="btn tool-btn" data-tool="eraser" title="Gomme (.)">🧹 Gomme</button>
    <button class="btn tool-btn" data-tool="fill" title="Remplissage (G)">🪣 Pot</button>
    <button class="btn tool-btn" data-tool="picker" title="Pipette (Alt+Click)">💧 Pipette</button>
    <div style="width:1px; height:24px; background:var(--border);"></div>
    <button class="btn" id="btn-undo" title="Annuler (Ctrl+Z)">↩️</button>
    <button class="btn" id="btn-redo" title="Rétablir (Ctrl+Y)">↪️</button>
    <button class="btn" id="btn-revert" title="Réinitialiser à la version disque">🔄 Réinitialiser</button>
    <button class="btn btn-primary" id="btn-save" title="Enregistrer dans tools/sprites.py (Ctrl+S)">💾 Enregistrer</button>
  </div>

  <div id="workspace">
    <div id="editor-pane">
      <div id="canvas-container">
        <canvas id="editor-canvas"></canvas>
      </div>
      <div id="palette-bar"></div>
    </div>

    <div id="preview-pane">
      <div class="panel-section">
        <div class="panel-title">Prévisualisation Jeu</div>
        <div id="preview-container">
          <div class="preview-box">
            <span>Échelle combat réelle (x3)</span>
            <canvas id="prev-battle" class="preview-canvas"></canvas>
          </div>
          <div class="preview-box">
            <span>Taille native (1x) & Zoom (2x)</span>
            <div style="display:flex; gap:12px; align-items:flex-end;">
              <canvas id="prev-1x" class="preview-canvas"></canvas>
              <canvas id="prev-2x" class="preview-canvas"></canvas>
            </div>
          </div>
        </div>
      </div>

      <div class="panel-section">
        <div class="panel-title">Fond de test</div>
        <div style="display:flex; gap:6px; flex-wrap:wrap;">
          <button class="btn btn-bg active" data-bg="#161B2A">Ardoise</button>
          <button class="btn btn-bg" data-bg="#000000">Noir</button>
          <button class="btn btn-bg" data-bg="#FFF1E8">Blanc</button>
          <button class="btn btn-bg" data-bg="arena">Arène Combat</button>
        </div>
      </div>

      <div class="panel-section">
        <div class="panel-title">Inspecteur Anti-Artefacts</div>
        <div id="artifact-stats" style="font-size:12px; line-height:1.6; color:var(--muted);">
          Pixels opaques : <b id="stat-opaque" style="color:var(--text);">0</b><br>
          Pixels orphelins (isolés) : <b id="stat-orphan" style="color:var(--success);">0</b><br>
          Couleurs utilisées : <b id="stat-colors" style="color:var(--text);">0/16</b>
        </div>
        <button class="btn" id="btn-copy-py" style="width:100%; margin-top:12px; justify-content:center;">📋 Copier matrice Python</button>
      </div>
    </div>
  </div>
</div>

<div id="toast"></div>

<script>
const PICO_PAL = [
  "#000000", "#1D2B53", "#7E2553", "#008751",
  "#AB5236", "#5F574F", "#C2C3C7", "#FFF1E8",
  "#FF004D", "#FFA300", "#FFEC27", "#00E436",
  "#29ADFF", "#83769C", "#FF77A8", "#FFCCAA"
];
const HEX_KEYS = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"];

let spritesData = [];
let currentSprite = null;
let grid = []; // 2D array of char ('0'..'f' or '.')
let currentSize = 16;
let currentColor = "0";
let currentTool = "pencil";
let testBg = "#161B2A";
let undoStack = [];
let redoStack = [];
let isDrawing = false;

// DOM
const editorCanvas = document.getElementById("editor-canvas");
const ctx = editorCanvas.getContext("2d");
const prev1x = document.getElementById("prev-1x");
const prev2x = document.getElementById("prev-2x");
const prevBattle = document.getElementById("prev-battle");

async function init() {
  buildPalette();
  bindEvents();
  await loadSprites();
  // Selectionner par defaut le sprite 64 s'il existe
  const target = spritesData.find(s => s.id === 64) || spritesData[0];
  if (target) selectSprite(target.id);
}

function buildPalette() {
  const bar = document.getElementById("palette-bar");
  bar.innerHTML = "";
  // Bouton transparent
  const tSwatch = document.createElement("div");
  tSwatch.className = "swatch swatch-transparent";
  tSwatch.title = "Transparent (.)";
  tSwatch.dataset.color = ".";
  tSwatch.innerText = "X";
  tSwatch.onclick = () => selectColor(".");
  bar.appendChild(tSwatch);

  // 16 couleurs
  for (let i = 0; i < 16; i++) {
    const sw = document.createElement("div");
    sw.className = "swatch" + (i === 0 ? " active" : "");
    sw.style.background = PICO_PAL[i];
    sw.dataset.color = HEX_KEYS[i];
    sw.title = `${HEX_KEYS[i]} : ${PICO_PAL[i]}`;
    sw.innerText = HEX_KEYS[i];
    sw.onclick = () => selectColor(HEX_KEYS[i]);
    bar.appendChild(sw);
  }
}

function selectColor(c) {
  currentColor = c;
  document.querySelectorAll(".swatch").forEach(s => {
    s.classList.toggle("active", s.dataset.color === c);
  });
}

async function loadSprites() {
  const res = await fetch("/api/sprites");
  spritesData = await res.json();
  renderSpriteList();
}

function renderSpriteList(filter = "") {
  const list = document.getElementById("sprite-list");
  list.innerHTML = "";
  let lastCat = "";
  const f = filter.toLowerCase();

  spritesData.forEach(s => {
    if (f && !s.name.toLowerCase().includes(f) && !String(s.id).includes(f)) return;

    if (s.category !== lastCat) {
      lastCat = s.category;
      const t = document.createElement("div");
      t.className = "category-title";
      t.innerText = lastCat;
      list.appendChild(t);
    }

    const item = document.createElement("div");
    item.className = "sprite-item" + (currentSprite && currentSprite.id === s.id ? " active" : "");
    item.onclick = () => selectSprite(s.id);

    const thumb = document.createElement("canvas");
    thumb.className = "sprite-thumb";
    thumb.width = s.size;
    thumb.height = s.size;
    drawThumb(thumb, s.rows, s.size);

    const label = document.createElement("span");
    label.innerText = `#${s.id} ${s.name}`;

    item.appendChild(thumb);
    item.appendChild(label);
    list.appendChild(item);
  });
}

function drawThumb(canvas, rows, size) {
  const tctx = canvas.getContext("2d");
  tctx.clearRect(0, 0, size, size);
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const c = rows[y][x];
      if (c !== ".") {
        tctx.fillStyle = PICO_PAL[parseInt(c, 16)];
        tctx.fillRect(x, y, 1, 1);
      }
    }
  }
}

function selectSprite(id) {
  const s = spritesData.find(item => item.id === id);
  if (!s) return;
  currentSprite = s;
  currentSize = s.size;
  grid = s.rows.map(r => r.split(""));
  undoStack = [];
  redoStack = [];

  document.getElementById("current-title").innerText = s.name;
  document.getElementById("current-dim").innerText = `${s.size}x${s.size}`;

  document.querySelectorAll(".sprite-item").forEach(item => {
    item.classList.toggle("active", item.innerText.includes(`#${s.id} `));
  });

  setupCanvas();
  render();
}

function setupCanvas() {
  const cellSize = currentSize === 32 ? 14 : currentSize === 16 ? 26 : 40;
  editorCanvas.width = currentSize * cellSize;
  editorCanvas.height = currentSize * cellSize;
  editorCanvas.dataset.cellSize = cellSize;

  prev1x.width = currentSize;
  prev1x.height = currentSize;

  prev2x.width = currentSize * 2;
  prev2x.height = currentSize * 2;

  const battleScale = currentSize === 32 ? 2 : 3;
  prevBattle.width = currentSize * battleScale * 2;
  prevBattle.height = currentSize * battleScale * 2;
}

function pushUndo() {
  undoStack.push(grid.map(row => [...row]));
  if (undoStack.length > 50) undoStack.shift();
  redoStack = [];
}

function undo() {
  if (undoStack.length === 0) return;
  redoStack.push(grid.map(row => [...row]));
  grid = undoStack.pop();
  render();
}

function redo() {
  if (redoStack.length === 0) return;
  undoStack.push(grid.map(row => [...row]));
  grid = redoStack.pop();
  render();
}

function render() {
  const cellSize = parseInt(editorCanvas.dataset.cellSize);
  ctx.clearRect(0, 0, editorCanvas.width, editorCanvas.height);

  for (let y = 0; y < currentSize; y++) {
    for (let x = 0; x < currentSize; x++) {
      const c = grid[y][x];
      if (c !== ".") {
        ctx.fillStyle = PICO_PAL[parseInt(c, 16)];
        ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
      }
      // Grille
      ctx.strokeStyle = "rgba(255,255,255,0.07)";
      ctx.lineWidth = 1;
      ctx.strokeRect(x * cellSize, y * cellSize, cellSize, cellSize);
    }
  }

  // Previews
  renderPreview(prev1x, 1);
  renderPreview(prev2x, 2);
  renderBattlePreview();
  updateStats();
}

function renderPreview(canvas, scale) {
  const pctx = canvas.getContext("2d");
  pctx.clearRect(0, 0, canvas.width, canvas.height);
  if (testBg !== "arena") {
    pctx.fillStyle = testBg;
    pctx.fillRect(0, 0, canvas.width, canvas.height);
  }
  for (let y = 0; y < currentSize; y++) {
    for (let x = 0; x < currentSize; x++) {
      const c = grid[y][x];
      if (c !== ".") {
        pctx.fillStyle = PICO_PAL[parseInt(c, 16)];
        pctx.fillRect(x * scale, y * scale, scale, scale);
      }
    }
  }
}

function renderBattlePreview() {
  const pctx = prevBattle.getContext("2d");
  const w = prevBattle.width;
  const h = prevBattle.height;
  pctx.clearRect(0, 0, w, h);

  if (testBg === "arena") {
    // Fond decor combat PICO-8
    pctx.fillStyle = "#1D2B53";
    pctx.fillRect(0, 0, w, h);
    pctx.fillStyle = "#008751";
    pctx.fillRect(0, h * 0.65, w, h * 0.35);
  } else {
    pctx.fillStyle = testBg;
    pctx.fillRect(0, 0, w, h);
  }

  const scale = currentSize === 32 ? 3 : 5;
  const ox = Math.floor((w - currentSize * scale) / 2);
  const oy = Math.floor((h - currentSize * scale) / 2);

  for (let y = 0; y < currentSize; y++) {
    for (let x = 0; x < currentSize; x++) {
      const c = grid[y][x];
      if (c !== ".") {
        pctx.fillStyle = PICO_PAL[parseInt(c, 16)];
        pctx.fillRect(ox + x * scale, oy + y * scale, scale, scale);
      }
    }
  }
}

function updateStats() {
  let opaque = 0;
  let usedColors = new Set();
  let orphans = 0;

  for (let y = 0; y < currentSize; y++) {
    for (let x = 0; x < currentSize; x++) {
      const c = grid[y][x];
      if (c !== ".") {
        opaque++;
        usedColors.add(c);
        // Test orphelin : aucun voisin orthogonal ou diagonal non transparent
        let hasNeighbor = false;
        for (let dy = -1; dy <= 1; dy++) {
          for (let dx = -1; dx <= 1; dx++) {
            if (dx === 0 && dy === 0) continue;
            const ny = y + dy, nx = x + dx;
            if (ny >= 0 && ny < currentSize && nx >= 0 && nx < currentSize) {
              if (grid[ny][nx] !== ".") hasNeighbor = true;
            }
          }
        }
        if (!hasNeighbor) orphans++;
      }
    }
  }

  document.getElementById("stat-opaque").innerText = opaque;
  const orphanEl = document.getElementById("stat-orphan");
  orphanEl.innerText = orphans;
  orphanEl.style.color = orphans > 0 ? "var(--danger)" : "var(--success)";
  document.getElementById("stat-colors").innerText = `${usedColors.size}/16`;
}

function getGridPos(e) {
  const rect = editorCanvas.getBoundingClientRect();
  const cellSize = parseInt(editorCanvas.dataset.cellSize);
  const x = Math.floor((e.clientX - rect.left) / cellSize);
  const y = Math.floor((e.clientY - rect.top) / cellSize);
  return { x: Math.max(0, Math.min(currentSize - 1, x)), y: Math.max(0, Math.min(currentSize - 1, y)) };
}

function setPixel(x, y, color) {
  if (grid[y][x] === color) return;
  grid[y][x] = color;
  render();
}

function floodFill(startX, startY, targetCol, replCol) {
  if (targetCol === replCol) return;
  const queue = [[startX, startY]];
  while (queue.length > 0) {
    const [x, y] = queue.pop();
    if (x < 0 || x >= currentSize || y < 0 || y >= currentSize) continue;
    if (grid[y][x] !== targetCol) continue;
    grid[y][x] = replCol;
    queue.push([x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]);
  }
  render();
}

function bindEvents() {
  editorCanvas.onmousedown = (e) => {
    const { x, y } = getGridPos(e);
    pushUndo();

    if (e.button === 2 || currentTool === "eraser") {
      setPixel(x, y, ".");
    } else if (currentTool === "picker" || e.altKey) {
      selectColor(grid[y][x]);
      return;
    } else if (currentTool === "fill") {
      floodFill(x, y, grid[y][x], currentColor);
    } else {
      setPixel(x, y, currentColor);
    }
    isDrawing = true;
  };

  window.onmousemove = (e) => {
    if (!isDrawing) return;
    const { x, y } = getGridPos(e);
    if (e.buttons === 2 || currentTool === "eraser") {
      setPixel(x, y, ".");
    } else if (e.buttons === 1 && currentTool === "pencil") {
      setPixel(x, y, currentColor);
    }
  };

  window.onmouseup = () => { isDrawing = false; };
  editorCanvas.oncontextmenu = (e) => e.preventDefault();

  // Outils
  document.querySelectorAll(".tool-btn").forEach(b => {
    b.onclick = () => {
      document.querySelectorAll(".tool-btn").forEach(t => t.classList.remove("active"));
      b.classList.add("active");
      currentTool = b.dataset.tool;
    };
  });

  // Fonds
  document.querySelectorAll(".btn-bg").forEach(b => {
    b.onclick = () => {
      document.querySelectorAll(".btn-bg").forEach(t => t.classList.remove("active"));
      b.classList.add("active");
      testBg = b.dataset.bg;
      render();
    };
  });

  // Actions
  document.getElementById("btn-undo").onclick = undo;
  document.getElementById("btn-redo").onclick = redo;
  document.getElementById("btn-revert").onclick = () => {
    if (confirm("Réinitialiser ce sprite à la version sauvegardée ?")) {
      grid = currentSprite.rows.map(r => r.split(""));
      undoStack = [];
      redoStack = [];
      render();
      showToast("Sprite réinitialisé");
    }
  };

  document.getElementById("btn-save").onclick = saveCurrentSprite;
  document.getElementById("btn-copy-py").onclick = copyPythonMatrix;

  document.getElementById("filter-input").oninput = (e) => {
    renderSpriteList(e.target.value);
  };

  // Raccourcis clavier
  window.onkeydown = (e) => {
    if (e.target.tagName === "INPUT") return;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") {
      e.preventDefault();
      if (e.shiftKey) redo(); else undo();
    } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "y") {
      e.preventDefault();
      redo();
    } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
      e.preventDefault();
      saveCurrentSprite();
    } else if (HEX_KEYS.includes(e.key.toLowerCase())) {
      selectColor(e.key.toLowerCase());
    } else if (e.key === "." || e.key === "x" || e.key === "X") {
      selectColor(".");
    } else if (e.key.toLowerCase() === "b") {
      document.querySelector('[data-tool="pencil"]').click();
    } else if (e.key.toLowerCase() === "e") {
      document.querySelector('[data-tool="eraser"]').click();
    } else if (e.key.toLowerCase() === "g") {
      document.querySelector('[data-tool="fill"]').click();
    }
  };
}

async function saveCurrentSprite() {
  if (!currentSprite) return;
  const rows = grid.map(r => r.join(""));
  try {
    const res = await fetch("/api/save", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: currentSprite.id, size: currentSize, rows })
    });
    const data = await res.json();
    if (data.success) {
      currentSprite.rows = rows;
      showToast(`✅ #${currentSprite.id} enregistré dans sprites.py et cartouche recompilée !`);
      renderSpriteList(document.getElementById("filter-input").value);
    } else {
      alert("Erreur d'enregistrement : " + data.error);
    }
  } catch (err) {
    alert("Erreur réseau : " + err);
  }
}

function copyPythonMatrix() {
  if (!currentSprite) return;
  const rows = grid.map(r => `        "${r.join("")}",`).join("\\n");
  const code = `    ${currentSprite.id}: [\\n${rows}\\n    ],`;
  navigator.clipboard.writeText(code).then(() => {
    showToast("📋 Matrice Python copiée dans le presse-papier !");
  });
}

function showToast(msg) {
  const t = document.getElementById("toast");
  t.innerText = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 3000);
}

window.onload = init;
</script>
</body>
</html>
"""


class SpriteEditorHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/" or url.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif url.path == "/api/sprites":
            sprites_list = get_all_sprites()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(sprites_list).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        url = urlparse(self.path)
        if url.path == "/api/save":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode("utf-8"))
                sid = int(data["id"])
                size = int(data["size"])
                rows = data["rows"]
                save_sprite_to_file(sid, size, rows)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Silence HTTP logs
        return


def main():
    parser = argparse.ArgumentParser(description="Éditeur de sprites PICO-8 local.")
    parser.add_argument("--port", type=int, default=8088, help="Port local (défaut 8088)")
    parser.add_argument("--no-open", action="store_true", help="Ne pas ouvrir le navigateur automatiquement")
    args = parser.parse_args()

    port = args.port
    # Trouver un port libre si 8088 est occupé
    for p in range(port, port + 20):
        try:
            server = socketserver.TCPServer(("127.0.0.1", p), SpriteEditorHandler)
            port = p
            break
        except OSError:
            continue
    else:
        print("Erreur : impossible de lier un port local.")
        sys.exit(1)

    url = f"http://localhost:{port}"
    print(f"✨ Éditeur de sprites PICO-8 démarré sur {url}")
    print("👉 Appuyez sur Ctrl+C pour arrêter le serveur.")

    if not args.no_open:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt de l'éditeur.")


if __name__ == "__main__":
    main()
