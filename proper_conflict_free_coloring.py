
from pysat.solvers import Solver
from pysat.formula import IDPool
from itertools import combinations
from itertools import permutations


class ProperConflictFreeColoringSolver:

    def __init__(self, G):
        """
        Initializes a solver for computation of conflict free colorings.
        :param G: Undirected graph G as a dictionary.
        """

        self.G = G

        # initialization of private attributes
        self.variables = None
        self.solver = None


    # gives ID of SAT-variable x_{v,i}. True if and only if vertex v has color i
    def _x(self, v, i):
        return self.variables.id(f"x_{v}_{i}")


    # gives ID of SAT-variable y_{v,i}. If true, color i appears at least once in N(v)
    def _y(self, v, i):
        return self.variables.id(f"y_{v}_{i}")


    # gives ID of SAT-variable z_{v,i}. If true, color i appears at most once in N(v)
    def _z(self, v, i):
        return self.variables.id(f"z_{v}_{i}")


    # gives ID of SAT-variable q_{v,i}. If true, color i appears exactly once in N(v)
    def _q(self, v, i):
        return self.variables.id(f"q_{v}_{i}")


    def _add_conflict_coloring_constraints(self, number_colors):
        """
        Adds the SAT-constraints that define the conflict free coloring problem to self.solver.
        :param number_colors: Numbers of colors for which a coloring needs to be found.
        """

        n = len(self.G)

        # each vertex gets exactly one color
        for v in self.G:

            # v gets at least one color
            self.solver.add_clause([self._x(v, i) for i in range(number_colors)])

            for i, j in combinations(range(number_colors), 2):
                # v does not get both colors i and j
                self.solver.add_clause([-self._x(v, i), -self._x(v, j)])

        # no two adjacent vertices have the same color
        for u in self.G:
            for v in self.G[u]:
                if u < v:
                    for i in range(number_colors):
                        # not both vertices u and v have color i
                        self.solver.add_clause([-self._x(u, i), -self._x(v, i)])

        # for each non-isolated vertex v, there must be some color i that appears exactly once among N(v)
        for v in self.G:
            neighbors = self.G[v]

            if len(neighbors) == 0:
                # vertex is isolated. By definition, we do not require a unique color among its neighborhood.
                continue

            for i in range(number_colors):
                # if y(v, i), then color i appears at least once in N(v)
                self.solver.add_clause([self._x(w, i) for w in neighbors] + [-self._y(v, i)])

                # if z(v, i), then color i appears at most once in N(v)
                for w_1, w_2 in combinations(neighbors, 2):
                    self.solver.add_clause([-self._x(w_1, i), -self._x(w_2, i), -self._z(v, i)])

                # if q(v, i). then color i appears exactly once in N(v)
                self.solver.add_clause([self._y(v, i), -self._q(v, i)])
                self.solver.add_clause([self._z(v, i), -self._q(v, i)])

            # at least one color appears exactly once in N(v)
            self.solver.add_clause([self._q(v, i) for i in range(number_colors)])


    def find_coloring(self, number_colors):
        """
        Computes a conflict free coloring using number_colors if it exists.
        :param number_colors: Number of colors for the conflict free coloring.
        :return: Tuple (satisfiable, coloring). satisfiable is True if a coloring
        exists and False otherwise. If a coloring exists, coloring contains the coloring as a dictionary.
        """

        self.solver = Solver()
        self.variables = IDPool()
        self._add_conflict_coloring_constraints(number_colors)

        satisfiable = self.solver.solve()

        if satisfiable:
            model = self.solver.get_model()
            coloring = {}
            for v in self.G:
                for i in range(number_colors):
                    if self._x(v, i) in model:
                        coloring[v] = i
                        break
            return True, coloring
        else:
            return False, None


    def enumerate_colorings(self, number_colors):
        """
        Enumerates all conflict free colorings up to permutation of colors.
        :param number_colors: Number of colors for the conflict free coloring.
        """

        self.solver = Solver()
        self.variables = IDPool()
        self._add_conflict_coloring_constraints(number_colors)

        while self.solver.solve():

            model = self.solver.get_model()

            coloring = {}
            for v in self.G:
                for i in range(number_colors):
                    if self._x(v, i) in model:
                        coloring[v] = i
                        break

            yield coloring

            for p in permutations(list(range(number_colors))):
                self.solver.add_clause([-self._x(v, list(p)[coloring[v]]) for v in self.G])


    def count_colorings(self, number_colors):
        """
        Counts all conflict free colorings up to permutation of colors.
        This function is not more efficient than enumerating them all.
        :param number_colors: Number of colors for the conflict free coloring.
        :return: Number of conflict free colorings up to permutation of colors.
        """

        count = 0
        for coloring in self.enumerate_colorings(number_colors):
            count += 1

        return count


    def conflict_free_chromatic_number(self, max_chromatic_number = None):
        """
        Computes the minimum number of colors in a conflict free coloring.
        This function successively tries to find a coloring using 1, 2, ... colors.
        :param max_chromatic_number: If specified, will not try to find a coloring using more than the specified number
        of colors.
        :return: Tuple (number, coloring), where number is the minimum number of colors in a conflict free coloring,
        and coloring is as coloring as a dictionary using the minimum number of colors.
        """

        if max_chromatic_number is None:
            upper_bound = len(self.G)
        else:
            upper_bound = max_chromatic_number

        for k in range(upper_bound + 1):
            satisfiable, coloring = self.find_coloring(k)
            if satisfiable:
                return (k, coloring)

        raise Exception(f"No conflict free coloring found using up to {upper_bound} colors!")