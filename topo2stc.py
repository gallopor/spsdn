import time
import yaml
import webbrowser
from pyecharts.charts import Graph

from Topology import parse
from painter import draw_nodes, draw_links


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
path = topo.find_shortest_path(src, dst)
print('\n从路由器%s到路由器%s, 最短路径为:\n%s' % (src, dst, str(path)))

c = (
    Graph()
    .add("", draw_nodes(topo), draw_links(topo, path), layout='none')
    .render("topo.html")
)
webbrowser.open("topo.html")

paths = topo.find_all_path(src, dst)
print('\n从路由器%s到路由器%s, 有如下可选路径:' % (src, dst))
for i in range(len(paths)):
    print('%s : %s' % (str(i+1), str(paths[i])))

time.sleep(5)

index = 5
path = paths[index]
print('\n选择%s号路径: %s' % (str(index+1), str(path)))

c = (
    Graph()
    .add("", draw_nodes(topo), draw_links(topo, path), layout='none')
    .render("topo.html")
)
webbrowser.open("topo.html")
