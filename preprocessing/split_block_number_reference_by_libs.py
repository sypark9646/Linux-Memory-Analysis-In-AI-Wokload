import argparse
import json
import os

import pandas as pd
from alive_progress import alive_bar


def load_logfile_to_dictionary(filename):
    print("load logfile to dictionary")
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def main(read_txt_file, mapping_dictionary_file):
    library_maps = load_logfile_to_dictionary(mapping_dictionary_file)

    index = read_txt_file.rfind(".")
    write_file_name = read_txt_file[:index]

    df = pd.read_csv(read_txt_file, delimiter=' ', lineterminator='\n', header=None)
    df.columns = ['index', 'type', 'library_number', 'block_number']

    num_lines = len(library_maps)
    with alive_bar(num_lines, force_tty=True) as bar:
        for key in library_maps.keys():
            library_number = library_maps[key]
            filtered_df = df[df['library_number'] == library_number]
            filtered_df.to_csv(write_file_name+"_"+str(library_number)+".csv", encoding='utf-8')
            bar()


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else:
        return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='preprocess to draw block number - logical time reference graph')
    parser.add_argument("-i", dest="txt_file", required=True,
                        help="input block number referenced txt file",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-json", dest="mapping_dictionary_file", required=True,
                        help="input library:number dictionary json file",
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    main(args.txt_file, args.mapping_dictionary_file)
