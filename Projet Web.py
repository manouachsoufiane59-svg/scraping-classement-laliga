from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


SOURCE_URL = "https://www.mercato.fr/equipe/girona-fc/classement"
OUTPUT_FILE = Path(__file__).resolve().with_name("index.html")
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
    )
}


def scrape_teams():
    response = requests.get(SOURCE_URL, headers=HEADERS, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("Le tableau du classement est introuvable sur la page source.")

    teams = []
    for row in table.find_all("tr"):
        columns = row.find_all("td")
        if len(columns) < 3:
            continue

        position = columns[1].get_text(" ", strip=True)
        name = columns[2].get_text(" ", strip=True)
        logo = row.find("img")
        logo_url = urljoin(SOURCE_URL, logo.get("src", "")) if logo else ""
        if position and name:
            teams.append((position, name, logo_url))

    if not teams:
        raise ValueError("Aucune équipe n’a été extraite. La structure de la page source a peut-être changé.")
    return teams


def render_page(teams):
    updated_at = datetime.now().astimezone().strftime("%d/%m/%Y à %H:%M")
    leader = escape(teams[0][1])
    rows = []

    for position, name, logo_url in teams:
        try:
            rank = int(position)
        except ValueError:
            rank = 0

        row_class = "top-three" if 1 <= rank <= 3 else ""
        logo = ""
        if logo_url:
            logo = (
                f'<img class="club-logo" src="{escape(logo_url, quote=True)}" '
                f'alt="" loading="lazy" onerror="this.hidden=true">'
            )
        rows.append(
            f'<tr class="{row_class}">'
            f'<td class="position">{escape(position)}</td>'
            f'<td><div class="club">{logo}<span>{escape(name)}</span></div></td>'
            "</tr>"
        )

    template = """<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Classement de La Liga généré à partir de données collectées sur le web.">
  <title>Classement de La Liga | Football Data</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #14251f;
      --muted: #64736d;
      --paper: #f5f7f4;
      --card: #ffffff;
      --line: #e4eae5;
      --green: #146b4b;
      --lime: #c8f169;
      --gold: #f2b84b;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }
    .hero {
      background: #10251e;
      color: white;
      padding: 58px 24px 82px;
      overflow: hidden;
      position: relative;
    }
    .hero::after {
      content: "";
      position: absolute;
      width: 310px;
      height: 310px;
      right: 8%;
      top: -190px;
      border: 1px solid rgba(200, 241, 105, .35);
      border-radius: 50%;
      box-shadow: 0 0 0 28px rgba(200, 241, 105, .04), 0 0 0 58px rgba(200, 241, 105, .04);
      pointer-events: none;
    }
    .hero-inner, main, footer { width: min(900px, calc(100% - 40px)); margin-inline: auto; }
    .eyebrow {
      color: var(--lime);
      font-size: .76rem;
      font-weight: 750;
      letter-spacing: .16em;
      text-transform: uppercase;
    }
    h1 { margin: 14px 0 10px; font-size: clamp(2rem, 6vw, 3.7rem); letter-spacing: -.045em; line-height: 1.04; }
    .subtitle { margin: 0; color: #c0cdc6; font-size: 1.02rem; }
    main { margin-top: -38px; position: relative; }
    .summary {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      box-shadow: 0 12px 36px rgba(20, 37, 31, .08);
      display: grid;
      grid-template-columns: 1fr 1fr;
      overflow: hidden;
    }
    .summary-item { padding: 21px 24px; }
    .summary-item + .summary-item { border-left: 1px solid var(--line); }
    .summary-label { color: var(--muted); display: block; font-size: .78rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    .summary-value { display: block; font-size: 1.15rem; font-weight: 750; margin-top: 5px; }
    .panel {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 18px;
      margin-top: 22px;
      overflow: hidden;
    }
    .panel-head { align-items: center; border-bottom: 1px solid var(--line); display: flex; flex-wrap: wrap; gap: 16px; justify-content: space-between; padding: 22px 24px; }
    h2 { font-size: 1.15rem; letter-spacing: -.02em; margin: 0; }
    .count { color: var(--muted); font-size: .9rem; margin: 4px 0 0; }
    .search {
      background: #f7f9f7;
      border: 1px solid var(--line);
      border-radius: 10px;
      color: var(--ink);
      font: inherit;
      min-width: min(230px, 100%);
      padding: 10px 13px;
    }
    .search:focus { border-color: var(--green); outline: 3px solid rgba(20, 107, 75, .13); }
    .table-wrap { overflow-x: auto; }
    table { border-collapse: collapse; min-width: 350px; width: 100%; }
    th { background: #f7f9f7; color: var(--muted); font-size: .72rem; font-weight: 750; letter-spacing: .1em; padding: 12px 24px; text-align: left; text-transform: uppercase; }
    td { border-top: 1px solid #edf1ed; padding: 12px 24px; }
    tbody tr:hover { background: #f7faf7; }
    .position { color: var(--muted); font-variant-numeric: tabular-nums; font-weight: 750; width: 90px; }
    .top-three .position { color: var(--green); }
    .club { align-items: center; display: flex; font-weight: 650; gap: 12px; }
    .club-logo { height: 30px; object-fit: contain; width: 30px; }
    .source { color: var(--muted); font-size: .86rem; padding: 17px 24px; }
    .source a { color: var(--green); font-weight: 650; text-decoration-thickness: 1px; text-underline-offset: 3px; }
    footer { color: var(--muted); font-size: .8rem; padding: 25px 0 35px; text-align: center; }
    @media (max-width: 560px) {
      .hero { padding: 44px 20px 70px; }
      .hero-inner, main, footer { width: min(100% - 28px, 900px); }
      .summary-item { padding: 17px; }
      .panel-head { align-items: stretch; padding: 18px; }
      .search { width: 100%; }
      th, td { padding-left: 17px; padding-right: 17px; }
    }
  </style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <span class="eyebrow">Projet de web scraping · Football</span>
      <h1>Classement de La Liga</h1>
      <p class="subtitle">Une page de consultation produite automatiquement à partir de données collectées sur le web.</p>
    </div>
  </header>
  <main>
    <section class="summary" aria-label="Résumé du classement">
      <div class="summary-item"><span class="summary-label">Équipes classées</span><strong class="summary-value">__TEAM_COUNT__ équipes</strong></div>
      <div class="summary-item"><span class="summary-label">Équipe en tête</span><strong class="summary-value">__LEADER__</strong></div>
    </section>
    <section class="panel" aria-labelledby="standings-title">
      <div class="panel-head">
        <div><h2 id="standings-title">Classement</h2><p class="count">Données récupérées le __UPDATED_AT__</p></div>
        <label><span class="visually-hidden"></span><input class="search" id="team-search" type="search" placeholder="Rechercher une équipe…" aria-label="Rechercher une équipe"></label>
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr><th scope="col">Position</th><th scope="col">Équipe</th></tr></thead>
          <tbody id="teams">__ROWS__</tbody>
        </table>
      </div>
      <p class="source">Source des données : <a href="__SOURCE_URL__" target="_blank" rel="noopener noreferrer">mercato.fr</a></p>
    </section>
  </main>
  <footer>Page générée avec Python, Requests et BeautifulSoup.</footer>
  <style>.visually-hidden { clip: rect(0,0,0,0); clip-path: inset(50%); height: 1px; overflow: hidden; position: absolute; white-space: nowrap; width: 1px; }</style>
  <script>
    const search = document.querySelector('#team-search');
    const rows = [...document.querySelectorAll('#teams tr')];
    search.addEventListener('input', () => {
      const query = search.value.trim().toLocaleLowerCase('fr');
      rows.forEach(row => {
        row.hidden = !row.textContent.toLocaleLowerCase('fr').includes(query);
      });
    });
  </script>
</body>
</html>
"""
    return (
        template.replace("__TEAM_COUNT__", str(len(teams)))
        .replace("__LEADER__", leader)
        .replace("__UPDATED_AT__", escape(updated_at))
        .replace("__ROWS__", "\n".join(rows))
        .replace("__SOURCE_URL__", SOURCE_URL)
    )


if __name__ == "__main__":
    try:
        page = render_page(scrape_teams())
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
            file.write(page)
        print(f"{OUTPUT_FILE.name} généré avec succès.")
    except requests.RequestException as error:
        raise SystemExit(f"Impossible de récupérer les données : {error}") from error
    except ValueError as error:
        raise SystemExit(str(error)) from error
