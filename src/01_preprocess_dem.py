# 01: DEM Preprocessing

# Description:
# Resamples the high-resolution VRT (Virtual Raster) to a manageable
# single GeoTIFF file with 10m resolution for analysis.
#
# Key Steps:
# 1. Setup paths relative to the project root.
# 2. Resample (Downsample) using GDAL Warp with 'Average' method.
# ==========================================

import os
from osgeo import gdal

# --- PATH CONFIGURATION ---
# Get directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get project root directory
project_root = os.path.dirname(script_dir)

# Define file paths
input_vrt = os.path.join(project_root, "data", "swissalti3d", "swissalti3d_raw.vrt")
output_folder = os.path.join(project_root, "output")
output_tif = os.path.join(output_folder, "dem_10m_graubuenden.tif")

target_resolution = 10  # Target resolution in meters

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

print(f"Project Root: {project_root}")
print(f"Reading VRT: {input_vrt}")
print(f"Output Target: {output_tif}")

# Verify input file existence
if not os.path.exists(input_vrt):
    raise FileNotFoundError(f"VRT file not found at: {input_vrt}. Please check the path.")

# --- RESAMPLING ---
print(f"Starting resampling to {target_resolution}m resolution...")

# Use gdal.Warp to resample and compress the dataset
ds = gdal.Warp(
    output_tif,
    input_vrt,
    format='GTiff',
    xRes=target_resolution,
    yRes=target_resolution,
    resampleAlg=gdal.GRA_Average, # Average prevents data noise when downsampling
    dstNodata=-9999,              # Define NoData value
    outputType=gdal.GDT_Float32,  # Float32 is sufficient for elevation
    creationOptions=[
        "COMPRESS=LZW",           # Lossless compression
        "TILED=YES",              # Optimized for faster reading
        "BIGTIFF=IF_NEEDED"       # Handle files larger than 4GB
    ]
)

# Close dataset to flush data to disk
ds = None 

print(f"Success! File saved to: {output_tif}")