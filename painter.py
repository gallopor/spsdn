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


def draw_links():
    return [
        opts.GraphLink(source="IsisRouter00", target="IsisRouter01"),
        opts.GraphLink(source="IsisRouter01", target="IsisRouter02"),
    ]


if __name__ == '__main__':
    import webbrowser
    from pyecharts.charts import Graph
    from Topology import parse

    tfpath = './topologies/ER33.yaml'
    topo = parse(tfpath)

    opts_highlight = opts.LineStyleOpts(color='red', width=3)

    c = (
        Graph()
        .add("", draw_nodes(topo), draw_links(), layout='none')
        .render("topo.html")
    )

    webbrowser.open("topo.html")
