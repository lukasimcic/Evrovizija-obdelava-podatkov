import zajem_podatkov_orodja as orodja
import re
import os
import csv

url_bdp_seznam = [f'https://countryeconomy.com/gdp?year={leto}' for leto in range(1994, 2020)]
drugačne_države = {'Netherlands': 'The Netherlands', 'North Macedonia': 'Macedonia', 'Bosnia and Herzegovina': 'Bosnia & Herzegovina'}

konec_podatkov = 'Comparison: GDP per capita' # na spletni strani sta dve tabeli, jaz potrebujem prvo, ki se konča s tem nizom


# vzorci za iskanje:

vzorec_bloka = re.compile(
    r"year=1994'>.*?"
    r">1994<.*?"
    r"(M\..|€)<",
    flags=re.DOTALL)

vzorec_podatkov = re.compile(
    r"year=1994'>(?P<država>.*?) \[\+\].*"
    r'<td class="numero (dol|eur)".*?>(?P<bdp>.*?)<',
    flags=re.DOTALL)


# bdp bo oblike '1,859,310M.€' ali '8,555M.$', želim da bo le številka v evrih po ustreznem tečaju.

def uredi_bdp(niz, url):
    if '€' in niz:
        return int(niz.replace('M.€', '').replace(',', ''))
    else:
        with open(os.path.join(orodja.mapa, 'bdp_tecaji.csv'), newline='') as dat:
            reader = csv.reader(dat)
            for vrstica in reader:
                if vrstica[0] == 'May ' + url[-2:]:
                    tecaj = float(vrstica[1])
                    return int(tecaj * int(niz.replace('M.$', '').replace(',', '')))


def uredi_podatke(slovar, url):
    if slovar['država'] in orodja.države:
        slovar['bdp'] = uredi_bdp(slovar['bdp'], url)
        slovar['leto'] = url[-4:]
        return [slovar]
    else:
        return []


seznam_podatkov = []
for url in url_bdp_seznam:
    seznam_podatkov_za_leto = orodja.podatki_iz_strani(url, 'bdp_1994', vzorec_bloka, vzorec_podatkov, uredi_podatke, države=drugačne_države, zmanjsaj_stran=konec_podatkov)
    seznam_podatkov += seznam_podatkov_za_leto


orodja.zapisi_csv(seznam_podatkov, ['leto', 'država', 'bdp'], os.path.join(orodja.mapa, 'bdp.csv'))