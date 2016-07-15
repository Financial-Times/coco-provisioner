#!/usr/bin/env python
import os
from os import listdir
import re
import servicefiles
import simplejson

# PATTERN_REQUIRES = re.compile("^Requires=(.*)$")
# PATTERN_WANTS = re.compile("^Wants=(.*)$")
# PATTERN_WANTS = re.compile("^Description=(.*)$")

BASE_PATH = '../../up-service-files'


def run():
    files = get_file_list()
    services = []
    for filename in files:
        with open('{}/{}'.format(BASE_PATH, filename)) as fp:
            s = servicefiles.ServiceFile(fp)
            services.append(s)
    graph_text = "digraph dependency_graph {\n    rankdir=LR"
    print [s.wants for s in services]
    for s in services:
        for r in s.requires:
            graph_text += "    {} -> {} [label=\"Requires\", style=\"solid\", color=\"Red\"];\n".format(
                sanitise(s.name), sanitise(r)
            )
        for w in s.wants:
            graph_text += "    {} -> {} [label=\"Wants\", style=\"dashed\", color=\"Blue\"];\n".format(
                sanitise(s.name), sanitise(w)
            )
    graph_text += "}"
    with open("graph.dot", 'w') as f:
        f.write(graph_text)


def sanitise(nodename):
    return str.replace(str.replace(str.replace(str.replace(nodename, '.', '_'), '-', '_'), '@', '_'), '%', '_')


def get_file_list():
    mypath = BASE_PATH
    onlyfiles = [f for f in listdir(mypath) if os.path.isfile(os.path.join(mypath, f)) and os.path.splitext(f)[1] == ".service"]
    return onlyfiles


def test():
    print "Graph generator"
    with open("graph.dot", 'w') as f:
        text = """graph helloworld {
    a -- b -- c;
    b -- d
}
"""
        f.write(text)

if __name__ == "__main__":
    run()
