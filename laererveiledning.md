# Orkanen Gabrielle – lærerveiledning

Økt på 120 minutter i Geofag 2. Elevene jobber i `orkanen_gabrielle.ipynb` i JupyterLab i conda-miljøet `geofag2`. Notatboken bruker bare pakkene fra Miniforge-guiden (numpy, pandas, matplotlib, xarray, netcdf4, cartopy).

**Faglig innhold:** tropiske sykloner som varmemaskin, rask intensivering, havtemperatur og 26,5 °C-grensen, kaldt kjølvann (blanding og Ekman-pumping), vindskjær, ekstratropisk overgang, trykkgradient og vind, middelvind og vindkast, og usikkerhet i data.

## Mappestruktur

```
orkanen-gabrielle/
├── orkanen_gabrielle.ipynb       elevnotatboken
├── hent_data_gabrielle.py        kjøres én gang av læreren
├── laererveiledning.md
└── data/
    ├── asorene_stasjoner_gabrielle.csv            følger med (NHC-rapporten, tabell 2)
    ├── gabrielle_bane_nhc_tabell1_utdrag.csv      følger med (reserve, fra 21.09)
    ├── gabrielle_bane.csv                         lages av skriptet
    ├── humberto_bane.csv                          lages av skriptet
    ├── oisst_gabrielle.nc                         lages av skriptet
    ├── era5_bakke.nc                              lages av skriptet (--era5)
    ├── era5_trykkflater.nc                        lages av skriptet (--era5)
    └── argo_gabrielle.csv                         lages av skriptet (--argo)
```

Notatboken leser filene fra `data/` ved siden av seg selv. Legg hele mappen i repoet, så kan elevene klone repoet eller laste ned zip-fila fra GitHub og pakke den ut i geofag-mappen sin. Da slipper de å bruke Nedlastinger-mappen.

## Forberedelse (ca. 30 min, én gang)

1. Installer pakkene som bare du trenger:
   ```
   conda activate geofag2
   conda install -c conda-forge cdsapi argopy
   ```
2. Lag en konto på Copernicus Climate Data Store (cds.climate.copernicus.eu). Godta lisensen for ERA5, og legg API-nøkkelen i `~/.cdsapirc` slik det står på siden «How to API».
3. Kjør skriptet fra mappen `orkanen-gabrielle`:
   ```
   python hent_data_gabrielle.py --alt
   ```
4. Åpne notatboken og kjør alle cellene (Run → Run All Cells). Sjekk figurene og fyll inn tallene i løsningsforslaget nedenfor.

Filene blir små fordi skriptet lagrer komprimerte 32-biters tall (anslag: OISST ca. 3–5 MB, ERA5 til sammen ca. 10–15 MB).

### ERA5 manuelt (hvis cdsapi ikke virker)

| | Bakke | Trykkflater |
|---|---|---|
| Datasett | ERA5 hourly data on single levels from 1940 to present | ERA5 hourly data on pressure levels from 1940 to present |
| Produkttype | Reanalysis | Reanalysis |
| Variabler | Mean sea level pressure, 10m u-component of wind, 10m v-component of wind | U-component of wind, V-component of wind, Temperature |
| Trykknivå | – | 200, 500, 850 hPa |
| Dato | 2025-09-20 til 2025-09-28 | samme |
| Tid (UTC) | 00:00, 06:00, 12:00, 18:00 | samme |
| Område | N 50, V −80, S 20, Ø 0 | samme |
| Format | NetCDF4, unarchived | samme |

Lagre filene som `data/era5_bakke.nc` og `data/era5_trykkflater.nc`. Kjør deretter dette én gang, slik at variabelnavnene blir de samme som notatboken bruker:

```python
import xarray as xr, hent_data_gabrielle as h
for f in ["era5_bakke.nc", "era5_trykkflater.nc"]:
    ds = xr.open_dataset(h.DATA / f).load()
    h.lagre(h.rydd_era5(ds), h.DATA / f)
```

### Hvis noe mangler

- Mangler `gabrielle_bane.csv`, bruker notatboken utdraget fra NHC-rapporten. Da starter banen 21. september.
- Mangler ERA5, hopper Del 3a og 3b over figurene. 3c og 3d virker fortsatt.
- Mangler OISST, hopper Del 2 over figurene.

## Tidsplan

| Tid | Del | Merknad |
|---|---|---|
| 0–10 | Oppstart og hypotese | Vis gjerne et satellittbilde av Gabrielle ved toppen (NOAA-21 VIIRS, 22.09) |
| 10–35 | Del 1 Banen og styrken | 1a–1d |
| 35–60 | Del 2 Havet som drivstoff | 2a–2c |
| 60–70 | Pause | |
| 70–100 | Del 3 Fra orkan til ekstratropisk storm | 3a–3d. Kutt 3d hvis tiden blir knapp |
| 100–120 | Del 4 Oppsummering | Skriftlig svar med tre tall fra dataene |

Fordypning A (Argo) og B (Humberto) er for elever som blir tidlig ferdige.

## Løsningsforslag og stikkord

Tallene som står her, er hentet fra NHC-rapporten (Blake 2025). Fyll inn tallene merket ☐ når du har kjørt notatboken med de ekte dataene.

**1a** Først vest-nordvest og nordvest i strømmen rundt den sørlige delen av det subtropiske høytrykket. Banen bøyer mot nord gjennom et brudd i høytrykksryggen og deretter mot nordøst og øst i vestavindsbeltet. Farten øker mye etter 24.09, og punktene ligger langt fra hverandre.

