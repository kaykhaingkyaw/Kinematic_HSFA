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
### Step 1:Filtering rule to choose the blue spots which has potential of backwater effect

```python
FILTER events.csv → keep rows with (spill_volume>0 OR nodetype='junction') AND (us_v>0 OR dstrnodeid exists in nodeid list)
ASSIGN backwater = "YES" for all rows except nodetype='junction' → "NO"
```
#### Expected Terminal Output:

<img width="1623" height="377" alt="image" src="https://github.com/user-attachments/assets/4fb477af-1ea4-4b49-9863-d8c89cdbef63" />


---

---
### Step 2: Creating flow length rasters for bluespots/watersheds
```python
FOR each bluespot/watershed ID → build a binary mask and trace D8‑direction paths to accumulate downstream distance per pixel
SAVE each resulting flow‑length grid as a raster using DEM georeferencing

```
#### Expected Terminal Output:
 <img width="892" height="790" alt="image" src="https://github.com/user-attachments/assets/e1d319b3-5440-47f9-9ed0-40783de35a46" />

---
### Step 3: Calculating Qmax fro each bluespot/watershed
```python
FOR each bluespot/watershed CSV → group pixels by flow‑length class, compute travel‑time‑based discharge Q and cumulative Q
WRITE Q and Q_cumulative back into each CSV to obtain Qmax per unit
```
####Expected Terminal Output:
<img width="1313" height="317" alt="image" src="https://github.com/user-attachments/assets/9f948dc9-ffe5-4199-a7f7-09fd7d73e402" />

---
### Step 4: Vups (Volumes Upstream ) calculation
```python
FOR each watershed file → convert Q_cumulative into incremental and cumulative volumes over travel‑time intervals
ADJUST watershed volumes by subtracting bluespot volumes to obtain final_volume per watershed
```
#### Expected Terminal Output:
<img width="542" height="153" alt="image" src="https://github.com/user-attachments/assets/7977e8e1-1955-4046-bc51-7704ce82a905" />
<img width="1296" height="156" alt="image" src="https://github.com/user-attachments/assets/57c58f13-e59f-439e-b49f-f8be33476464" />


---
### Step 5: Delta h calculation
```python
FOR each watershed → take Qmax and applied it to calcute Δh using the weir equation
Store it as the initial Δh
```
#### Expected Terminal Output:
<img width="897" height="146" alt="image" src="https://github.com/user-attachments/assets/54a4e902-c17c-4049-9db0-2289f578c2e1" />


---
### Step 6: Volumes required (Vreq) calcualtion to achieve this delta h
```python
FOR each watershed → raise the pour‑point elevation by Δh and integrate all DEM pixels below this slicing level (excluding bluespot) to obtain Vreq
STORE Vreq for each bspot/watershed in the results table
```
---
### Step 7 : Comparison between Vups and Vreq.
```python
FOR each watershed/bluespot → if Vups ≥ Vreq then accept Δh, else recalculate Δh using Vups
WRITE final_deltah back into the results table
```
#### Expected Terminal Output:
<img width="442" height="222" alt="image" src="https://github.com/user-attachments/assets/213e5023-d9c2-4887-94f8-842e6a4f9b79" />

---

### Step 8: Travel time delay
```python
FOR each upstream stream path → sum all travel‑time segments to obtain total_delay_time and shift the spill‑volume hydrograph accordingly
EXPORT the delayed volume curve for each node as a time series
```
#### Expected Terminal Output:
<img width="893" height="142" alt="image" src="https://github.com/user-attachments/assets/00f8aa2f-3a87-49c2-9319-8d83d8f08266" />

---

### Step 9: Calculate final delta h
```python
FOR each watershed → take updated discharge new_Q (Qmax after delay/adjustments) and convert it to new_delta_h using the weir equation
WRITE new_delta_h into each watershed file
```
---

### Step 10 : Repeat Step 6 and Step 7
```python
Recalculate Vreq using new_delta_h and set new_final_deltah based on whether updated final_volume exceeds this new Vreq
```
#### Expected Terminal Output:
<img width="1348" height="161" alt="image" src="https://github.com/user-attachments/assets/3101ac3a-08cb-4c8b-b0a6-b72e2541d553" />

---

### Final step  : New flooding extent and water depth
```python
FOR each watershed with non‑zero final_deltah → raise DEM by (pour‑point elevation + final_deltah) and compute water depth = slicing_level − DEM within watershed mask
EXPORT the resulting water depth raster for each watershed as a GeoTIFF
```
#### Expected Terminal Output:
<img width="808" height="701" alt="image" src="https://github.com/user-attachments/assets/a9e29ea1-f2c3-4cc4-a380-bf4bcae51eff" />

---
