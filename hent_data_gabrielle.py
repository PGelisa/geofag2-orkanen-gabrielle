"""
Henter data om orkanen Gabrielle (AL072025, 17.–28. september 2025)
til elevoppgaven i Geofag 2.

Kjøres ÉN gang av læreren. Filene havner i mappen data/ ved siden av
dette skriptet, og kan legges i repoet slik at elevene slipper å laste
ned noe selv.

Bruk (i terminalen, med miljøet aktivert):

    conda activate geofag2
    python hent_data_gabrielle.py              # banedata + havtemperatur
    python hent_data_gabrielle.py --era5       # + ERA5 (krever CDS-konto)
    python hent_data_gabrielle.py --argo       # + Argo-profiler
    python hent_data_gabrielle.py --alt        # alt sammen

Ekstra pakker som bare læreren trenger:

    conda install -c conda-forge cdsapi argopy

Datakilder
----------
- Banedata:     IBTrACS v04r01 (NOAA NCEI), NHCs beste estimat
- Havtemperatur: NOAA OISST v2.1, daglig, 0,25° (via CoastWatch ERDDAP,
                 reserve: NOAA PSL OPeNDAP)
- Atmosfære:    ERA5 (Copernicus Climate Change Service)
- Hav i dybden: Argo (via argopy)
"""

import argparse
import io
import sys
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests
import xarray as xr

DATA = Path(__file__).resolve().parent / "data"
DATA.mkdir(exist_ok=True)

# Tidsrom og område for hav- og atmosfæredata
START, SLUTT = "2025-09-14", "2025-09-30"
LAT_MIN, LAT_MAX = 10.0, 50.0
LON_MIN, LON_MAX = -80.0, 0.0


# ---------------------------------------------------------------------------
# 1 Banedata fra IBTrACS
# ---------------------------------------------------------------------------
IBTRACS = (
    "https://www.ncei.noaa.gov/data/"
    "international-best-track-archive-for-climate-stewardship-ibtracs/"
    "v04r01/access/csv/ibtracs.{}.list.v04r01.csv"
)
KOLONNER = ["ISO_TIME", "LAT", "LON", "USA_WIND", "USA_PRES", "USA_STATUS",
            "STORM_SPEED", "STORM_DIR", "USA_RMW"]


def hent_bane():
    print("Henter banedata fra IBTrACS ...")
    tekst = None
    for utvalg in ["last3years", "NA"]:  # NA-fila er stor (ca. 100 MB)
        url = IBTRACS.format(utvalg)
        try:
            r = requests.get(url, timeout=300)
            r.raise_for_status()
            tekst = r.text
            print(f"  lastet ned {utvalg}")
            break
        except requests.RequestException as feil:
            print(f"  fikk ikke {utvalg}: {feil}")
    if tekst is None:
        sys.exit("Fant ikke IBTrACS. Sjekk adressen på "
                 "https://www.ncei.noaa.gov/products/international-best-track-archive")

    # Rad 2 i fila er enheter, ikke data
    df = pd.read_csv(io.StringIO(tekst), skiprows=[1], low_memory=False,
                     keep_default_na=False, na_values=[" ", ""])

    for navn, fil in [("GABRIELLE", "gabrielle_bane.csv"),
                      ("HUMBERTO", "humberto_bane.csv")]:
        storm = df[(df["SEASON"].astype(str) == "2025")
                   & (df["NAME"] == navn) & (df["BASIN"] == "NA")]
        if storm.empty:
            print(f"  fant ikke {navn} 2025 i fila")
            continue
        storm = storm[KOLONNER].copy()
        storm["ISO_TIME"] = pd.to_datetime(storm["ISO_TIME"])
        # Bare hovedtidspunktene (00, 06, 12, 18 UTC); IBTrACS har også
        # interpolerte verdier hver 3. time
        storm = storm[storm["ISO_TIME"].dt.hour.isin([0, 6, 12, 18])]
        storm = storm.rename(columns={
            "ISO_TIME": "tid_utc", "LAT": "lat", "LON": "lon",
            "USA_WIND": "vind_kt", "USA_PRES": "trykk_hPa",
            "USA_STATUS": "status", "STORM_SPEED": "fart_kt",
            "STORM_DIR": "retning_grader", "USA_RMW": "rmw_nmi"})
        storm.to_csv(DATA / fil, index=False)
        print(f"  lagret {fil} ({len(storm)} tidspunkter)")


# ---------------------------------------------------------------------------
# 2 Havtemperatur fra OISST
# ---------------------------------------------------------------------------
ERDDAP = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/ncdcOisst21Agg_LonPM180.nc"
PSL = ("https://psl.noaa.gov/thredds/dodsC/Datasets/"
       "noaa.oisst.v2.highres/sst.day.mean.2025.nc")


def lagre(ds, fil):
    """Lagrer som komprimert NetCDF med 32-biters tall (små filer)."""
    enc = {v: {"zlib": True, "complevel": 4, "dtype": "float32"}
           for v in ds.data_vars}
    ds.to_netcdf(fil, encoding=enc)


