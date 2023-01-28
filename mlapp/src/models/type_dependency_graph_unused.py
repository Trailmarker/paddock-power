# -*- coding: utf-8 -*-
from collections import defaultdict

class TypeDependencyGraph:

    def __init__(self, typeFactory):
        self.graph = defaultdict(list)
        self.nodes = set()
        self._typeFactory = typeFactory


    def addDependencies(self, cls, dependentTypes):
        for dependentType in dependentTypes:
            self.graph[cls].append(dependentType)
            self.nodes.add(dependentType)
            
        self.nodes.add(cls)
   
    def getDependencies(self, obj):
        if isinstance(obj, type):
            return self.graph[obj]
        else:
            return self.graph[type(obj)]
   
                
    @property
    def typeCount(self):
        return len(self.nodes)

    def _sortUtil(self, node, visited, sorted):
            visited[node] = True

            for dependentNode in self.graph[node]:
                if not visited[dependentNode]:
                    self._sortUtil(dependentNode, visited, sorted)

            sorted.insert(0, node)

    def topologicalSort(self):
        visited = dict([(node, False) for node in self.nodes])         
        sorted = []
        
        for node in self.nodes:
            if visited[node] == False:
                self._sortUtil(node, visited, sorted)

        return list(reversed(sorted))