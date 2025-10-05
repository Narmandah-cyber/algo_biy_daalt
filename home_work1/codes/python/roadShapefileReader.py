import geopandas as gpd
import matplotlib.pyplot as plt

# Read the file path from roadFile.txt
with open("roadFile.txt", "r") as f:
    road_path = f.read().strip()


# Load shapefile
roads = gpd.read_file(road_path)

# Filter by bounding box (minx, miny, maxx, maxy)
ub_bounds = (106.7, 47.7, 107.2, 48.1)
ub_roads = roads.cx[ub_bounds[0]:ub_bounds[2], ub_bounds[1]:ub_bounds[3]]

# Plot only UB area
ub_roads.plot(figsize=(10, 10), linewidth=0.5, color='blue')
plt.title("Ulaanbaatar Roads")
plt.show()
