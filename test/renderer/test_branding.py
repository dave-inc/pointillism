from pytest import fixture
from point.renderer.render import get_pipe
from lxml import etree
from io import BytesIO
from point.renderer.branding import get_height, set_height

# TODO shared fixtures
BODY = """
digraph Test {
    A -> {B, C, D}
}
"""


class TestBranding:
    @fixture
    def body(self):
        return get_pipe(BODY, format="svg")

    def test_url(self, body):
        assert 'pointillism.io' in body

    def test_svg_height(self, body):
        root = etree.parse(body).getroot()

        assert get_height(root)[0] == 100

