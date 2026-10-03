import requests
from bs4 import BeautifulSoup

# Nous avons choisi de scraper le classement de la Liga 25/26
url = "https://www.mercato.fr/equipe/girona-fc/classement"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"}

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table")
lignes = table.find_all("tr")

equipes = []

# On récupére les noms des equipes, leurs position en chiffre (1 - 20) et leurs logos
# On a utilisé ChatGpt pour la partie "equipes.append((pos, equipe, logo_url))"

for ligne in lignes:
    colonnes = ligne.find_all("td")

    if len(colonnes) > 2:
        pos = colonnes[1].text.strip()

        equipe = colonnes[2].text.strip()

        img_tag = ligne.find("img")
        logo_url = img_tag.get("src")

        equipes.append((pos, equipe, logo_url))

fichier = open("index.html", "w")

# Création de notre fichier HTML
fichier.write("""
<html>
<head>
    <title>Classement de la Liga 25/26</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background: linear-gradient(to bottom, red, orange, yellow);
        }

        #grand-titre {
        font-size: 30px;
        background: yellow;
        border: 5px;
        border-radius: 20px
        font-family: Roboto
        }

        #classement {
            background-color: white;
            width: 40%;
            margin: auto;
            padding: 10px;
            border-radius: 10px;
            margin-top: 40px;
            font-size: 22px;
            font-weight: bold;
        }

        #texte {
            background-color: white;
            width: 60%;
            margin: auto;
            padding: 15px;
            border-radius: 15px;
            font-family: Georgia, serif;
            font-size: 18px;
            margin-top: 30px;
        }

        table {
            border-collapse: collapse;
            width: 50%;
            margin: auto;
            margin-top: 30px;
            font-weight: bold; /* texte en gras */
        }

        th, td {
            border: 1px solid black;
            padding: 8px;
        }

        th {
            background-color: silver;
        }


        #titre-video {
            background-color: white;
            width: 40%;
            margin: auto;
            padding: 10px;
            border-radius: 10px;
            margin-top: 40px;
            font-size: 22px;
            font-weight: bold;
        }

        button {
            font-family: Impact, sans-serif;
            padding: 10px 20px;
            margin-top: 20px;
            border-radius: 10px;
            cursor: pointer;
        }

        #encadrement-accroche {
            margin-top: 40px;
            background-color: white;
            width: 60%;
            margin-left: auto;
            margin-right: auto;
            padding: 20px;
            border-radius: 15px;
            font-style: italic;
            font-size: 18px;
        }

        #encadrement-accroche img {
            width: 180px;
            border: 3px solid black;
            border-radius: 10px;
            margin-top: 10px;
        }

        .galerie {
            margin-top: 40px;
        }

        .galerie img {
            width: 300px;
            height: 300px;
            object-fit: cover;
            margin: 10px;
            border-radius: 10px;
        }

        video {
            width: 50%;
            max-widh: 500px;
            margin-top: 5px
        }
    </style>
</head>

<body>

    <b> <div id="grand-titre"> BIENVENUE AU CLASSEMENT de LALIGA 25/26 </div> </b>

    <div id="encadrement-accroche">
        « Ce qui est difficile dans un match facile, c’est de réussir à faire mal jouer l’adversaire. »
        – Johan Cruyff
        <br>
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTluPsUKyD1D1Dy2NvcpMcGY11YbW9NgJnMLg&s">
    </div>

    <p id="texte">
        La saison 2025-2026 de La Liga s’annonce passionnante, portée par une intensité retrouvée
        et une lutte serrée en tête du classement. Entre jeunes talents, nouvelles recrues et enjeux
        tactiques, cette édition promet un suspense incroyable.
    </p>

    <h2 id="classement"> Classement </h2>

    <table>
        <tr><th>POSITION</th><th> EQUIPE </th></tr>
""")



# Écriture des équipes dans le tableau
position = 1
for pos, equipe, logo in equipes:
    ligne = f'<tr> <td>{pos}</td> <td><img src ="{logo}" width ="30">{equipe}</td> </tr>\n'
    fichier.write(ligne)





# Continuation du html

fichier.write("""
    </table>

    <div id="titre-video"> Résumé du classico </div>

    <video controls> <source src="documents/site/classico.mp4" type="video/mp4"> </video>


    <br>

    <button onclick="window.location.href='https://www.laliga.com/es-FR';">
        Aller sur le site de La Liga
    </button>

    <div class="galerie">


        <img src="https://s.yimg.com/ny/api/res/1.2/TDn_5XfKuAzzwygkV1n3jg--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyNDI7aD04Mjg7Y2Y9d2VicA--/https://media.zenfs.com/fr/goal_fr_797/00483c47397c5c61d35a14d27878e115">

        <img src="https://assets.bundesliga.com/contender/2024/4/imago1034602594h.jpg?crop=0px,234px,4500px,2531px&fit=1140,1140">

        <img src="https://imgresizer.eurosport.com/unsafe/1200x0/filters:format(jpeg)/origin-imgresizer.eurosport.com/2024/08/25/4031194-81761528-2560-1440.jpg">
    </div>

</body>
</html>
""")


# Fermeture du fichier
fichier.close()

print("index.html généré avec succès !")