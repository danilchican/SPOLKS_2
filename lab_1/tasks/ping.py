import argparse
import os
import sys

from multiprocessing import Pool

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path[:-6])

from request.ping import PingRequest
from request.exceptions.unable_to_resolve_error import UnableToResolveError


def thread_exec(args):
    try:
        ping = PingRequest(args[0], args[1], args[3], args[2])
        ping.run()
        ping.statistic()
    except UnableToResolveError as errno:
        print(errno)
    except KeyboardInterrupt:
        print("\nping interrupted by user.")
        sys.exit(1)
    except:
        raise


def main():
    args = _parse_args(sys.argv[1:])
    settings = [args.count, args.size, args.timeout]
    options = [(host, *settings) for host in args.dest]

    with Pool(len(args.dest)) as pool:
        pool.map(thread_exec, options)


if __name__ == '__main__':
    main()


def _parse_args(args):
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=46, width=100)
    parser = argparse.ArgumentParser(
        description="Python parallel ping util", formatter_class=formatter)

    parser.add_argument("-d", "--dest", nargs="+",
                        help="<Required> list of hosts (at least one)",
                        required=True)
    parser.add_argument("-c", "--count", type=int, default=3,
                        help="count of packages will be sent")
    parser.add_argument("-t", "--timeout", type=int, default=5,
                        help="ping reply wait timeout")
    parser.add_argument("-s", "--size", type=int, default=32,
                        help="size of echo package payload")

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    return parsed_args