**1b** Sterkest 23.09 kl. 00 UTC med 120 kt (62 m/s) og 944 hPa, omtrent 170 nautiske mil øst for Bermuda. Det er kategori 4. Lavere trykk i sentrum gir brattere trykkgradient og sterkere vind. I den ekstratropiske fasen øker vinden igjen til 65 kt (33 m/s) rundt 27.09 kl. 00 UTC.

**1c** Fra 65 kt (993 hPa) 21.09 kl. 18 til 120 kt (944 hPa) omtrent 30 timer senere. Det er 55 kt og 49 hPa. Største økning over 24 timer er 50 kt, omtrent 26 m/s. Det skjedde rett sør og øst for Bermuda.

**1d** Tydelig sammenheng i den tropiske fasen. Ekstratropiske punkter har svakere vind ved samme trykk, fordi trykkfeltet er større og slakere. Trykkgradienten er det som gir vinden, ikke selve sentraltrykket.

**2a–2b** ☐ breddegrad for 26,5 °C ved banen. NHC skriver at varmere hav og mindre vindskjær rundt 20.09 ga intensivering, og at kaldere hav og økende vindskjær 23.–24.09 ga svekkelse. Tidlig var det også tørr luft som bremset utviklingen. Havtemperaturen alene forklarer derfor ikke svekkelsen.

**2c** ☐ største avkjøling. Avkjølingen er vanligvis sterkest på høyre side av banen på den nordlige halvkule, der vinden og stormens bevegelse virker i samme retning. Prosesser: vinden blander kaldt vann opp fra under blandingslaget, og Ekman-transport bort fra sentrum gir oppvelling (Ekman-pumping). En orkan som går sakte, blir liggende over sitt eget kalde vann.

**3a** 23.09: lite, symmetrisk lavtrykk med tette isobarer og varm kjerne. 25.09: større og skjevere, med kald luft som trekkes inn fra nordvest. 27.09: frontlignende temperaturkontraster, og energien kommer fra temperaturforskjellen mellom luftmassene (baroklin utvikling). ☐ sjekk at dette synes i figuren.

**3b** ☐ vindskjær under intensiveringen og 23.–24.09. Forventet mønster: lavt mens den intensiverte, deretter økende da den kom inn i vestavindsbeltet.

**3c** Orkankast (≥ 32,7 m/s) på Faial 08506 (83 kt, 43 m/s) og Terceira (65 kt, 33 m/s). Graciosa hadde 63 kt, rett under grensen. Ingen hadde orkan i middelvind nær havnivå. Vindkastfaktoren ligger mellom ca. 1,5 og 3. Vindkast kommer av turbulens som tar ned raskere luft ovenfra. På fjellet er friksjonen mindre, og stasjonen ligger høyere oppe i vindfeltet. En 10-minutters middelvind jevner ut de sterkeste minuttene og blir derfor lavere enn en 1-minutts middelvind.

**3d** Faial 08506 → São Miguel gir ca. 280 km på 4 timer, eller ca. 70 km/h. Banedataene gir ca. 50 km/h. Avviket kommer av at stasjonene ikke ligger på banen. Laveste trykk kommer når sentrum er nærmest, ikke når det passerer «samme punkt», og koordinatene er omtrentlige. NHC meldte at stormen gikk mot øst-nordøst med ca. 48–50 km/h. Sterkest vind på høyre side, der stormens egen vind og forflytningsfarten legges sammen.

**Del 4** Et godt svar har med varmt hav og lite vindskjær med tall fra 1c og 2b, svekkelse over kaldere vann og økende vindskjær, og ekstratropisk overgang med større vindfelt og ny forsterking, med tall fra 3a og 3c.

## Om dataene

- **Banedata.** IBTrACS v04r01 med NHCs beste estimat (USA_WIND, USA_PRES). NHC bruker 1-minutts middelvind.
- **Stasjonsdata.** NHC-rapporten, tabell 2. Stasjonene bruker 10-minutters middelvind. Koordinatene i fila (`lat_ca`, `lon_ca`) er omtrentlige posisjoner for flyplassen eller byen på hver øy. De er lagt inn i etterkant og står ikke i rapporten.
- **Utdraget fra tabell 1** er transkribert fra PDF-en. Sjekk gjerne noen rader mot rapporten.
- **Status for testingen.** Notatboken er kjørt fra start til slutt med syntetiske testdata, ikke med de ekte filene, fordi NOAA og Copernicus ikke var tilgjengelige der notatboken ble laget. Første gang du kjører med ekte data, bør du se ekstra nøye på OISST-nedlastingen (ERDDAP-adressen) og på kolonnenavnene fra argopy.

## Kilder

- Blake, E. S. (2025). *Tropical Cyclone Report. Hurricane Gabrielle (AL072025)*. National Hurricane Center. nhc.noaa.gov/data/tcr/AL072025_Gabrielle.pdf
- Knapp mfl. (2010). IBTrACS. *BAMS* 91, 363–376. Data: NOAA NCEI.
- Huang mfl. (2021). NOAA OISST v2.1. *J. Climate* 34, 2923–2939.
- Hersbach mfl. (2020). ERA5. *QJRMS* 146, 1999–2049. Copernicus Climate Change Service.
- Argo (2000). Argo float data and metadata from GDAC. SEANOE. doi:10.17882/42182