def rydd_sst(ds):
    ds = ds.rename({k: v for k, v in {"latitude": "lat", "longitude": "lon"}.items()
                    if k in ds.dims})
    if "zlev" in ds.dims:
        ds = ds.isel(zlev=0, drop=True)
    if float(ds.lon.max()) > 180:          # 0–360 → −180–180
        ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180)).sortby("lon")
    ds = ds[["sst"]]
    ds["time"] = ds.time.dt.floor("D")
    ds.sst.attrs.update(units="degC", long_name="Havtemperatur i overflaten")
    return ds.sortby("lat")


def hent_sst():
    fil = DATA / "oisst_gabrielle.nc"
    print("Henter havtemperatur (OISST) ...")
    sporring = (f"sst[({START}T12:00:00Z):1:({SLUTT}T12:00:00Z)]"
                f"[(0.0):1:(0.0)][({LAT_MIN}):1:({LAT_MAX})]"
                f"[({LON_MIN}):1:({LON_MAX})]")
    url = ERDDAP + "?" + quote(sporring, safe="():,.-")
    try:
        r = requests.get(url, timeout=600)
        r.raise_for_status()
        tmp = DATA / "_tmp_oisst.nc"
        tmp.write_bytes(r.content)
        with xr.open_dataset(tmp) as ds:
            lagre(rydd_sst(ds.load()), fil)
        tmp.unlink()
        print(f"  lagret {fil.name} (fra ERDDAP)")
        return
    except Exception as feil:  # noqa: BLE001
        print(f"  ERDDAP feilet ({feil}), prøver PSL ...")

    ds = xr.open_dataset(PSL)
    ds = ds.sel(time=slice(START, SLUTT), lat=slice(LAT_MIN, LAT_MAX),
                lon=slice(LON_MIN % 360, 360))
    lagre(rydd_sst(ds.load()), fil)
    print(f"  lagret {fil.name} (fra PSL)")


# ---------------------------------------------------------------------------
# 3 ERA5 (krever konto på https://cds.climate.copernicus.eu og ~/.cdsapirc)
# ---------------------------------------------------------------------------
def rydd_era5(ds):
    navn = {"valid_time": "time", "latitude": "lat", "longitude": "lon",
            "pressure_level": "nivaa"}
    ds = ds.rename({k: v for k, v in navn.items() if k in ds.variables})
    ds = ds.drop_vars([v for v in ["expver", "number"] if v in ds.variables])
    return ds.sortby("lat")


def hent_era5():
    import cdsapi

    c = cdsapi.Client()
    felles = {
        "product_type": ["reanalysis"],
        "year": ["2025"], "month": ["09"],
        "day": [f"{d:02d}" for d in range(20, 29)],
        "time": ["00:00", "06:00", "12:00", "18:00"],
        "area": [LAT_MAX, LON_MIN, 20.0, LON_MAX],   # N, V, S, Ø
        "grid": [0.5, 0.5],
        "data_format": "netcdf",
        "download_format": "unarchived",
    }
    jobber = [
        ("reanalysis-era5-single-levels", "era5_bakke.nc",
         {"variable": ["mean_sea_level_pressure",
                       "10m_u_component_of_wind",
                       "10m_v_component_of_wind"]}),
        ("reanalysis-era5-pressure-levels", "era5_trykkflater.nc",
         {"variable": ["u_component_of_wind", "v_component_of_wind",
                       "temperature"],
          "pressure_level": ["200", "500", "850"]}),
    ]
    for datasett, filnavn, ekstra in jobber:
        print(f"Bestiller {filnavn} fra CDS (kan ta noen minutter) ...")
        tmp = DATA / f"_tmp_{filnavn}"
        c.retrieve(datasett, {**felles, **ekstra}, str(tmp))
        with xr.open_dataset(tmp) as ds:
            lagre(rydd_era5(ds.load()), DATA / filnavn)
        tmp.unlink()
        print(f"  lagret {filnavn}")


# ---------------------------------------------------------------------------
# 4 Argo-profiler der orkanen var sterkest
# ---------------------------------------------------------------------------
def hent_argo():
    from argopy import DataFetcher

    print("Henter Argo-profiler ...")
    # Lengdegrad V, Ø, breddegrad S, N, trykk min, maks (dbar), dato fra, til
    omraade = [-66.0, -50.0, 26.0, 38.0, 0.0, 300.0,
               "2025-09-08", "2025-10-08"]
    ds = DataFetcher().region(omraade).to_xarray()
    df = ds.to_dataframe().reset_index()
    behold = ["PLATFORM_NUMBER", "CYCLE_NUMBER", "TIME", "LATITUDE",
              "LONGITUDE", "PRES", "TEMP", "PSAL"]
    df = df[[k for k in behold if k in df.columns]]
    df.to_csv(DATA / "argo_gabrielle.csv", index=False)
    n = df.groupby(["PLATFORM_NUMBER", "CYCLE_NUMBER"]).ngroups
    print(f"  lagret argo_gabrielle.csv ({n} profiler)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--era5", action="store_true", help="hent ERA5")
    p.add_argument("--argo", action="store_true", help="hent Argo")
    p.add_argument("--alt", action="store_true", help="hent alt")
    a = p.parse_args()

    hent_bane()
    hent_sst()
    if a.era5 or a.alt:
        hent_era5()
    if a.argo or a.alt:
        hent_argo()
    print("\nFerdig. Filene ligger i", DATA)
