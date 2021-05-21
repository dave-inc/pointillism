from graphviz import Source


def remove_head(body):
    """remove everything up to first {"""
    first_char = 0
    while body[first_char] != '{':
        first_char += 1
    first_char += 1
    return body[first_char:]


def remove_tail(body):
    """remove everything after last """
    last_char = -1
    while body[last_char] != '}':
        last_char -= 1
    return body[:last_char]


def join(*bodies):
    out = remove_tail(bodies[0])

    for body in bodies[1:]:
        out += "\n"
        out += remove_head(
            remove_tail(body)
        )
    out += "}"
    return out


def get_pipe(body, format):
    src = Source(body)
    return src.pipe(format=format)
