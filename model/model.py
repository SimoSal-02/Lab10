from time import time

import networkx as nx


from database.DAO import DAO


class Model:

    def __init__(self):
        self.idMapCountry = {}
        self._grafo = nx.Graph()


    def addEdgeGraphYear(self, year):
        self._grafo.clear()
        self._country = DAO.getAllCountryYear(year)
        for i in self._country:
            self.idMapCountry[i.CCode] = i
        self._grafo.add_nodes_from(self._country)
        self._allEdges = DAO.getAllEdgesYears(self.idMapCountry,year)
        self._grafo.add_edges_from(self._allEdges)
        self._gradi = dict(self._grafo.degree)
        return nx.number_connected_components(self._grafo) , dict(sorted(self._gradi.items(), key=lambda x: x[0]))


    def cercaRaggiungibili(self,stato):
        tic = time()
        nodi = self.getDFSNodes(stato)
        toc = time()
        print(f"DFS: {toc - tic}--{len(nodi)}")

        tic = time()
        nodi = self.getBFSNodes(stato)
        toc = time()
        print(f"BFS: {toc - tic}--{len(nodi)}")

        tic = time()
        nodi = self.getNodiIterativo(stato)
        toc = time()
        print(f"ITER: {toc - tic}--{len(nodi)}")

        tic = time()
        nodi = self.getRaggiungibiliRecursive(stato)
        toc = time()
        print(f"RECUR: {toc - tic}--{len(nodi)}")

        return nodi

    def getDFSNodes(self,source):
        tree_dfs = nx.dfs_tree(self._grafo,source)
        a=list(tree_dfs.nodes)
        a.remove(source)
        return a

    def getBFSNodes(self,source):
        tree_bfs = nx.bfs_tree(self._grafo,source)
        a=list(tree_bfs.nodes)
        a.remove(source)
        return a

    def getNodiIterativo(self,source):
        visitati=set()
        daVisitare=set()
        visitati.add(source)

        vicini = self._grafo.neighbors(source)
        daVisitare.update(vicini)

        while daVisitare:
            nodoPreso=daVisitare.pop()
            visitati.add(nodoPreso)
            vicini=self._grafo.neighbors(nodoPreso)
            for vicino in vicini:
                if vicino not in daVisitare:
                    daVisitare.add(vicino)
            for nodo in visitati:
                if nodo in daVisitare:
                    daVisitare.remove(nodo)
        visitati.remove(source)
        return visitati

    def getRaggiungibiliRecursive(self,source):
        visitati=[]
        self.ricorsione(source,visitati)
        visitati.remove(source)
        return visitati
    def ricorsione(self,n,visitati):
        visitati.append(n)
        for s in self._grafo.neighbors(n):
            if s not in visitati:
                self.ricorsione(s,visitati)




