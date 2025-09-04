import unittest
from proper_conflict_free_coloring import ProperConflictFreeColoringSolver


class MyTestCase(unittest.TestCase):

    def test_peterson_graph(self):

        peterson_graph = {
            0: [1, 4, 5],
            1: [0, 2, 6],
            2: [1, 3, 7],
            3: [2, 4, 8],
            4: [0, 3, 9],
            5: [0, 7, 8],
            6: [1, 8, 9],
            7: [2, 5, 9],
            8: [3, 5, 6],
            9: [4, 6, 7]
        }

        solver = ProperConflictFreeColoringSolver(peterson_graph)

        # it is easy to verify that the Peterson graph is cannot be proper conflict-free colored using only 3 colors.
        self.assertEqual(solver.conflict_free_chromatic_number()[0], 4)
        self.assertEqual(solver.find_coloring(3), (False, None))
        self.assertEqual(solver.find_coloring(5)[0], True)

        # verify the properties of every coloring
        for coloring in solver.enumerate_colorings(4):

            # coloring uses colors 0, 1, 2, 3
            for v in coloring:
                c = coloring[v]
                self.assertEqual(c >= 0, True)
                self.assertEqual(c <= 4, True)

            # coloring is proper:
            for v in peterson_graph:
                for w in peterson_graph[v]:
                    self.assertTrue(coloring[v] != coloring[w])

            # coloring is conflict free, equivalently, no vertex has a monochromatic neighborhood
            for v in peterson_graph:
                neighbor_colors = [coloring[w] for w in peterson_graph[v]]
                self.assertTrue(not ((neighbor_colors[0] == neighbor_colors[1]) and (neighbor_colors[0] == neighbor_colors[2])))

    def test_C5(self):

        C_5 = {
            0: [4, 1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 0]
        }

        solver = ProperConflictFreeColoringSolver(C_5)
        self.assertEqual(solver.conflict_free_chromatic_number()[0], 5)

        self.assertEqual(solver.count_colorings(0), 0)
        self.assertEqual(solver.count_colorings(1), 0)
        self.assertEqual(solver.count_colorings(2), 0)
        self.assertEqual(solver.count_colorings(3), 0)
        self.assertEqual(solver.count_colorings(4), 0)
        self.assertEqual(solver.count_colorings(5), 1)
        self.assertEqual(solver.count_colorings(6), 1)
        self.assertEqual(solver.count_colorings(7), 1)


    def test_C6(self):

        C_6 = {
            0: [5, 1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 5],
            5: [4, 0]
        }

        solver = ProperConflictFreeColoringSolver(C_6)
        self.assertEqual(solver.conflict_free_chromatic_number()[0], 3)
        self.assertEqual(solver.count_colorings(3), 1)

        # it can be easily verified that there are 4 different proper conflict free colorings of C_6 using 4 colors:
        # Either there are three colors A, B, C, each of them being used twice. This gives exactly one coloring: A, B, C, A, B, C
        # Or there are two colors A, B, each used once, and two colors C, D, each used twice. A, B must appear on opposite vertices, which gives 3 possibilities.
        self.assertEqual(solver.count_colorings(4), 4)


    def test_handling_of_isolated_vertices(self):

        C_5_extra_vertices = {
            0: [4, 1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3, 0],
            5: [],
            6: []
        }

        solver = ProperConflictFreeColoringSolver(C_5_extra_vertices)
        self.assertEqual(solver.conflict_free_chromatic_number()[0], 5)

if __name__ == '__main__':
    unittest.main()
