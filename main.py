import sys
import graphhlib as gl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Graph():
    def __init__(self):
        self.adjacency_list = []


    def addVertex(self):
        gl.addVertex(self.adjacency_list)


    def deleteVertex(self, v):
        gl.deleteVertex(v, self.adjacency_list)


    def addEdge(self, v1, v2):
        gl.addEdge(v1, v2, self.adjacency_list)


    def addOrientedEdge(self, v1, v2):
        gl.addOrientedEdge(v1, v2, self.adjacency_list)


    def deleteEdge(self, v1, v2):
        gl.deleteEdge(v1, v2, self.adjacency_list)


    def deleteOrientedEdge(self, v1, v2):
        gl.deleteOrientedEdge(v1, v2, self.adjacency_list)


    def randGraph(self, n, oriented):
        self.adjacency_list = gl.randGraph(n, oriented)


    def isCyclic(self):
        return gl.isCyclic(self.adjacency_list)


    def findCycle(self):
        return gl.findCycle(self.adjacency_list)


    def findBridges(self):
        return gl.findBridges(self.adjacency_list)


    def countPaths(self, v1, v2):
        return gl.countPaths(v1, v2, self.adjacency_list)


    def countAllPaths(self, v):
        return gl.countAllPaths(v, self.adjacency_list)


    def findDistances(self, v):
        return gl.findDistances(v, self.adjacency_list)


    def findPath(self, v1, v2):
        return gl.findPath(v1, v2, self.adjacency_list)
    

    def findComponents(self):
        return gl.findComponents(self.adjacency_list)
        

    def clear(self):
        self.adjacency_list = []


