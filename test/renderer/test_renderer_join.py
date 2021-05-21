from point.renderer.render.dot import *

DOT1 = """
digraph Dot1 {
    A -> B
    B -> C
}
"""

DOT2 = """
digraph Dot2 {
    B -> D
    C -> D
}
"""

EXPECTED = """
digraph Dot1 {
    A -> B
    B -> C


    B -> D
    C -> D
}"""

class TestRendererJoin:
    def test_remove_head(self):
        result = remove_head(DOT1)
        assert DOT1[15:] == result

    def test_remove_tail(self):
        result = remove_tail(DOT1)
        assert DOT1[:-2] == result

    def test_join(self):
        result = join(DOT1, DOT2)
        assert result == EXPECTED
