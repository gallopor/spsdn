import yaml


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
        return sorted(self._neighbors.keys())

    def get_neighbors(self):
        '''
        返回该节点所有邻居节点及其权重
        '''
        return self._neighbors

    def __repr__(self):
        return str(self.name)

    def add_neighbor(self, vertex, weight=1):
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
        self._vertices = dict()

    @property
    def vertices(self):
        return sorted(self._vertices)

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex):
            if vertex.name not in self._vertices:
                self._vertices[vertex.name] = vertex
            else:
                print('Vertex: name=%s, already exists' % vertex.name)

    def get_vertex(self, name):
        if name in self._vertices:
            return self._vertices[name]

    def add_edge(self, src, dst, weight=1):
        if src in self._vertices and dst in self._vertices:
            self._vertices[src].add_neighbor(self._vertices[dst], weight)

    def __contains__(self, name):
        return name in self._vertices

    # 迭代显示邻接表的每个顶点
    def __iter__(self):
        return iter(self._vertices.values())

    def __repr__(self):
        graph = dict()
        for name in sorted(self._vertices):
            graph[name] = self.get_vertex(name).get_neighbors()
        return yaml.dump(graph, indent=4)

    def bfs(self, src, func=None):
        visited = list()
        queue = list()
        queue.append(src)
        visited.append(src)
        while queue:
            cur = queue.pop(0)
            if func:
                try:
                    func(cur)
                except Exception:
                    print('Failed to call the function %s!' % func)
            else:
                print(cur, end=' ')

            for node in self.get_vertex(cur).neighbors:
                if node not in visited:
                    queue.append(node)
                    visited.append(node)

    def find_path(self, src, dst, path=[]):
        path = path + [src]
        if src == dst:
            return path
        for node in self._vertices[src].neighbors:
            if node not in path:
                new_path = self.find_path(node, dst, path)
                if new_path:
                    return new_path
        return None

    def find_all_path(self, src, dst, path=[]):
        path = path + [src]
        if src == dst:
            return [path]

        paths = []  # 存储所有路径
        for node in self._vertices[src].neighbors:
            if node not in path:
                new_paths = self.find_all_path(node, dst, path)
                for np in new_paths:
                    paths.append(np)
        return paths

    def find_shortest_path(self, src, dst, path=[]):
        path = path + [src]
        if src == dst:
            return path

        shortest_path = []
        for node in self._vertices[src].neighbors:
            if node not in path:
                new_path = self.find_shortest_path(node, dst, path)
                if new_path:
                    if not shortest_path or len(new_path) < len(shortest_path):
                        shortest_path = new_path
        return shortest_path


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

    # g.bfs(0)
