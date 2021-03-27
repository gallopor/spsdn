import yaml
from Topology import parse


tfpath = './topologies/ER33.yaml'

topo = parse(tfpath)
print('拓扑描述文件解析如下(仅表述节点间邻接关系及权重):\n%s' % topo)

props = dict()
for router in topo:
    props[router.name] = router.properties
print('\n各路由器参数如下:')
print(yaml.dump(props, indent=4))

src = 'IsisRouter00'
dst = 'IsisRouter09'
paths = topo.find_all_path(src, dst)
print('\n从路由器%s到路由器%s, 有如下可选路径:' % (src, dst))
for i in range(len(paths)):
    print('%s : %s' % (str(i+1), str(paths[i])))

path = topo.find_shortest_path('IsisRouter00', 'IsisRouter09')
print('\n从路由器%s到路由器%s, 最短路径为:\n%s' % (src, dst, str(path)))
