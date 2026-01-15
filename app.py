import streamlit as st
import folium
from streamlit_folium import st_folium
from pathlib import Path
import json

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Wolf Habitat Graubünden",
    page_icon="🐺",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar by default for cleaner look
)

# --- PATHS ---
DATA_DIR = Path("web_data")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .legend-box {
        border-radius: 5px;
        padding: 10px;
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
        color: #333333 !important;
    }
    .legend-item {
        display: flex;
        align-items: center;
        margin-bottom: 5px;
        font-size: 14px;
        color: #333333 !important;
    }
    .color-box {
        width: 20px;
        height: 20px;
        margin-right: 10px;
        border-radius: 3px;
        border: 1px solid rgba(0,0,0,0.2);
    }
    .gradient-bar {
        height: 15px;
        width: 100%;
        /* RdYlBu Gradient: Red -> Yellow -> Blue */
        background: linear-gradient(90deg, #d73027 0%, #ffffbf 50%, #4575b4 100%);
        border-radius: 3px;
        margin-bottom: 5px;
        border: 1px solid rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNCTIONS ---

@st.cache_data
def load_bounds(filename):
    """Loads bounds for PNG overlays."""
    path = DATA_DIR / filename
    if not path.exists():
        return None
    with open(path, 'r') as f:
        return json.load(f)

def add_png_layer(m, filename_base, layer_name, opacity=0.7, show=False, group=None):
    """Helper to add a PNG layer to the map."""
    img_path = DATA_DIR / f"{filename_base}.png"
    bounds_path = f"{filename_base}_bounds.json"
    
    if img_path.exists():
        bounds = load_bounds(bounds_path)
        if bounds:
            # We use FeatureGroup to allow cleaner layer control grouping if needed
            fg = folium.FeatureGroup(name=layer_name, show=show)
            folium.raster_layers.ImageOverlay(
                image=str(img_path),
                bounds=bounds,
                opacity=opacity,
                name=layer_name
            ).add_to(fg)
            fg.add_to(m)

def create_map():
    # Start coordinates Graubünden
    m = folium.Map(
        location=[46.65, 9.6], 
        zoom_start=9, 
        tiles=None,
        control_scale=True
    )

    # 1. Base Map: Swisstopo Grey
    folium.TileLayer(
        tiles="https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-grau/default/current/3857/{z}/{x}/{y}.jpeg",
        attr="&copy; swisstopo",
        name="Swisstopo Grey",
        overlay=False,
        control=True
    ).add_to(m)

    # 2. Add All Layers (Controlled via internal LayerControl)
    
    # Background: Habitat Suitability (Default: Visible)
    add_png_layer(m, "habitat_overlay", "Habitat Suitability Index", opacity=0.8, show=True)

    # Scenarios (Default: Hidden)
    add_png_layer(m, "scenario_wolf", "Scenario: Best Case Wolf", opacity=0.6, show=False)
    add_png_layer(m, "scenario_human", "Scenario: Best Case Human", opacity=0.6, show=False)

    # Conflicts (Default: Hidden)
    add_png_layer(m, "conflict_medium", "Risk: Medium (Pastures)", opacity=0.6, show=False)
    add_png_layer(m, "conflict_high", "Risk: High (Sheep Alpages)", opacity=0.6, show=False)

    # Layer Control (collapsed=False makes it visible immediately)
    folium.LayerControl(collapsed=False).add_to(m)
    
    return m

# --- MAIN LAYOUT ---

st.title("Wolf Habitat Analysis Graubünden")

# --- PROJECT DESCRIPTION (ABOUT) ---
with st.expander("ℹ️ About this Project & Methodology", expanded=False):
    st.markdown("""
    ### Project Goal
    This interactive dashboard visualizes the potential habitat suitability for wolves in the Canton of Graubünden, Switzerland. 
    It aims to identify core habitats, highlight potential conflict zones with human activities (focus on livestock grazing)
    and simulate different management scenarios.

    ### Methodology: Multi-Criteria Analysis (MCA)
    The model calculates a suitability score (0 to 1) for every 10x10m area based on ecological and anthropogenic factors.
    
    ##### Key Criteria:
    * **Landcover:** Forest density and shrubland availability (high weight).
    * **Prey:** Presence of alpine pastures as a proxy for wild ungulates.
    * **Topography:** Preference for moderate altitudes (900-2200m) and avoidance of steep cliffs.
    * **Disturbance:** Strong avoidance of settlements and heavy traffic roads (Distance decay).

    ##### Scenarios:
    * **Best Case Wolf:** Shows great habitat potential (suitability score > 0.6).
    * **Best Case Human:** Restricts the wolf to areas with minimal conflict potential (suitability score > 0.6, far from settlements/livestock grazing).
                
    ##### Visualization & Color Scale:
    The map uses a **Red-Yellow-Blue** scale. To enhance visual contrast and interpretability, the color ramp is scaled to the **range 0.15 - 0.85** rather than the theoretical 0-1 interval.
    * **Actual Scores:** The calculated suitability scores in the study area range from a minimum of **~0.20** to a maximum of **~0.85**.
    * **Interpretation:** **Red** represents the relatively lowest suitability found locally, while **Blue** represents the best habitat available within the canton.
        
    <br>                       
    
    For detailed methodology, data sources, and analysis, please refer to the [full report](#####) and [GitHub Repository](https://github.com/klaveflo/Wolf_habitat_suitability_Graubunden).            
    """, unsafe_allow_html=True)

# --- MAIN CONTENT AREA ---
col_map, col_legend = st.columns([3, 1])

with col_map:
    # THE MAP
    # returned_objects=[] ensures NO reloading when zooming/panning
    m = create_map()
    st_folium(m, width="100%", height=700, returned_objects=[])

with col_legend:
    st.subheader("Legend & Guide")
    
    # 1. Habitat Suitability Legend
    st.markdown("""
    <div class="legend-box">
        <b>Habitat Suitability</b><br>
        <div class="gradient-bar"></div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #333;">
            <span>Low (Red)</span>
            <span>High (Blue)</span>
        </div>
        <small style="color: #555;">Scaled to range 0.15 - 0.85.</small>
    </div>
    """, unsafe_allow_html=True)

    # 2. Scenarios Legend
    st.markdown("""
    <div class="legend-box">
        <b>Scenarios</b><br>
        <div class="legend-item">
            <div class="color-box" style="background-color: #00FFFF; opacity: 0.7;"></div>
            <div>
                <b>Best Case Wolf</b><br>
                <small>Habitat potential (suitability score > 0.6) (Cyan)</small></div>
        </div>
        <div class="legend-item">
            <div class="color-box" style="background-color: #FF00FF; opacity: 0.7;"></div>
            <div>
                <b>Best Case Human</b><br>
                <small>Conflict-minimized core areas (suitability score > 0.6) (Magenta)</small></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Conflict Legend
    st.markdown("""
    <div class="legend-box">
        <b>Conflict Potential</b><br>
        <div class="legend-item">
            <div class="color-box" style="background-color: #000000; opacity: 0.8;"></div>
            <div>
                <b>High Risk</b><br>
                <small>Sheep Alpages in good habitat (Black)</small></div>
        </div>
        <div class="legend-item">
            <div class="color-box" style="background-color: #8B4513; opacity: 0.8;"></div>
            <div>
                <b>Medium Risk</b><br>
                <small>General pastures in good habitat (Brown)</small></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 **Tip:** Toggle layers using the layer control icon (top right) on the map.")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 14px;">
    Semester Project GISScience and Geodatabases | ZHAW Life Sciences & Facility Management<br>
    Data Sources: swisstopo (swissALTI3D, swissTLM3D, swissBOUNDARIES3D), geocat (Arealstatistik) | 
    <a href="https://github.com/klaveflo/Wolf_habitat_suitability_Graubunden" target="_blank">GitHub Repository</a> | 
    <a href="#####" target="_blank">Full Report</a>
</div>
""", unsafe_allow_html=True)