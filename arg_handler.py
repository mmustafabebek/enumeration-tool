import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Check cloud service accessibility for a given name.")
    parser.add_argument("name", help="Name to check for accessibility")
    parser.add_argument("-k", "--keyword", help="Similar keyword to check for", default=None)
    return parser

def parse_args():
    parser = create_parser()
    return parser.parse_args()
