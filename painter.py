from pyecharts import options as opts


def draw_nodes(topo):
    topo_nodes = list()
    for v in topo:
        topo_nodes.append(opts.GraphNode(
            name=v.name,
            x=int(v.properties['Position'][0]),
            y=int(v.properties['Position'][1]),
            symbol_size=50,
            symbol='image://./pic/router_blue.png'
        ))
    return topo_nodes


def draw_links(topo, path=[], highlight=opts.LineStyleOpts(color='red', width=3)):
    links = list()
    pairs = list()
    i = 0
    while i < len(path) - 1:
        pairs.append(sorted([path[i], path[i+1]]))
        i += 1
    for edge in topo.get_edges():
        if edge in pairs:
            links.append(opts.GraphLink(source=edge[0], target=edge[1], linestyle_opts=highlight))
        else:
            links.append(opts.GraphLink(source=edge[0], target=edge[1]))
    return links


if __name__ == '__main__':
    import webbrowser
    from pyecharts.charts import Graph
    from Topology import parse

    tfpath = './topologies/ER33.yaml'
    topo = parse(tfpath)
    path = topo.find_shortest_path('IsisRouter00', 'IsisRouter09')

    opts_highlight = opts.LineStyleOpts(color='red', width=3)

    c = (
        Graph()
        .add("", draw_nodes(topo), draw_links(topo, path), layout='none')
        .render("topo.html")
    )

    webbrowser.open("topo.html")
