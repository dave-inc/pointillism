import re
from io import BytesIO
from lxml import etree
# x = "-10"
# y = "-10"
# text - anchor = "end"
BRANDABLE_FORMATS = ['svg']

BRANDING = """
<g a="sdf"  y="{}px">
<text
    stroke="cadetblue"
    font-family="courier">
    <a href="https://pointillism.io">pointillism.io</a>
</text>
</g>
"""


def get_height(svg):
    height_s = svg.attrib['height']
    index = 0
    for chr in height_s:
        if ord(chr) > 58:
            break
        index += 1

    value = int(height_s[:index])
    type_ = height_s[index:]

    return (value, type_)


def set_height(svg):
    height_s = svg.attrib['height']
    index = 0
    for chr in height_s:
        if ord(chr) > 58:
            break
        index += 1

    value = int(height_s[:index])
    type_ = height_s[index:]
    height = value + 25
    # svg.attrib['height'] = f"{height}{type_}"
    return height


def is_brandable_format(format):
    return format in BRANDABLE_FORMATS


def brand(body):
    """
    param body:
    """
    rendering = etree.parse(BytesIO(body))
    root = rendering.getroot()
    height = set_height(root)
    root.insert(2, etree.XML(BRANDING.format(height-25)))
    return etree.tostring(rendering).decode('utf8')  # todo, don't decode


