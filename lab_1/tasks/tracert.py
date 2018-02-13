import argparse
import logging
import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path[:-6])

from request.exceptions.unable_to_resolve_error import UnableToResolveError
from request.traceroute import TraceRouteRequest

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__file__)


def _parse_args(args):
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=46,
                                                    width=100)
    parser = argparse.ArgumentParser(
        description="Python tracing route util", formatter_class=formatter)

    parser.add_argument("-d", "--dest", type=str,
                        help="<Required> host name", required=True)
    parser.add_argument("-c", "--count", type=int, default=30,
                        help="count of hops")
    parser.add_argument("-t", "--timeout", type=int, default=5,
                        help="trace reply timeout")

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    return parsed_args


def main():
    args = _parse_args(sys.argv[1:])

    LOGGER.info('traceroute run configuration')
    LOGGER.info('destination = %s', args.dest)
    LOGGER.info('hops count = %d', args.count)
    LOGGER.info('reply timeout = %d seconds\n', args.timeout)

    try:
        trace = TraceRouteRequest(args.dest, args.count, args.timeout)
        trace.run()
    except UnableToResolveError as errno:
        print(errno)
    except KeyboardInterrupt:
        print("\ntracing route interrupted by user.")
        sys.exit(1)
    except:
        raise


if __name__ == '__main__':
    main()