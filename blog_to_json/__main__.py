import argparse

import xmltodict

from json import dumps

from . import (
    wordpress_xml_dict_to_normalized_dict,
    disqus_xml_dict_to_normalized_dict,
    graphcomment_xml_dict_to_normalized_dict
)


def get_normalized_document(dump, dump_type, *args):
    if dump_type == "wordpress":
        dump_dict = xmltodict.parse(dump)
        return wordpress_xml_dict_to_normalized_dict(dump_dict)
    elif dump_type == "disqus":
        dump_dict = xmltodict.parse(dump)
        return disqus_xml_dict_to_normalized_dict(dump_dict)
    elif dump_type == "graphcomment":
        dump_dict = xmltodict.parse(dump)
        return graphcomment_xml_dict_to_normalized_dict(dump_dict, args[0])
    else:
        raise Exception("invalid dump type.")


def default_parser():
    parser = argparse.ArgumentParser(description="Convert a blog dump to JSON.")
    parser.add_argument(
        "path",
        type=argparse.FileType("r"),
        help="Path to the blog dump.",
    )
    return parser


def _main(parser):
    args = parser.parse_args()
    with args.path as f:
        dump = f.read()

    if args.type is not "graphcomment":
        normalized_document = get_normalized_document(dump, args.type)
    else:
        normalized_document = get_normalized_document(dump, args.type, args.host)
    json_document = dumps(normalized_document, indent=2)
    print(json_document)


def main():
    parser = default_parser()
    parser.add_argument(
        "--type",
        type=str,
        help="Type of blog dump to process.",
        choices=["wordpress", "disqus"],
    )
    _main(parser)


def main_wordpress():
    parser = default_parser()
    parser.description = "Convert Wordpress XML to JSON"
    parser.add_argument(
        "--type",
        type=str,
        help=argparse.SUPPRESS,
        default="wordpress",
    )
    _main(parser)


def main_disqus():
    parser = default_parser()
    parser.description = "Convert Disqus XML to JSON"
    parser.add_argument(
        "--type",
        type=str,
        help=argparse.SUPPRESS,
        default="disqus",
    )
    _main(parser)

def main_graphcomment():
    parser = default_parser()
    parser.description = "Convert GraphComment Wordpress XML to JSON"
    parser.add_argument(
        "--type",
        type=str,
        help=argparse.SUPPRESS,
        default="graphcomment"
    )
    parser.add_argument(
        "--host",
        type=str,
        help="The base URL of the site",
        default="https://fakesite.github.io"
    )
    _main(parser)

if __name__ == "__main__":
    main()
