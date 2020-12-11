
def read_input(filename='input', separator=''):
    with open(filename, 'r') as f:
        contents = f.read()

    if len(separator) > 0:
        return contents.split(separator)

    if not contents[-1]:
        # remove last newline
        return contents[:-1]
    else:
        return contents