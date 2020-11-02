import zajem_podatkov_orodja as orodja
import re
import os

url_meje = 'https://www.cia.gov/library/publications/the-world-factbook/fields/281.html'
drugačne_države = {'Czechia': 'Czech Republic', 'Netherlands': 'The Netherlands', 'North Macedonia': 'Macedonia', 'Bosnia and Herzegovina': 'Bosnia & Herzegovina', 'UK': 'United Kingdom'}


# vzorci za iskanje:

vzorec_bloka = re.compile(
    r"<td class='country'.*?"
    r"</div>\s*</div>",
    flags=re.DOTALL)

vzorec_podatkov = re.compile(
    r"<a href=.*?>(?P<država>.*?)</a>.*?"
    r"border countries \(\w{1,2}\):</span>(?P<meje>.*?)</div>\s*</div>",
    flags=re.DOTALL)


# meja bo oblike '\n    država1 8 km, drža va2 22 km, država3 3 km      '
# želim, da je oblike {država1, drža va2, država3}, kjer so upoštevane le države iz Evorvizije
def uredi_meje(niz):
    if niz == None:
        return None
    množica = set()
    for beseda in niz.strip().split(' '):
        for x in [država.split(' ') for država in orodja.države]:
            if beseda in x:
                država = str(x).replace('[', '').replace(']', '').replace(',', '').replace("'", '')
                množica.add(država)
    return množica


def uredi_podatke(slovar):
    seznam = []
    if slovar['država'] in orodja.države:
        for mejna_država in uredi_meje(slovar['meje']):
            seznam.append({'država': slovar['država'], 'meja': mejna_država})
    return seznam


seznam_podatkov = orodja.podatki_iz_strani(url_meje, 'meje', vzorec_bloka, vzorec_podatkov, uredi_podatke, drugačne_države)

# ostale so še otoške države, ki nimajo sosedov:
for država in orodja.države:
    if država not in [seznam_podatkov[i]['država'] for i in range(len(seznam_podatkov))]:
        seznam_podatkov.append({'država': država, 'meja': []})


orodja.zapisi_csv(seznam_podatkov, ['država', 'meja'], os.path.join(orodja.mapa, 'meje.csv'))