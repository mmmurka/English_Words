"""Console migrate tool."""

import logging.config
import typing


def main() -> None:
    """Run console tool."""
    log_level = 'INFO'
    log_config: typing.Dict[str, typing.Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(asctime)s [%(levelname)s] (%(name)s) %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S%Z',
            },
        },
        'handlers': {
            'stdout': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'level': log_level,
                'formatter': 'simple',
            },
        },
        'loggers': {
            '': {
                'handlers': ['stdout'],
                'level': log_level,
            },
        },
    }
    logging.config.dictConfig(log_config)


if __name__ == '__main__':
    main()
