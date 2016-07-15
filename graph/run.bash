#!/usr/bin/env bash
./graph.py
cat graph.dot
dot -Tpng graph.dot > graph.png
open graph.png
