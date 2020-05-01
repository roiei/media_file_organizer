import getopt


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