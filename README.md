# Orkanen Gabrielle

Dataoppgave i Geofag 2 (REA3043) om orkanen Gabrielle i Atlanterhavet, 17.–28. september 2025. Økten tar 120 minutter.

Elevene bruker ekte data til å svare på hvorfor Gabrielle ble så sterk så raskt, hvorfor den svekket seg, og hvordan Asorene kunne få orkankast fra en storm som ikke lenger var en tropisk syklon.

## For elever

**Se notatboken uten å installere noe.** Trykk på `orkanen_gabrielle_kjort.ipynb` i fillisten ovenfor. Det er en ferdig kjørt versjon, så du ser alle figurene og tallene rett i nettleseren.

**Vil du kjøre koden selv**, trenger du conda-miljøet `geofag2` fra guiden [Installere og åpne Jupyter Lab](https://pgelisa.github.io/geofag2-python-opendrift/).

**Hent filene**

1. Trykk den grønne knappen **Code** øverst på denne siden og velg **Download ZIP**.
2. Flytt zip-filen fra Nedlastinger til geofag-mappen din før du pakker den ut.
   - **Mac:** dobbeltklikk zip-filen i geofag-mappen.
   - **Windows:** høyreklikk zip-filen og velg **Pakk ut alle**. Velg geofag-mappen som mål.
3. Slett zip-filen fra Nedlastinger.

Kan du bruke git, går det også fint med `git clone`.

**Åpne notatboken**

```
conda activate geofag2
jupyter lab
```

Gå til mappen du pakket ut, og åpne `orkanen_gabrielle.ipynb`. Mappen `data` må ligge ved siden av notatboken.

## Hva kan du endre?

I cellene merket 🔧 kan du endre verdier og kjøre cellen på nytt. Dataene dekker bare en bestemt periode og et bestemt område. Velger du et tidspunkt utenfor, bruker notatboken det nærmeste tidspunktet som finnes i dataene. Da kan figuren se riktig ut selv om den viser en annen dag enn du tror, så sjekk alltid datoen i figurtittelen.

| Del | Variabel | Dette kan du velge |
|---|---|---|
| 1c | `TERSKEL` | Hvilken økning i vind (m/s per 24 timer) som regnes som rask intensivering |
| 2a | `DATO_KART` | En dato fra 14.09 til 30.09.2025 |
| 2c | `FOR`, `ETTER` | To datoer fra 14.09 til 30.09.2025 |
| 2c | `MAKS_AVSTAND_KM` | Hvor langt fra banen (km) koden leter etter største avkjøling. Koden leter bare innenfor 20–42° N og 70–40° V |
| 3a | `TIDER` | Tre tidspunkter fra 20.09 kl. 00 til 28.09 kl. 18 UTC, hver 6. time (kl. 00, 06, 12 eller 18) |
| 3b | `BOKS` | Hvor mange grader rundt sentrum vindskjæret regnes over |
| 3d | `FRA`, `TIL` | To av stasjonene Flores, Faial (08505), Faial (08506), Pico, Graciosa, Terceira og São Miguel. Skriv navnet nøyaktig slik |
| A | `MAKS_AVSTAND`, `BOYE` | Avstand fra banen (km) og eventuelt et bøyenummer fra listen notatboken skriver ut |
| B | `t` | Et tidspunkt fra 24.09 kl. 12 til 28.09 kl. 18 UTC, hver 6. time. Bare da finnes begge stormene |

**Hva dataene dekker**

| Data | Periode | Område | Oppløsning |
|---|---|---|---|
| Banen til Gabrielle | 17.09 kl. 18 til 28.09 kl. 18 UTC | Langs banen | Hver 6. time |
| Banen til Humberto | 24.09 kl. 12 til 01.10 kl. 12 UTC | Langs banen | Hver 6. time |
| Havtemperatur (OISST) | 14.09–30.09.2025 | 10–50° N, 80° V–0° | Ett kart per døgn, 0,25° |
| Atmosfære (ERA5) | 20.09 kl. 00 til 28.09 kl. 18 UTC | 20–50° N, 80° V–0° | Hver 6. time, 0,5° |
| Argo-bøyer | 08.09–07.10.2025 | 26–38° N, 66–50° V | 75 profiler fra 31 bøyer, 0–300 dbar |
| Stasjoner på Asorene | 26.09.2025 | 7 stasjoner | Bare største og minste verdi, ikke tidsserier |

Vindskjæret i 3b kan bare regnes ut mens stormen er inne i ERA5-området. De første dagene av banen, før 20.09, er derfor ikke med. Nær Portugal blir boksen rundt sentrum delvis liggende utenfor området.

## For lærere

Se [laererveiledning.md](laererveiledning.md) for tidsplan, løsningsforslag og hvordan du henter dataene med `hent_data_gabrielle.py`.

## Datakilder

- Banedata: IBTrACS v04r01 (NOAA NCEI), med beste estimat fra National Hurricane Center
- Havtemperatur: NOAA OISST v2.1
- Atmosfære: ERA5 (Copernicus Climate Change Service, ECMWF)
- Hav i dybden: Argo
- Stasjonsdata fra Asorene: NHC Tropical Cyclone Report AL072025, tabell 2

Laget av Elisabeth Engum, Amalie Skram videregående skole.
