from bs4 import BeautifulSoup
import requests
import re
import csv

url = 'http://www.imdb.com/chart/top'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

films = soup.select('td.titleColumn')
liens = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
casting = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
sortie = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

imdb = []
# Ouvrir le fichier en mode écriture
fichier = open('250films.csv','w',encoding='utf-8')
# Créer l'writeret fichier
# writer = csv.writer(fichier, delimiter=',')
writer = csv.writer(fichier, lineterminator='\n')
for index in range(0, len(films)):
    films_string = films[index].get_text()
    film = (' '.join(films_string.split()).replace('.', ''))
    titre_du_film = film[len(str(index))+1:-7]
    annee = re.search('\((.*?)\)', films_string).group(1)
    place = film[:len(str(index))-(len(film))]
    data = {"titre_du_film": titre_du_film,
            "annee": annee,
            "place": place,
            "star_cast": casting[index],
            "rating": sortie[index],
            "vote": votes[index],
            "link": liens[index]}
    imdb.append(data)
    # Chaque élément de imdb correspond à une ligne
    writer.writerow(place)
    writer.writerow(titre_du_film)
    writer.writerow(annee)
    writer.writerow(casting[index])
    writer.writerow(' ')
fichier.close()
