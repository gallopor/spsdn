class Vertex:
    def __init__(self, id, **kwargs):
        self._id = id
        self.properties = kwargs       # 节点属性
        self.neighbors = dict()        # 相邻节点

    @property
    def id(self):
        return self._id

    def add_neighbor(self, vertex, weight=0):
        '''
        添加邻居节点
        :param vertex: 邻居节点
        :param weight: 权重，默认值为0
        '''
        if isinstance(vertex, Vertex):
            if vertex.id not in self.neighbors:
                self.neighbors[vertex.id] = weight
                vertex.neighbors[self.id] = weight

    def get_neighbors(self):
        '''
        获取该节点所有邻居的ID
        '''
        return list(self.neighbors.keys())

    def __repr__(self):
        return str(self.id) + ' connected to: ' + str([x for x in self.neighbors])

    def set_weight(self, vertex, weight):
        if isinstance(vertex, Vertex):
            if vertex.id in self.neighbors:
                self.neighbors[vertex.id] = weight
                vertex.neighbors[self.id] = weight

    def get_weight(self, nbr):
        return self.neighbors[nbr]

    def set_properties(self, **kwargs):
        self.properties = self.properties + kwargs

    def get_properties(self):
        return self.properties


# 采用邻接表存储图
class GraphAL:
    # 初始化图
    def __init__(self):
        self.vertices = dict()

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex):
            if vertex.id not in self.vertices.keys():
                self.vertices[vertex.id] = vertex
            else:
                print('Vertex: id=%s, already exists' % vertex.id)
        return list(self.vertices.keys())

    def get_vertex(self, id):
        if id in self.vertices:
            return self.vertices[id]

    def add_edge(self, src, dst, weight=0):
        if src in self.vertices and dst in self.vertices:
            self.vertices[src].add_neighbor(self.vertices[dst], weight)

    def __contains__(self, id):
        return id in self.vertices

    # 迭代显示邻接表的每个顶点的邻居节点
    def __iter__(self):
        return iter(self.vertices.values())

    def __repr__(self):
        for id in self.vertices:
            print(self.vertices[id])


if __name__ == '__main__':

    # a = Vertex(1, name='A')
    # b = Vertex(2, name='B')
    # c = Vertex(3, name='C')
    # d = Vertex(4, name='D')
    # e = Vertex(5, name='E')

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

    for v in g:
        for w in v.get_neighbors():
            print("(%s,%s)" % (v.id, g.get_vertex(w).id))
