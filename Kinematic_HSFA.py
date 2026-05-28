
"""
Kinematic_HSFA.py: This is pesudo codes for the conceptualization of Kinematic Hierarchical Filling-and-Spilling Algorithm
Inputs: CLSA_LiDAR.tif, CLSA_LiDAR.d8.tif, bluespots.labels.tif, watersheds.labels.tif,events.shp
"""

import os
import math
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio

# ================================================================
#  KINEMATIC SAFERRAIN WORKFLOW — PSEUDOCODE PIPELINE
#  Overcoming the limitation of the traditional Hierachical Filling and Spilling Algorithm : Additional flood extent beyond
the boundary of depressions
# ================================================================

# Step 1: Filtering rule to choose the blue spots with potential backwater effect
# FILTER events.csv → keep rows with (spill_volume > 0 OR nodetype = 'junction')
# AND (us_v > 0 OR dstrnodeid exists in nodeid list)
# ASSIGN backwater = "YES" for all rows except nodetype = 'junction' → "NO"

# Step 2: Creating flow‑length rasters for bluespots/watersheds
# FOR each bluespot/watershed ID → build a binary mask and trace D8‑direction
# paths to accumulate downstream distance per pixel
# SAVE each resulting flow‑length grid as a raster using DEM georeferencing

# Step 3: Calculating Qmax for each bluespot/watershed
# FOR each bluespot/watershed CSV → group pixels by flow‑length class,
# compute travel‑time‑based discharge Q and cumulative Q
# WRITE Q and Q_cumulative back into each CSV to obtain Qmax per unit

# Step 4: Vups (Volumes Upstream) calculation
# FOR each watershed file → convert Q_cumulative into incremental and cumulative
# volumes over travel‑time intervals
# ADJUST watershed volumes by subtracting bluespot volumes to obtain final_volume

# Step 5: Delta h calculation
# FOR each watershed → take Qmax and apply the weir equation to compute Δh
# STORE this as the initial Δh

# Step 6: Volumes required (Vreq) to achieve this Δh
# FOR each watershed → raise the pour‑point elevation by Δh and integrate all DEM
# pixels below this slicing level (excluding bluespot) to obtain Vreq
# STORE Vreq for each bspot/watershed

# Step 7: Comparison between Vups and Vreq
# FOR each watershed/bluespot → if Vups ≥ Vreq then accept Δh,
# ELSE recalculate Δh using Vups
# WRITE final_deltah back into the results table

# Step 8: Travel‑time delay
# FOR each upstream stream path → sum all travel‑time segments to obtain
# total_delay_time and shift the spill‑volume hydrograph accordingly
# EXPORT the delayed volume curve for each node as a time series

# Step 9: Calculate final delta h
# FOR each watershed → take updated discharge new_Q (Qmax after delay/adjustments)
# and convert it to new_delta_h using the weir equation
# WRITE new_delta_h into each watershed file

# Step 10: Repeat Step 6 and Step 7
# Recalculate Vreq using new_delta_h and set new_final_deltah based on whether
# updated final_volume exceeds this new Vreq

# Final Step: New flooding extent and water depth
# FOR each watershed with non‑zero final_deltah → raise DEM by
# (pour‑point elevation + final_deltah) and compute:
# water_depth = slicing_level − DEM within watershed mask
# EXPORT the resulting water‑depth raster for each watershed as a GeoTIFF
# ================================================================

 
  
    
