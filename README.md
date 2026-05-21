# Kinematic_HSFA : Kinematic Hierarchical Filling-and-Spilling Algorithm for Fast-Processing Modelling of Urban Pluvial Flooding
# Overview
This algorithm simulates flooding beyond the boundaries of the depressions, which is one of the limitations of the traditional HSFA, which we call backwater effect.

The example dataset required to run this algorithm (including the 1m resolution LiDAR DEM, flow direction, watersheds, bluespots and events) is hosted on Zenodo.

**Dataset DOI:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18484142.svg)](https://doi.org/10.5281/zenodo.18484142)

### Instructions to Setup Data:
1. **Download** the zip file from [Zenodo (DOI: 10.5281/zenodo.18484142)](https://doi.org/10.5281/zenodo.18484142).
2. **Create** a folder named `data` in your project root directory.
3. **Extract** the contents into that folder. Your directory should look like this:
   ```text
   /flowpathflood-project
     ├── data/
     │    ├── CLSA_LiDAR.tif
     │    ├── CLSA_LiDAR.d8.tif
     │    ├── watersheds.labels.tif
     │    └── bluespots.labels.tif
          └── events.shp          
     ├── requirements.txt
     ├── main.py
     ├── Kinematic_HSFA.py
     └── README.md
   ```
# 🚀 Methodology
### Step 1:Filtering the potential bluespots which will have backwater effects
Computes storage variables and filters the nodes that have no downstream contributions.
```python
def filter_network_matrix(events_features):
    data = extract_attributes(events_features)
    return data[((data['spillv'] != 0) | (data['nodetype'] == 'junction')) & ~(((data['spillv'] - data['rainv']) + data['v'] == 0) & (~data['dstrnodeid'].isin(set(data['nodeid']))))]
```
---
### Step 2: Flow length rasters
```python
def compute_flow_distances(flow_dir_grid, bluespot_mask):
    # Continuously trace downhill vectors until exiting the target boundary mask
    return [accumulate_path(cell, flow_dir_grid) for cell in bluespot_mask if cell_is_inside(cell, bluespot_mask)]
```
---
### Step 3: Calculating delta h using weir equation
```python
def calculate_peak_weir_head(cumulative_Q):
    # Extract structural overtop level from peak mass accumulation
    return ((max(cumulative_Q)) / (mu * B * sqrt(2 * g))) ** (2/3)
```
---
### Step 4: Delaying upstream flood volume transfer
```python
def route_downstream_lag(spill_volume, stream_length, flow_velocity, duration):
    # Translate and divide volumes linearly according to total channel transit time
    return [0, spill_volume] if (stream_length / flow_velocity) >= duration else [spill_volume * (stream_length / flow_velocity / duration), spill_volume * (1 - (stream_length / flow_velocity / duration))]
```
---
### Step 5: Combining to get final inundation map
```python
def render_inundation_depth(dem, watershed_bounds, final_deltah, pour_point_alt):
    # Subtract elevation values from the water surface line within active catchments
    return [(pour_point_alt + final_deltah) - dem[pixel] for pixel in dem if (dem[pixel] <= pour_point_alt + final_deltah) and watershed_bounds[pixel]]
```
---
