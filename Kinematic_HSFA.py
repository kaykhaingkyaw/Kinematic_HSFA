
"""
Kinematic_HSFA.py: This is pesudo codes for the implementation.
Inputs: CLSA_LiDAR.tif, CLSA_LiDAR.d8.tif, bluespots.labels.tif, watersheds.labels.tif,events.shp
"""

import os
import math
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio

def filter_network_matrix(events_features):
    """
    Step 1: Network Initialization & Filter Matrix (events.csv)
    Computes storage variables and filters stagnant nodes with no downstream dependents.
    """
    data = extract_attributes_to_dataframe(events_features)
    return data[((data['spillv'] != 0) | (data['nodetype'] == 'junction')) & ~(((data['spillv'] - data['rainv']) + data['v'] == 0) & (~data['dstrnodeid'].isin(set(data['nodeid']))))]



def compute_flow_distances(flow_dir_grid, bluespot_mask):
    """
    Step 2: Hydraulic Distance Evaluation (flow_length_raster_bluespots)
    Traces directional values from CLSA_LiDAR.d8.tif cell-by-cell to accumulate flow lengths inside depression bounds.
    """
    return [accumulate_path(cell, flow_dir_grid) for cell in bluespot_mask if cell_is_inside(cell, bluespot_mask)]


def calculate_peak_weir_head(cumulative_Q, mu=0.385, B=1.0, g=9.81):
    """
    Step 3: Runoff Mass Balance & Weir Hydraulics
    Calculates discharge accumulations and evaluates localized water level inflation (delta_h) via weir equations.
    """
    return ((max(cumulative_Q)) / (mu * B * math.sqrt(2 * g))) ** (2/3)


def route_downstream_lag(spill_volume, stream_length, flow_velocity, duration=60.0):
    """
    Step 4: Lagged Hydrograph Routing Cascades (delayed_volume_output)
    Shifts fluid volumes downstream based on transit speed lags and physical stream channel lengths.
    """
    return [0, spill_volume] if (stream_length / flow_velocity) >= duration else [spill_volume * (stream_length / flow_velocity / duration), spill_volume * (1 - (stream_length / flow_velocity / duration))]


def render_inundation_depth(dem, watershed_bounds, final_deltah, pour_point_alt):
    """
    Step 5: Slicing Plane Topographic Inundation Maps (combined_water_depth.tif)
    Intersects terrain values from CLSA_LiDAR.tif against flat pool levels to project variable water depth maps.
    """
    return [(pour_point_alt + final_deltah) - dem[pixel] for pixel in dem if (dem[pixel] <= pour_point_alt + final_deltah) and watershed_bounds[pixel]]


if __name__ == "__main__":
    print("Kinematic HSFA runs successfully.")
    