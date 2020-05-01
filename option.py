import getopt


def get_opts2(args):
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

    sys.exit()
    return opts

def get_opts(args):
    opts = {}

    for arg in args[1:]:
        items = arg.split('--')

        while items and not items[0]:
            items.pop(0)

        for item in items:
            idx = item.find('=')
            if -1 == idx:
                continue

            opts[item[:idx]] = item[idx + 1:]

    return opts