

LOG_LEVEL_ERROR = 3
LOG_LEVEL_WARN = 2
LOG_LEVEL_NOTIFY = 1
LOG_LEVEL_IGNORE = 0

LOG_LEVEL_ENABLED = LOG_LEVEL_WARN


def logd(opt, log):
    if opt >= LOG_LEVEL_ENABLED:
        print(log)