class Vertex():
    def __init__(self, x, y, name, color):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.connected_vertexes = []


    def connect(self, other):
        self.connected_vertexes.append(other)


    def unconnect(self, other):
        if other in self.connected_vertexes:
            self.connected_vertexes.remove(other)


    def isConnected(self, other):
        return other in self.connected_vertexes


    def __str__(self):
        return f"{self.name}({self.x}, {self.y})"


    __repr__ = __str__
    

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.startSetting()
        self.setupUI()


    def setupUI(self):
        self.setWindowTitle('Graphs')
        self.setGeometry(200, 200, 800, 600)
        
        self.fieldSizeX = 550
        self.fieldSizeY = 580

        self.font = QFont()
        self.font.setPointSize(11)
        self.font.setBold(True)
        self.font.setWeight(75)
        
        self.graph_type_label = QLabel("Тип графа:", self)
        self.graph_type_label.setGeometry(QRect(570, 10, 221, 31))
        self.graph_type_label.setFont(self.font)

        self.graph_type_label = QLabel("Функции:", self)
        self.graph_type_label.setGeometry(QRect(570, 80, 221, 31))
        self.graph_type_label.setFont(self.font)

        self.font.setBold(False)
        self.font.setPointSize(10)
        
        self.non_oriented_btn = QRadioButton("Неориентированный", self)
        self.non_oriented_btn.setChecked(True)
        self.non_oriented_btn.setGeometry(QRect(570, 40, 221, 17))
        self.non_oriented_btn.setFont(self.font)

        self.oriented_btn = QRadioButton("Ориентированный", self)
        self.oriented_btn.setGeometry(QRect(570, 60, 221, 17))
        self.oriented_btn.setFont(self.font)

        self.graph_type_group = QButtonGroup()
        self.graph_type_group.addButton(self.non_oriented_btn)
        self.graph_type_group.addButton(self.oriented_btn)
        self.graph_type_group.buttonClicked.connect(self.chooseType)

        self.find_path_btn = QPushButton("Поиск кратчайшего пути", self)
        self.find_path_btn.setGeometry(QRect(570, 110, 221, 31))
        self.find_path_btn.setFont(self.font)
        self.find_path_btn.clicked.connect(self.findPathChoose)

        self.find_paths_btn = QPushButton("Подсчёт расстояний", self)
        self.find_paths_btn.setGeometry(QRect(570, 150, 221, 31))
        self.find_paths_btn.setFont(self.font)
        self.find_paths_btn.clicked.connect(self.findDistances)

        self.find_all_paths_btn = QPushButton("Подсчёт количества всех путей", self)
        self.find_all_paths_btn.setGeometry(QRect(570, 190, 221, 31))
        self.find_all_paths_btn.setFont(self.font)
        self.find_all_paths_btn.clicked.connect(self.countAllPaths)


        self.find_cycle_btn = QPushButton("Поиск цикла", self)
        self.find_cycle_btn.setGeometry(QRect(570, 230, 221, 31))
        self.find_cycle_btn.setFont(self.font)
        self.find_cycle_btn.clicked.connect(self.findCycle)

        self.find_bridges_btn = QPushButton("Поиск мостов", self)
        self.find_bridges_btn.setGeometry(QRect(570, 270, 221, 31))
        self.find_bridges_btn.setFont(self.font)
        self.find_bridges_btn.clicked.connect(self.findBridges)

        self.clear_highlighted_btn = QPushButton("Убрать отображение", self)
        self.clear_highlighted_btn.setGeometry(QRect(570, 310, 221, 31))
        self.clear_highlighted_btn.setFont(self.font)
        self.clear_highlighted_btn.clicked.connect(self.clearHighlight)

        self.clear_btn = QPushButton("Отчистить", self)
        self.clear_btn.setGeometry(QRect(570, 560, 221, 31))
        self.clear_btn.setFont(self.font)
        self.clear_btn.clicked.connect(self.clear)

        
    def startSetting(self):
        self.oriented_graph = False
        self.vertexes = []
        self.selected_vertex = -1
        self.highlight = []
        self.numbers = []
        self.mode = 0
        self.vertex_names = [chr(a).upper() for a in range(ord('a'), ord('z') + 1)]


    def chooseType(self, button):
        if button == self.non_oriented_btn:
            self.oriented_graph = False
            n = len(self.vertexes)
            for v1 in range(n):
                for v2 in range(n):
                    if self.vertexes[v1].isConnected(self.vertexes[v2]) and not self.vertexes[v2].isConnected(self.vertexes[v1]):
                        self.vertexes[v2].connect(self.vertexes[v1])
                        graph.addOrientedEdge(v2, v1)
        else:
            self.oriented_graph = True
        self.clearHighlight()
        self.update()

        
    def mousePressEvent(self, event):
        btn = event.button()
        x = event.x()
        y = event.y()
        if btn == 1:
            self.selectVertex(x, y)
        elif btn == 2:
            self.deleteVertex(x, y)


    def mouseDoubleClickEvent(self, event):
        btn = event.button()
        x = event.x()
        y = event.y()
        if event.button() == 1:
            self.createVertex(x, y)


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.drawField(event, qp)
        self.drawEdges(event, qp)
        self.drawHighlighted(event, qp)
        self.drawArrows(event, qp)
        self.drawVertexes(event, qp)
        self.drawDistances(event, qp)
        qp.end()


    def drawField(self, event, qp):
        qp.setBrush(QColor('White'))
        qp.drawRect(10, 10, self.fieldSizeX, self.fieldSizeY)


    def drawEdges(self, event, qp):
        for vertex in self.vertexes:
            for connected in vertex.connected_vertexes:
                px = vertex.x + 6
                py = vertex.y + 6
                cx = connected.x + 6
                cy = connected.y + 6
                qp.setPen(QPen(QColor("Black"), 2))
                qp.drawLine(px, py, cx, cy)

                    
    def drawHighlighted(self, event, qp):
        for part in self.highlight:
            qp.setPen(QPen(QColor(part[1]), 2))
            v1 = part[0][0]
            v2 = part[0][1]
            v1x = v1.x + 6
            v1y = v1.y + 6
            v2x = v2.x + 6
            v2y = v2.y + 6
            qp.drawLine(v1x, v1y, v2x, v2y)

    
    def drawArrows(self, event, qp):
        if self.oriented_graph:
            for vertex in self.vertexes:
                for connected in vertex.connected_vertexes:
                    px = vertex.x + 6
                    py = vertex.y + 6
                    cx = connected.x + 6
                    cy = connected.y + 6
                    qp.setPen(QPen(QColor(0, 255, 0), 4))
                    dx = int(12 * (px - cx) / (((px - cx) ** 2 + (py - cy) ** 2) ** 0.5))
                    dy = int(12 * (py - cy) / (((px - cx) ** 2 + (py - cy) ** 2) ** 0.5))
                    qp.drawLine(px, py, px - dx, py - dy)


    def drawVertexes(self, event, qp):
        qp.setPen(QPen(QColor("Black"), 1))
        for vertex in self.vertexes:
            qp.setBrush(QColor(vertex.color))
            qp.drawEllipse(vertex.x, vertex.y, 12, 12)
            qp.drawText(vertex.x + 3, vertex.y - 3, vertex.name)


    def drawDistances(self, event, qp):
        qp.setPen(QPen(QColor("Green")))
        font = self.font
        font.setBold(True)
        qp.setFont(self.font)
        for d in range(len(self.numbers)):
            qp.drawText(self.vertexes[d].x + 2, self.vertexes[d].y + 22, str(self.numbers[d]))


    def findVertex(self, x, y):
        for i in range(len(self.vertexes)):
            a = self.vertexes[i].x
            b = self.vertexes[i].y
            if (x - 13 <= a <= x) and (y - 13 <= b <= y):
                return i
        return -1


    def createVertex(self, x, y):
        if self.findVertex(x, y) == -1:
            if (16 <= x <= self.fieldSizeX) and (26 <= y <= self.fieldSizeY):
                self.vertexes.append(Vertex(x - 5,
                                            y - 5,
                                            self.vertex_names.pop(0),
                                            "Black"))
                graph.addVertex()
                self.selectVertex(x - 5, y - 5)
                self.clearHighlight()
                self.update()


    def selectVertex(self, x, y):
        vertex = self.findVertex(x, y)
        if vertex != -1:
            if self.selected_vertex != -1 and self.selected_vertex != vertex:
                if self.mode == 1:
                    self.countPaths(self.selected_vertex, vertex)
                    self.mode = 0
                elif self.mode == 2:
                    self.findPath(self.selected_vertex, vertex)
                    self.mode = 0
                else:
                    self.connectVertexes(vertex, self.selected_vertex)
            else:
                self.selected_vertex = vertex
                self.vertexes[self.selected_vertex].color = "Cyan"
                self.update()
        else:
            if self.selected_vertex != -1:
                self.unselectVertex()


    def unselectVertex(self):
        if self.vertexes != []:
            self.vertexes[self.selected_vertex].color = "Black"
        self.selected_vertex = -1
        self.update()


    def connectVertexes(self, v1, v2):
        if self.oriented_graph:
            if not self.vertexes[v1].isConnected(self.vertexes[v2]):
                self.vertexes[v1].connect(self.vertexes[v2])
                graph.addOrientedEdge(v1, v2)
            else:
                self.vertexes[v1].unconnect(self.vertexes[v2])
                graph.deleteOrientedEdge(v2, v1)
        else:
            if not self.vertexes[v1].isConnected(self.vertexes[v2]):
                self.vertexes[v1].connect(self.vertexes[v2])
                self.vertexes[v2].connect(self.vertexes[v1])
                graph.addEdge(v1, v2)
            else:
                self.vertexes[v1].unconnect(self.vertexes[v2])
                self.vertexes[v2].unconnect(self.vertexes[v1])
                graph.deleteEdge(v1, v2)
        self.clearHighlight()
        self.update()

                    
    def deleteVertex(self, x, y):
        vertex = self.findVertex(x, y)
        if vertex != -1:
            print('deleted', self.vertexes[vertex])
            self.unselectVertex()
            for p in self.vertexes:
                p.unconnect(self.vertexes[vertex])
            self.vertex_names.append(self.vertexes[vertex].name)
            self.vertex_names.sort()
            self.vertexes.pop(vertex)
            graph.deleteVertex(vertex)
            self.clearHighlight()
            self.update()


    def findDistances(self):
        if self.selected_vertex != -1:
            self.numbers = graph.findDistances(self.selected_vertex)
        else:
            QMessageBox.about(self, "Подсчёт расстояний", "Выберите вершину")
        self.update()


    def countPathsChoose(self):
        if self.selected_vertex != -1:
            self.mode = 1
            QMessageBox.about(self, "Подсчёт путей", "Выберите 2-ую вершину")
        else:
            QMessageBox.about(self, "Подсчёт путей", "Выберите 1-ую вершину")


    def countAllPaths(self):
        if self.selected_vertex != -1:
            self.numbers = graph.countAllPaths(self.selected_vertex)
        else:
            QMessageBox.about(self, "Подсчет количества всех путей", "Выберите вершину")
        self.update()
        

    def findPathChoose(self):
        if self.selected_vertex != -1:
            self.mode = 2
            QMessageBox.about(self, "Поиск кратчайшего пути", "Выберите 2-ую вершину")
        else:
            QMessageBox.about(self, "Поиск кратчайшего пути", "Выберите 1-ую вершину")


    def findPath(self, v1, v2):
        path = graph.findPath(v1, v2)
        if path:
            self.highlight = self.pathToDisplay(path, "Path")
        else:
            QMessageBox.about(self, "Поиск кратчайшего пути", "Вершины несвязны")
        self.update()

        
    def findCycle(self):
        if self.oriented_graph:
            if graph.isCyclic():
                cycle = graph.findCycle()
                self.highlight = self.pathToDisplay(cycle, "Cycle")
            else:
                QMessageBox.about(self, "Поиск цикла", "Граф ацикличен")
        else:
            QMessageBox.about(self, "Поиск цикла", "Несответствующий тип графа")
        self.update()


    def findBridges(self):
        if not self.oriented_graph:
            bridges = graph.findBridges()
            self.highlight = self.pathToDisplay(bridges, "Bridge")
            if not bridges:
                QMessageBox.about(self, "Поиск мостов", "Мостов не найдено")
        else:
            QMessageBox.about(self, "Поиск мостов", "Несоответствующий тип графа")
        self.update()


    def clearHighlight(self):
        self.highlight = []
        self.mode = 0
        self.numbers = []
        self.update()


    def pathToDisplay(self, path, mode):
        if mode == "Cycle":
            gen_path = []
            for v in range(len(path)):
                gen_path.append(([self.vertexes[path[v - 1]], self.vertexes[path[v]]], "Blue"))
            path = gen_path
        elif mode == "Path":
            gen_path = []
            for v in range(1, len(path)):
                gen_path.append(([self.vertexes[path[v - 1]], self.vertexes[path[v]]], "Blue"))
            path = gen_path
        elif mode == "Bridge":
            for bridge in range(len(path)):
                for v in range(2):
                    path[bridge][v] = self.vertexes[path[bridge][v]]
                path[bridge] = (path[bridge], "Yellow")
        return path


    def clear(self):
        self.vertex_names = [chr(a).upper() for a in range(ord('a'), ord('z') + 1)]
        self.unselectVertex()
        self.clearHighlight()
        self.vertexes = []
        graph.clear()
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    graph = Graph()
    win = Window()
    win.show()
    sys.exit(app.exec_())
