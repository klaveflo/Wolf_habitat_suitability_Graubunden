# Wolf Habitat Suitability Analysis for Graubünden: <br> A Multi-Criteria Analysis Approach for Conflict-Sensitive Habitat Modeling

**Author:** Florian Klaver

## General Information
The natural recolonization of the Alps by the gray wolf (Canis lupus) presents a significant conservation success but also a considerable challenge for coexistence in human-dominated landscapes. This project models suitable wolf habitats in the Canton of Graubünden (Switzerland) using a raster-based Multi-Criteria Analysis (MCA) and quantifies the spatial trade-offs between biological potential and social constraints.

This repository contains the complete Python-based geoprocessing workflow used to:  

1. Integrate environmental factors (forest cover, slope, prey availability) and anthropogenic disturbance (roads, settlements).
2. Identify conflict zones where suitable habitat overlaps with vulnerable livestock grazing areas.
3. Model two scenarios: "Potential Core Habitats" (Biological Suitability) vs. "Conflict-Minimized Core Habitats" (Social Tolerance).

Key Findings: While biologically suitable habitat is abundant (~2225 km²), applying strict social constraints reduces the available core habitat by approximately 73% to only ~603 km², resulting in a highly fragmented landscape. 
<br>  
You can explore the results, toggle map layers, and compare scenarios interactively via this [streamlit dashboard](https://wolf-habitat-suitability-graubunden.streamlit.app/). <br>
The full report can be accessed as [web-version](https://klaveflo.github.io/Wolf_habitat_suitability_Graubunden/) or as [PDF](docs/index.pdf).

## Repository Structure
```
Wolf_Habitat_Suitability_Graubunden/
│───.gitignore                                 # Collection of files and folder for Git to ignore     
│───app.py                                     # Code for streamlit dashboard
│───environment_local.yml                      # dependancies for full workflow
│───README.md                                  # README
│───requirements.txt                           # requirements for web-hosted streamlit dashboard
│───wolf_habitat.qgz                           # QGIS-project
│───_quarto.yml                                # Quarto dependancies
├───docs
│   │───.nojekyll                              # Additional file for webversion of report
│   │───index.html                             # HTML for webversion of report
│   │───index.pdf                              # Full report as PDF
│   │───index.qmd                              # Raw quarto file of report
│   │───references.bib                         # List of references
│   │
│   └───images                                 # Images shown in report
|    └───... 
│
├───src
│   │───00_swissalti3d_data_acquisition.ipynb  # Data collection DEM
│   │───01_preprocess_dem.py                   # Preprocess DEM datacolelction
│   │───02_data_exploration.ipynb              # Data exploration to find relevant layers  
│   │───03_data_preparation.ipynb              # Prepare data for MCA  
│   │───04_MCA.ipynb                           # MCA: Habitat suitability calculation
│   │───05_conflict_analysis.ipynb             # Conflict zones analysis
│   │───06_scenario_analysis.ipynb             # Potential vs conflict-minimized habitat
│   │───07_web_data_preparation.ipynb          # Data preparation for dashboard
│
├───web_data                                   # Folder with data for web-hosted dashboard
|   └───...  
│
└───_extensions                                # Quarto extensions 
    └───...  

```


## Usage
This project is designed to run locally using Python and Conda. Since raw geospatial data (SwissTLM3D, swissALTI3D) cannot be distributed in this repository due to licensing, you must acquire them separately (see Data Sources below).

1. **Clone Repository**
2. **Set up Environment**
```
conda env create -f environment_local.yml
```
3. **Acquire Data**  
Place the following datasets into a seperate data/ folder (ensure filenames match the scripts or adjust paths in the src scripts):
  - swissALTI3D (DEM tiles or mosaic)
  - SWISSTLM3D (Vector Land Cover)
  - swissBOUNDARIES3D (Cantonal borders)
  - Arealstatistik (Land Use)
 
4. **Run the Analysis**  
Execute the scripts in their numbered order. You can easily adjust parameters at the top of the relevant scripts to comapre how the results change.

5. **Run Dashboard locally (Optional)**  
To analyze how different parameters change the resulting map you can test the interactive map on your local machine.
```
# Important: In shell with activated conda environment and basefolder of Repository
streamlit run dashboard/app.py
```

## Data sources
**Swisstopo**
- [swissALTI3D](https://www.swisstopo.admin.ch/en/height-model-swissalti3d)
- [swissTLM3D](https://www.swisstopo.admin.ch/en/landscape-model-swisstlm3d)
- [swissBOUNDARIES3D](https://www.swisstopo.admin.ch/en/landscape-model-swissboundaries3d)

**BFS**
- [Arealstatistik](https://www.geocat.ch/geonetwork/srv/api/records/f0b56783-613d-4664-9216-98442ce1994d?language=ger)
