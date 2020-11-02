# nekatere funkcije sem dobil iz predavanj Programiranja 1 (orodja iz vaje 2)

import csv
import os
import requests
import sys
import re
mapa = 'Evrovizija-obdelava-podatkov\\podatki'

# ker bom obdeloval spletne strani, ki vsebujejo podatke od vseh svetovnih držav,
# potrebujem množico vseh držav, ki so sodelovale na Evroviziji od 1994 naprej
države = set()
with open(os.path.join(mapa, 'esc.csv'), newline='') as dat:
    reader = csv.reader(dat)
    vsebina = list(reader)
    for vrstica in vsebina[1:]:
        seznam = vrstica[0].split(';')
        država = seznam[4]
        if seznam[0] > '1993' and država != '':
            if 'Macedonia' in država: # da se izognem 'F.Y.R. Macedonia' in 'North Macedonia'
                države.add('Macedonia')
            elif država == 'Serbia & Montenegro': # te države, ki je obstajala le nekaj let, ne bom posebej obravnaval
                pass
            else:
                države.add(država)

# nekatere države iz množice 'države' so drugače poimenovane kot na spletnih stran, ki jih bom obdeloval,
# zato bom napisal funkcijo, ki zamenja imena držav v pobranih datotekah z državami iz množice 'države'
def zamenjaj_države(vsebina, države):
    '''zamenja imena držav v pobranih datotekah z državami iz množice "države"'''
    for stara_država, nova_država in države.items():
        vsebina = re.sub(stara_država, nova_država, vsebina)
    return vsebina


def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False, mapa=mapa):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    pot = os.path.join(mapa, ime_datoteke)
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(pot) and not vsili_prenos:
            print('\n... shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('\n... stran ne obstaja!')
    else:
        os.makedirs(mapa, exist_ok=True)
        with open(pot, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('\n... shranjeno!')


def vsebina_datoteke(ime_datoteke, mapa=mapa):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    path = os.path.join(mapa, ime_datoteke)
    with open(path, encoding='utf-8') as datoteka:
        return datoteka.read()


def bloki(vsebina, vzorec_bloka):
    '''Iz vsebine naredi bloke, v vsakem bloku so informacije o mejah ene države'''
    return [blok.group(0) for blok in vzorec_bloka.finditer(vsebina)]


def izloci_podatke_iz_bloka(blok, vzorec_podatkov):
    zadetek = re.search(vzorec_podatkov, blok)
    if zadetek is not None:
        slovar = zadetek.groupdict()
        return slovar
    return None


def podatki_iz_strani(url, ime_datoteke, vzorec_bloka, vzorec_podatkov, uredi_podatke, države={}, zmanjsaj_stran=False):
    '''Naredi seznam slovarjev podatkov'''
    seznam = []
    shrani_spletno_stran(url, ime_datoteke)
    vsebina = vsebina_datoteke(ime_datoteke)
    if zmanjsaj_stran:
        vsebina = re.split(zmanjsaj_stran, vsebina)[0]
    vsebina = zamenjaj_države(vsebina, države)
    for blok in bloki(vsebina, vzorec_bloka):
        slovar = izloci_podatke_iz_bloka(blok, vzorec_podatkov)
        if slovar is not None:
            seznam += uredi_podatke(slovar, url)
    return seznam

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)
            