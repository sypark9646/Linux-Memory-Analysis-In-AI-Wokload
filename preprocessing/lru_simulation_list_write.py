# -*- coding: utf-8 -*-

import argparse
import json
import os
import time

import pandas as pd
from alive_progress import alive_bar


class LRUCache:  # Only write affect rank changes
    def __init__(self):
        self.cache = []
        self.addresses = set()
        # self.capacity = capacity # initialising capacity

    def read(self, key: int) -> int:
        if key in self.addresses:  # re-referenced
            rank = 1
            for i in self.cache:  # return previous rank of key
                if i == key:
                    break
                rank += 1
            return rank
        return -1

    def write(self, key: int) -> int:
        rank = self.read(key)
        if rank != -1:  # re-referenced
            self.cache.insert(0, key)
            self.addresses.add(key)
        return rank


def to_json(pointer, write_file_name, ranking_access):
    with open(f"{write_file_name}_LRU_{pointer}.json", 'w') as fp:
        json.dump(ranking_access, fp)
    print("saved", f"{write_file_name}_LRU_{pointer}.json")


def to_txt(write_file_name, type, ranking_access):
    file_write = open(f"{write_file_name}_{type}_LRU.txt", "w")
    file_write.write("rank access_number\n")
    for rank in sorted(ranking_access):
        file_write.write(str(rank) + " " + str(ranking_access[rank]) + "\n")
    file_write.close()


def main(read_file_name):
    print("process", read_file_name, "and save every", str(step), "lines.")
    index = read_file_name.rfind(".")
    write_file_name = read_file_name[:index]

    read_ranking_access = {}
    write_ranking_access = {}
    cache = LRUCache()

    pointer = 0
    num_lines = sum(1 for line in open(read_file_name))
    with alive_bar(num_lines, force_tty=True) as bar:
        for chunks in pd.read_csv(read_file_name, chunksize=1000000, skiprows=1,
                                  names=['type', 'address', 'size', 'block_address'], skipinitialspace=True,
                                  delim_whitespace=True, lineterminator="\n"):
            # with alive_bar(step, force_tty=True) as bar:
            chunks = chunks.reset_index()
            for index, chunk in chunks.iterrows():
                rank = -1
                if chunk['type'].startswith('read'):
                    rank = cache.read(chunk['block_address'])
                else:  # data_type.startswith('write'):
                    rank = cache.write(chunk['block_address'])

                if rank != -1:
                    if chunk['type'].startswith('read'):
                        read_ranking_access.setdefault(rank, 0)
                        read_ranking_access[rank] = read_ranking_access[rank] + 1
                    else:  # data_type.startswith('write'):
                        write_ranking_access.setdefault(rank, 0)
                        write_ranking_access[rank] = write_ranking_access[rank] + 1

                pointer += 1
                time.sleep(.005)
                bar()
    to_txt(write_file_name, 'read', read_ranking_access)
    to_txt(write_file_name, 'write', write_ranking_access)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else:
        return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='simulation LRU policy and return ranking - access count txt file')
    parser.add_argument("-i", dest="filename", required=True,
                        help="input cleared trace data",
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    main(args.filename)
