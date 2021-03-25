class Vertex:
    def __init__(self, name, properties=None):
        self._name = name
        self._properties = properties  # 节点属性(dict)
        self._neighbors = dict()       # 相邻节点

    @property
    def name(self):
        return self._name

    @property
    def properties(self):
        return self._properties

    @property
    def neighbors(self):
        '''
        返回该节点所有邻居节点排序后的名称列表
        '''
        return sorted(list(self._neighbors.keys()))

    def __repr__(self):
        return str(self.name)

    def add_neighbor(self, vertex, weight=0):
        '''
        添加邻居节点
        :param vertex: 邻居节点
        :param weight: 权重，默认值为0
        '''
        if isinstance(vertex, Vertex):
            if vertex.name not in self._neighbors:
                self._neighbors[vertex.name] = weight
                vertex._neighbors[self.name] = weight

    def set_weight(self, vertex, weight):
        if isinstance(vertex, Vertex):
            if vertex.name in self._neighbors:
                self._neighbors[vertex.name] = weight
                vertex._neighbors[self.name] = weight

    def get_weight(self, nbr_name):
        return self._neighbors[nbr_name]

    def set_properties(self, properties):
        self.properties = self.properties + properties


# 采用邻接表存储图
class GraphAL:
    def __init__(self):
        self.vertices = dict()

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex):
            if vertex.name not in self.vertices.keys():
                self.vertices[vertex.name] = vertex
            else:
                print('Vertex: name=%s, already exists' % vertex.name)
        return list(self.vertices.keys()).sort()

    def get_vertex(self, name):
        if name in self.vertices:
            return self.vertices[name]

    def add_edge(self, src, dst, weight=0):
        if src in self.vertices and dst in self.vertices:
            self.vertices[src].add_neighbor(self.vertices[dst], weight)

    def __contains__(self, name):
        return name in self.vertices

    # 迭代显示邻接表的每个顶点的邻居节点
    def __iter__(self):
        return iter(self.vertices.values())

    def __repr__(self):
        graph = ''
        for name in self.vertices:
            graph = graph + str(self.vertices[name]) + ' - '
            for x in self.vertices[name].neighbors:
                graph = graph + str(self.vertices[x]) + ', '
            graph = graph.rstrip(', ') + '\n'
        return graph


if __name__ == '__main__':
    g = GraphAL()
    for i in range(6):
        g.add_vertex(Vertex(i))

    print(g.vertices)

    g.add_edge(0, 1, 5)
    g.add_edge(0, 5, 2)
    g.add_edge(1, 2, 4)
    g.add_edge(2, 3, 9)
    g.add_edge(3, 4, 7)
    g.add_edge(3, 5, 3)
    g.add_edge(4, 0, 1)
    g.add_edge(5, 4, 8)
    g.add_edge(5, 2, 1)

    print(g)

    for v in g:
        for w in v.neighbors:
            print("(%s, %s, %s)" % (v.name, w, v.get_weight(w)))
