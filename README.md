## Glasovanje na 

![slika esc](https://upload.wikimedia.org/wikipedia/en/thumb/e/e1/Eurovision_Song_Contest.svg/1331px-Eurovision_Song_Contest.svg.png)

Analiziral bom 26 tekmovanj za pesem Evrovizije (1994 - 2019).

#### Podatke bom dobil iz:
- [countryeconomy.com](https://countryeconomy.com/gdp?year=2014) za podatke o bdp,
- [cia.gov](https://www.cia.gov/library/publications/the-world-factbook/fields/281.html) za podatke o mejah,
- [investing.com](https://www.investing.com/currencies/usd-eur-historical-data) za podatke o EUR-USD tečajih,
- [data.world](https://data.world/datagraver/eurovision-song-contest-scores-1975-2019) za podatke o glasovanju na Evroviziji.

#### Ustvaril bom štiri datoteke s podatki:
- na katere države meji vsaka država,
- kakšen je bil posamezno leto bdp držav,
- komu je vsaka država posamezno leto dala točke in
- koliko točk so dobile države po letih.

#### Zanimalo me bo:
- Obstaja povezava med številom podeljenih točk med dvema državama in njuno geografkso bližino?
- Obstaja povezava med uspehom države in njeno gospodarsko razvitostjo?
- So bile katere države nadpovprečno / podpovprečno uspešne, ali vse približno enako?

------------------

#### Opombe po pobranih podatkih:
- Podatke iz prvih dveh virov sem pridobil ročno, iz zadnjih dveh pa sem jih prenesel kar v csv obliki.
- V mapi ```podatki``` so datoteke s podatki, ki jih generirajo sledeče datoteke:
  - ```zajem_podatkov_bdp.py``` shrani vsebine 26 spletnih strani iz [countryeconomy.com](https://countryeconomy.com/gdp?year=2014), tako da za vsako leto od 1994 do 2019 usvari ```bdp_{leto}```. Poleg tega ustvari ```bdp.csv```, kjer so v csv obliki shranjeni podatki o bdp vsake države vsako leto.
  - ```zajem_podatkov_meje.py``` shrani vsebino spletne strani iz [cia.gov](https://www.cia.gov/library/publications/the-world-factbook/fields/281.html) v ```meje``` in pare mejnih držav v ```meje.csv```.
  - v mapi ```podatki``` sta še datoteki ```bdp_tecaji.csv```, ki vsebuje tečaje EUR-USD skozi leta in je pobrana iz [investing.com](https://www.investing.com/currencies/usd-eur-historical-data), in ```esc.csv```, v kateri so podrobni glasovi na Evroviziji med državami skozi leta, in je pobrana iz [data.world](https://data.world/datagraver/eurovision-song-contest-scores-1975-2019).
  - iz ```esc.csv``` sem prek ```zajem_podatkov_esc.py``` izluščil še eno tabelo, kjer sem za vsako leto za sodelujoče države izračunal dosežene točke, in jo shranil v ```uvrstitve.csv```.
- v ```zajem_podatkov_orodja.py``` sem zbral in presonaliziral orodja iz [repozitorija predmeta](https://github.com/matijapretnar/programiranje-1).
