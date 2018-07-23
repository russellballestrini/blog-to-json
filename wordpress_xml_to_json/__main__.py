import argparse

import xmltodict

from . import wordpress_xml_dict_to_normalized_dict

from json import dumps


def main():
    parser = argparse.ArgumentParser(description="Convert Wordpress XML to JSON.")
    parser.add_argument(
        "xml",
        type=argparse.FileType("r"),
        help="The path to the Wordpress XML Dump.",
    )
    args = parser.parse_args()
    with args.xml as xml_file:
        document = xmltodict.parse(xml_file.read())

    normalized_document = wordpress_xml_dict_to_normalized_dict(document)
    json_document = dumps(normalized_document, indent=2)
    print(json_document)


if __name__ == "__main__":
    main()

