from toscaparser.tosca_template import ToscaTemplate
from GraphAL import Vertex, GraphAL


tfpath = './topologies/ER33.yaml'


def parse(tfpath):
    try:
        tosca_tpl = ToscaTemplate(tfpath)
    except Exception:
        print('Failed to parse the topology file.')

    topo = GraphAL()
    devices = dict()
    ports = dict()
    links = list()
    for node in tosca_tpl.nodetemplates:
        if node.type == 'com.spirent.velocity.Device':
            # 设置Device属性及参数
            properties = dict()
            # properties['name'] = node.get_property_value('name')
            name = node.get_property_value('name')
            properties['Position'] = (node.get_property_value('boundary')['x'],
                                      node.get_property_value('boundary')['y'])
            for pg in node.get_property_value('property_groups'):
                if pg['name'] == 'System Identification':  # Identification作为Device属性
                    for prop in pg['group']:
                        properties[prop['name']] = prop['value']
                else:
                    group_name = pg['name']
                    kv = dict()
                    for prop in pg['group']:
                        kv[prop['name']] = prop['value']
                    properties[group_name] = kv
            # devices[node.name] = properties
            devices[node.name] = node.get_property_value('name')
            topo.add_vertex(Vertex(name, properties))
        elif node.type == 'com.spirent.velocity.Port':
            ports[node.name] = node.requirements[0]['device']
        elif node.type == 'com.spirent.velocity.EthernetLink':
            f, t = node.requirements
            links.append((f['from'], t['to']))
        else:
            continue

    for link in links:
        f, t = link
        src = devices[ports[f]]
        dst = devices[ports[t]]
        topo.add_edge(src, dst)

    return topo


# topo = parse(tfpath)
# print(topo)

# paths = topo.find_all_path('IsisRouter00', 'IsisRouter09')
# print(paths)
