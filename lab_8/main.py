import numpy as np
from copy import deepcopy

class Node:
    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        if isinstance(other, Node):
            return other.key == self.key
        else:
            return False


class GrafMatrix:
    def __init__(self, edge=1, no_edge=0):
        self.matrix = []
        # self.dict_node = {}
        self.tab_node = []
        self.edge = edge
        self.no_edge = no_edge

    def getVertexldx(self, vertex):
        return self.tab_node.index(vertex)

    def getVertex(self, index):
        return self.tab_node[index]

    def get_tab_node(self):
        return self.tab_node

    def neighbours(self, vertexldx):
        list_neighbours_in_matrix = self.matrix[vertexldx]
        list_neighbours = [self.tab_node[i] for i in range(len(list_neighbours_in_matrix)) if
                           list_neighbours_in_matrix[i] != 0]
        return list_neighbours

    # def neighbours(self, vertexldx):
    #    return self.tab_node[self.neighboursldx(vertexldx)]

    def order(self):
        return len(self.matrix)

    def size(self):
        sum = 0
        for elem in self.matrix:
            for item_in_elem in elem:
                if item_in_elem != self.no_edge:
                    sum += 1
        return sum

    def isEmpty(self):
        if len(self.matrix) == 0:
            return True
        else:
            return False

    def insertVerex(self, vertex):
        self.tab_node.append(vertex)
        index = self.getVertexldx(vertex)
        empty_list = [self.no_edge for i in range(len(self.tab_node) - 1)]
        self.matrix.insert(index, empty_list)

        for elem in self.matrix:
            elem.insert(index, self.no_edge)

    def insertEdge(self, vertex1, vertex2, wag):
        self.matrix[self.getVertexldx(vertex1)][self.getVertexldx(vertex2)] = wag
        self.matrix[self.getVertexldx(vertex2)][self.getVertexldx(vertex1)] = wag

    def deleteVertex(self, vertex):
        index = self.getVertexldx(vertex)
        del self.matrix[index]

        for elem in self.matrix:
            del elem[index]
        del self.tab_node[index]

    def deleteEdge(self, vertex1, vertex2):
        self.matrix[self.getVertexldx(vertex1)][self.getVertexldx(vertex2)] = self.no_edge
        self.matrix[self.getVertexldx(vertex2)][self.getVertexldx(vertex1)] = self.no_edge

    def edges(self):
        list_edges = []
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                if self.matrix[row][col] == self.edge:
                    list_edges.append((self.getVertex(row).key, self.getVertex(col).key))
        return list_edges

    def get_adjacency_matrix(self):
        return self.matrix


def create_graph(list_edge: list):
    result_graph = GrafMatrix()
    for elem in list_edge:
        v1 = Node(elem[0])
        v2 = Node(elem[1])
        if v1 not in result_graph.get_tab_node():
            result_graph.insertVerex(v1)
        if v2 not in result_graph.get_tab_node():
            result_graph.insertVerex(v2)
        result_graph.insertEdge(v1, v2, elem[2])
    return result_graph


def prune(g_matrix, p_matrix, m_matrix):
    for row_ in range(m_matrix.shape[0]):
        for col_ in range(m_matrix.shape[1]):
            if m_matrix[row_][col_] == 1:
                current_p = []
                for row_v2 in range(p_matrix.shape[0]):
                    if p_matrix[row_][row_v2] == 1:
                        current_p.append(row_v2)
                current_g = []
                for col_v2 in range(g_matrix.shape[0]):
                    if g_matrix[col_][col_v2] == 1:
                        current_g.append(col_v2)
                for x in current_p:
                    help = False
                    for y in current_g:
                        if m_matrix[x][y] == 1:
                            help = True
                            break
                    if help:
                        break
                else:
                    m_matrix[row_][col_] = 0
                    return True
    return False


def get_izomorfizm_matrixs_quantity(numpy_matrix_p, numpy_matrix_g, function_ullman):
    matrix_M = np.zeros((numpy_matrix_p.shape[0], numpy_matrix_g.shape[0]))
    used_col = [False for i in range(matrix_M.shape[1])]
    apropriate_result = []
    matrix_0 = np.zeros((numpy_matrix_p.shape[0], numpy_matrix_g.shape[0]))
    for vp in range(matrix_0.shape[0]):
        for vg in range(matrix_0.shape[1]):
            p_deg = len([elem for elem in numpy_matrix_p[vp] if elem == 1])
            g_deg = len([elem for elem in numpy_matrix_g[vg] if elem == 1])
            if p_deg <= g_deg:
                matrix_0[vp][vg] = 1

    no_recursion = function_ullman(0, matrix_M, numpy_matrix_p, numpy_matrix_g, apropriate_result, used_col, matrix_0)

    return len(apropriate_result), no_recursion


