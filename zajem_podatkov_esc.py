import zajem_podatkov_orodja as orodja
import csv
import os


# naredimo slovar slovarjev za ustavljanje podatkov iz csv datoteke
slovar = {}
for leto in range(1994, 2020):
    slovar[leto] = {}


# noter ustavimo podatke
with open(os.path.join(orodja.mapa, 'esc.csv'), newline='') as dat:
    reader = csv.DictReader(dat, delimiter=';')
    for vrstica in reader:
        leto, država, točke = int(vrstica['Year']), vrstica['To country'], int(vrstica['Points      '])
        
        if leto < 1994 or vrstica['(semi-) final'] != 'f': # upoštevam le finalna tekmovanja od 1994 naprej
            continue
        elif država == 'Serbia & Montenegro': # te države, ki je obstajala le nekaj let, ne bom posebej obravnaval
            continue
        elif 'Macedonia' in država: # da se izognem 'F.Y.R. Macedonia' in 'North Macedonia'
                država = 'Macedonia'
        
        elif vrstica['From country'] not in slovar[leto]: # dodamo še države, ki se niso uvrstile v finale. Te bodo imele 0 točk
            slovar[leto][vrstica['From country']] = 0

        if država not in slovar[leto]:
            slovar[leto][država] = točke
        else:
            slovar[leto][država] += točke


# preuredimo slovar slovarjev v seznam slovarjev
seznam_podatkov = []
for leto in slovar:
    for država in slovar[leto]:
        if leto >= 2016: # leta 2016 so spremenili točkovni sistem, tako da se štejejo dvojne točke
            točke = slovar[leto][država] // 2
        else:
            točke = slovar[leto][država]
        seznam_podatkov.append({'leto': leto, 'država': država, 'točke': točke})


orodja.zapisi_csv(seznam_podatkov, ['leto', 'država', 'točke'], os.path.join(orodja.mapa, 'uvrstitve.csv'))