import re
from io import BytesIO
from lxml import etree
# x = "-10"
# y = "-10"
# text - anchor = "end"
BRANDABLE_FORMATS = ['svg']

BRAND_WIDTH = 140
BRANDING = """
<g>
<text x="{x}" y="{y}"
    stroke="cadetblue"
    font-family="courier">
    <a href="{url}">pointillism.io</a>
</text>
</g>
"""


def get_width(svg):
    height_s = svg.attrib['width']
    index = 0
    for chr in height_s:
        if ord(chr) > 58:
            break
        index += 1

    value = int(height_s[:index])
    type_ = height_s[index:]

    return (value, type_)

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
    height = value + 50
    svg.attrib['height'] = f"{height}{type_}"
    return height


def is_brandable_format(format):
    return format in BRANDABLE_FORMATS


def brand(body, brand_link="https://pointillism.io"):
    """
    param body:
    """
    rendering = etree.parse(BytesIO(body))
    root = rendering.getroot()
    height = set_height(root)
    padding = get_width(root)[0] - BRAND_WIDTH
    root.insert(2, etree.XML(
        BRANDING.format(
            x=padding,
            y=height-30,
            url=brand_link)
    ))

    return etree.tostring(rendering).decode('utf8')  # TODO, don't decode
