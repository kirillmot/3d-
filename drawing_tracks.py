import pyqtgraph.opengl as gl
import PyQt6.QtWidgets as pqg
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
import numpy as np



unit_color = (255, 0, 0, 200) # красный цвет для единичных цепочек
binary_color = (0, 0, 255, 200) # синий цвет для двоичных цепочек
# Breaking tracks from a file into separate hits
tracks = []
track_id = 0
with open("event.txt", "r") as f:
    for i in f:
        temp = []
        tracks.append([])
        mas = i.split(", ")
        t = 0
        j = 0
        while j < len(mas):
            if t != 9:
                temp.append(float(mas[j]))
                t += 1
                j += 1
            else:
                tracks[track_id].append(temp)
                temp = []
                t = 0
        if j == t:
            tracks[track_id].append(temp)
            temp = []
            t = 0
        track_id += 1

# Discard all characteristics of hits, except for coordinates
tracks_new = []
indexes = []
i = 0
j = 0
for track_num in range(len(tracks)):
    indexes.append([])
    for hit in range(len(tracks[track_num])):
        x = tracks[track_num][hit][1]
        y = tracks[track_num][hit][2]
        z = tracks[track_num][hit][3]
        tracks_new.append([x, y, z])
        indexes[i].append(j)
        j += 1
    i += 1

# Looking for the maximum track length
max_len = -1
for i in range(len(indexes)):
    if len(indexes[i]) > max_len:
        max_len = len(indexes[i])

for i in range(len(indexes)):
    if len(indexes[i]) < max_len:
        indexes[i].extend([indexes[i][-1]] * (max_len - len(indexes[i])))

# Draw a graph
app = pqg.QApplication([])
plot = gl.GLViewWidget()
graphs = gl.GLGraphItem()
graphs.setData(nodePositions=np.array(tracks_new),
               edges=np.array(indexes),
               edgeColor=(0, 255, 0),
               edgeWidth=2)

# Отметим все единичные цепочки - новая часть кода
for track_num in range(len(tracks)):
    for hit in range(len(tracks[track_num])):
        if tracks[track_num][hit][-1] == 1: # последнее значение в строке - метка единичной цепочки
            indexes[track_num][hit] = -1 # пометим единичную цепочку индексом -1

# Отметим все двоичные цепочки - новая часть кода
for track_num in range(len(tracks)):
    for hit in range(len(tracks[track_num])):
        if tracks[track_num][hit][-1] == 2: # последнее значение в строке - метка двоичной цепочки
            indexes[track_num][hit] = -2 # пометим двоичную цепочку индексом -2

unit_edges = np.array([edge for edge in np.array(indexes) if -1 in edge]).astype(int) # все ребра, относящиеся к единичным цепочкам
binary_edges = np.array([edge for edge in np.array(indexes) if -2 in edge]).astype(int) # все ребра, относящиеся к двоичным цепочкам
#построение графика
graphs_unit = gl.GLGraphItem()
graphs_unit.setData(nodePositions=np.array(tracks_new), edges=unit_edges, edgeColor=unit_color, edgeWidth=2)

graphs_binary = gl.GLGraphItem()
graphs_binary.setData(nodePositions=np.array(tracks_new), edges=binary_edges, edgeColor=binary_color, edgeWidth=2)
plot = gl.GLViewWidget()
plot.addItem(graphs_unit)
plot.addItem(graphs_binary)

plot.addItem(graphs)

plot.show()

if __name__ == '__main__':
    app.exec()
