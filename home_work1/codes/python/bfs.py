import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from collections import defaultdict, deque
import math

# 1. Shapefile унших
with open("roadFile.txt", "r") as f:
    road_path = f.read().strip()

roads = gpd.read_file(road_path)

# 2. Graph үүсгэх (segment болгож)
graph = defaultdict(list)
for idx, row in roads.iterrows():
    line: LineString = row.geometry
    coords = list(line.coords)
    for i in range(len(coords)-1):
        start = tuple(coords[i])
        end = tuple(coords[i+1])
        graph[start].append(end)
        if row['oneway'] != 'yes':
            graph[end].append(start)

nodes = list(graph.keys())

# 3. Haversine distance
def haversine(coord1, coord2):
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371  # км
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(a))

def find_nearest_node(coord, nodes):
    return min(nodes, key=lambda n: haversine(coord, n))

# 4. BFS
def bfs_shortest_path(graph, start, goal):
    visited = set()
    queue = deque([(start, [start])])
    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None

# 5. Interactive click
clicks = []

def onclick(event):
    if event.inaxes:
        x, y = event.xdata, event.ydata
        clicks.append((x, y))
        print(f"Clicked: {(x, y)}")
        ax.scatter(x, y, color="green" if len(clicks)==1 else "orange", s=100)
        fig.canvas.draw()
        if len(clicks) == 2:
            start_node = find_nearest_node(clicks[0], nodes)
            end_node = find_nearest_node(clicks[1], nodes)
            path = bfs_shortest_path(graph, start_node, end_node)
            if path:
                line = LineString(path)
                gpd.GeoSeries([line]).plot(ax=ax, color="red", linewidth=2)
                fig.canvas.draw()
            print("Shortest path calculated and displayed.")

# 6. Plot UB roads
ub_bounds = (106.7, 47.7, 107.2, 48.1)
ub_roads = roads.cx[ub_bounds[0]:ub_bounds[2], ub_bounds[1]:ub_bounds[3]]

fig, ax = plt.subplots(figsize=(12,12))
ub_roads.plot(ax=ax, linewidth=0.5, color="blue")
plt.title("Ulaanbaatar Roads - Click Start/End")

cid = fig.canvas.mpl_connect("button_press_event", onclick)
plt.show()
