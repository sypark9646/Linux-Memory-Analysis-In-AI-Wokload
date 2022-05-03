# -*- coding: utf-8 -*-

import argparse
import json
import os
import time

import pandas as pd
from alive_progress import alive_bar

import csv
import zlib

def txt_to_csv(filename):
    index = read_file_name.rfind(".")
    write_file_name = read_file_name[:index]+".csv"
    
    with open(filename, 'r') as in_file:
        lines = in_file.read().splitlines()
        stripped = [line.replace(","," ").split() for line in lines]
        grouped = zip(*[stripped]*1)
        with open(write_file_name, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('index', 'block_number'))
            for group in grouped:
                writer.writerows(group)

def preprocess_block_number(read_file_name, write_file_name):
    file_write = open(write_file_name, "a");
    index = 0
    block_num_map = {}
    block_number = 0
    num_lines = sum(1 for line in open(read_file_name))
    with alive_bar(num_lines, force_tty=True) as bar:
      with open(read_file_name) as f:
        for line in f:
          if (line.startswith('read') or line.startswith('write')):
            data_line = line.split()
            block_address = data_line[-1]
            data_line.insert(0,str(index))
            index += 1
            if block_address not in block_num_map:
              block_number += 1
              block_num_map[block_address] = block_number
            data_line.append(str(block_num_map[block_address]))
            file_write.write(" ".join(data_line)+"\n")
          bar()
    file_write.close()
    print(len(block_num_map))

def main(read_file_name, write_file_name):
    preprocess_block_number(read_file_name, write_file_name)
    txt_to_csv(write_file_name)

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else:
        return arg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='preprocess to draw blocknumber - logicaltime reference graph')
    parser.add_argument("-i", dest="read_file_name", required=True,
                        help="input trace data",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-c", dest="write_file_name", default=1000000, type=str,
                        help="output csv file")
    args = parser.parse_args()
    main(args.read_file_name, args.write_file_name)
