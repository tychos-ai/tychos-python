import sys
import argparse
from .vector_data_store import VectorDataStore

def query(args):
    tds = VectorDataStore(api_key=args.api_key)
    result = tds.query(args.name, args.query_string, args.limit)
    print(result)

def main():
    parser = argparse.ArgumentParser(description='Tychos CLI')
    subparsers = parser.add_subparsers()

    query_parser = subparsers.add_parser('query')
    query_parser.add_argument('--api-key', required=True, help='Tychos API key')
    query_parser.add_argument('--name', required=True, help='name of the index to query')
    query_parser.add_argument('--query-string', required=True, help='query string to search against index')
    query_parser.add_argument('--limit', type=int, default=5, help='number of results to return')
    query_parser.set_defaults(func=query)

    args = parser.parse_args()
    if 'func' in args:
        # Call the function associated with the provided sub-command
        args.func(args)
    else:
        # No sub-command was provided
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()