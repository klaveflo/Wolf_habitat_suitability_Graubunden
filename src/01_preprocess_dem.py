import os
from osgeo import gdal

# --- PFAD-KONFIGURATION ---
# Wir ermitteln den Pfad dieses Skripts (z.B. .../project/code/)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Wir gehen einen Ordner hoch zum Projekt-Root (z.B. .../project/)
project_root = os.path.dirname(script_dir)

# Pfade relativ zum Projekt-Root definieren
input_vrt = os.path.join(project_root, "data", "swissalti3d", "swissalti3d_raw.vrt")
output_folder = os.path.join(project_root, "output")
output_tif = os.path.join(output_folder, "dem_10m_graubuenden.tif")

target_resolution = 10  # 10 Meter Auflösung

# Ordner 'output' erstellen, falls nicht vorhanden
os.makedirs(output_folder, exist_ok=True)

print(f"Projekt-Root erkannt: {project_root}")
print(f"Lese VRT: {input_vrt}")
print(f"Schreibe nach: {output_tif}")

# Prüfen, ob VRT existiert
if not os.path.exists(input_vrt):
    raise FileNotFoundError(f"Die VRT-Datei wurde nicht gefunden: {input_vrt}. Überprüfe den Pfad!")

print(f"Starte Resampling... Zielauflösung: {target_resolution}m. Das kann einige Minuten dauern...")

# gdal.Warp ist das Schweizer Taschenmesser für Rasteroperationen
# Es liest das VRT und schreibt ein neues, komprimiertes GeoTIFF
ds = gdal.Warp(
    output_tif,
    input_vrt,
    format='GTiff',
    xRes=target_resolution,
    yRes=target_resolution,
    # WICHTIG: 'average' Resampling verhindert Datenrauschen beim Verkleinern!
    resampleAlg=gdal.GRA_Average, 
    dstNodata=-9999,      # Definiert, was "keine Daten" sind
    outputType=gdal.GDT_Float32, # Float32 ist präzise genug für Höhenmeter
    creationOptions=[
        "COMPRESS=LZW",   # Verlustfreie Kompression spart Platz
        "TILED=YES",      # Beschleunigt das spätere Lesen von Ausschnitten
        "BIGTIFF=IF_NEEDED" # Falls die Datei doch > 4GB wird
    ]
)

# Aufräumen (Schließt die Datei und schreibt final auf die Festplatte)
ds = None 

print(f"Fertig! Datei gespeichert unter: {output_tif}")