import getopt


def get_opts(args):
    opts = {}

    for arg in args:
        items = arg.split()

        for item in items:
            if not item.startswith('--'):
                continue
            idx = item.find('=')
            if -1 == idx:
                continue

            opts[item[2:idx]] = item[idx + 1:]

    return opts