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

## For lærere

Se [laererveiledning.md](laererveiledning.md) for tidsplan, løsningsforslag og hvordan du henter dataene med `hent_data_gabrielle.py`.

## Datakilder

- Banedata: IBTrACS v04r01 (NOAA NCEI), med beste estimat fra National Hurricane Center
- Havtemperatur: NOAA OISST v2.1
- Atmosfære: ERA5 (Copernicus Climate Change Service, ECMWF)
- Hav i dybden: Argo
- Stasjonsdata fra Asorene: NHC Tropical Cyclone Report AL072025, tabell 2

Laget av Elisabeth Engum, Amalie Skram videregående skole.