def ullman3(current_row, matrixM, m_P, m_G, apropriate_solution, used_col, matrix0, no_recursion=0):
    no_recursion = no_recursion + 1
    if current_row == matrixM.shape[0]:
        M_G = matrixM @ m_G
        m_G_t = M_G.T
        result_calculate = matrixM @ m_G_t
        if (result_calculate == m_P).all():
            apropriate_solution.append(matrixM.copy())
        return no_recursion

    copy_matrix_M = matrixM.copy()

    m_copy = deepcopy(matrixM)
    br = False
    if current_row == len(matrixM) - 1:
       br = prune(m_G, m_P, m_copy)

    for col in range(copy_matrix_M.shape[1]):
        if br == True and current_row != 0:
            break
        if used_col[col] is False and matrix0[current_row][col] == 1:
            used_col[col] = True

            for c in range(copy_matrix_M.shape[1]):
                if c == col:
                    copy_matrix_M[current_row][c] = 1
                else:
                    copy_matrix_M[current_row][c] = 0

            next_row = current_row + 1
            no_recursion = ullman3(next_row, copy_matrix_M, m_P, m_G, apropriate_solution, used_col, matrix0, no_recursion)
            used_col[col] = False
    return no_recursion


def ullman1(current_row, matrixM, m_P, m_G, apropriate_solution, used_col, matrix0, no_recursion=0):
    no_recursion = no_recursion + 1
    if current_row == matrixM.shape[0]:
        M_G = matrixM @ m_G
        m_G_t = M_G.T
        result_calculate = matrixM @ m_G_t
        if (result_calculate == m_P).all():
            apropriate_solution.append(matrixM.copy())
        return no_recursion

    copy_matrix_M = matrixM.copy()

    for col in range(copy_matrix_M.shape[1]):
        if used_col[col] is False :
            used_col[col] = True

            for c in range(copy_matrix_M.shape[1]):
                if c == col:
                    copy_matrix_M[current_row][c] = 1
                else:
                    copy_matrix_M[current_row][c] = 0

            next_row = current_row + 1
            no_recursion = ullman1(next_row, copy_matrix_M, m_P, m_G, apropriate_solution, used_col, matrix0, no_recursion)
            used_col[col] = False
    return no_recursion

def ullman2(current_row, matrixM, m_P, m_G, apropriate_solution, used_col, matrix0, no_recursion=0):
    no_recursion = no_recursion + 1
    if current_row == matrixM.shape[0]:
        M_G = matrixM @ m_G
        m_G_t = M_G.T
        result_calculate = matrixM @ m_G_t
        if (result_calculate == m_P).all():
            apropriate_solution.append(matrixM.copy())
        return no_recursion

    copy_matrix_M = matrixM.copy()

    for col in range(copy_matrix_M.shape[1]):
        if used_col[col] is False and matrix0[current_row][col] == 1:
            used_col[col] = True

            for c in range(copy_matrix_M.shape[1]):
                if c == col:
                    copy_matrix_M[current_row][c] = 1
                else:
                    copy_matrix_M[current_row][c] = 0

            next_row = current_row + 1
            no_recursion = ullman2(next_row, copy_matrix_M, m_P, m_G, apropriate_solution, used_col, matrix0, no_recursion)
            used_col[col] = False
    return no_recursion



graph_G = [('A', 'B', 1), ('C', 'D', 1), ('C', 'E', 1), ('B', 'F', 1), ('B', 'C', 1), ('D', 'E', 1)]
graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]

graph_g = create_graph(graph_G)
graph_p = create_graph(graph_P)

numpy_matrix_p1 = np.array(graph_p.get_adjacency_matrix())
numpy_matrix_g1 = np.array(graph_g.get_adjacency_matrix())

izomorfizm_matrix, quantity = get_izomorfizm_matrixs_quantity(numpy_matrix_p1, numpy_matrix_g1, ullman1)
print(izomorfizm_matrix, quantity)

izomorfizm_matrix, quantity = get_izomorfizm_matrixs_quantity(numpy_matrix_p1, numpy_matrix_g1, ullman2)
print(izomorfizm_matrix, quantity)

izomorfizm_matrix, quantity = get_izomorfizm_matrixs_quantity(numpy_matrix_p1, numpy_matrix_g1, ullman3)
print(izomorfizm_matrix, quantity)
