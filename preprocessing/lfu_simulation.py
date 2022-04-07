# -*- coding: utf-8 -*-
"""LFU_simulation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FKQIevw4094wCv1kxtDdK6SXBuAtp6sE
"""

import argparse
import json
import os
import time

import pandas as pd
from alive_progress import alive_bar


class LFUCache:  # Both reads & writes affect rank changes
    def __init__(self):
        self.blockAddress_accessCount = {}
        self.accessCount_addressCount = {}
        # self.capacity = capacity # initialising capacity

    def read(self, key: int) -> int:
        if key in self.blockAddress_accessCount:
            current_count = self.blockAddress_accessCount.get(key)  # return previous count of key
            rank = 0
            for count in self.accessCount_addressCount:
                if count > current_count + 1:
                    rank += self.accessCount_addressCount[count]
            # add key access_count when used
            self.blockAddress_accessCount[key] = current_count + 1
            if current_count != 0:
                self.accessCount_addressCount[current_count] = self.accessCount_addressCount.get(current_count) - 1
            self.accessCount_addressCount[current_count + 1] = self.accessCount_addressCount.get(current_count + 1, 0) + 1
            return rank
        else:
            return -1

    def write(self, key: int) -> int:
        rank = self.read(key)
        if rank == -1:  # if key is not in the cache list
            self.blockAddress_accessCount[key] = 1
            self.accessCount_addressCount[1] = self.accessCount_addressCount.get(1, 0) + 1
        return rank


def tojson(pointer, write_file_name, ranking_access):
    with open(f"{write_file_name}_LFU_{pointer}.json", 'w') as fp:
        json.dump(ranking_access, fp)
    print("saved", f"{write_file_name}_LFU_{pointer}.json")


def totxt(pointer, write_file_name, ranking_access):
    file_write = open(f"{write_file_name}_LFU_{pointer}.txt", "w");
    file_write.write("rank access_number\n")
    for rank in sorted(ranking_access):
        file_write.write(str(rank) + " " + str(ranking_access[rank]) + "\n")
    print("saved", f"{write_file_name}_LFU_{pointer}.txt")
    file_write.close()


def main(read_file_name, STEP):
    print("process", read_file_name, "and save every", str(STEP), "lines.")
    index = read_file_name.rfind(".")
    write_file_name = read_file_name[:index]

    ranking_access = {}
    cache = LFUCache()

    pointer = 0
    num_lines = sum(1 for _ in open(read_file_name))
    for chunks in pd.read_csv(read_file_name, chunksize=STEP, skiprows=1,
                                  names=['type', 'address', 'size', 'block_address'], skipinitialspace=True,
                                  delim_whitespace=True, lineterminator="\n"):
        with alive_bar(num_lines, force_tty=True) as bar:
            chunks = chunks.reset_index()
            for index, chunk in chunks.iterrows():
                rank = -1
                if chunk['type'].startswith('read'):
                    rank = cache.read(chunk['block_address'])
                else:  # data_type.startswith('write'):
                    rank = cache.write(chunk['block_address'])

                if rank != -1:
                    ranking_access.setdefault(rank, 0)
                    ranking_access[rank] = ranking_access[rank] + 1

                pointer += 1
                time.sleep(.005)
                bar()
            tojson(pointer, write_file_name, ranking_access)  # check point
    totxt(pointer, write_file_name, ranking_access)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else:
        return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='simulation LFU policy and return ranking - access count txt file')
    parser.add_argument("-i", dest="filename", required=True,
                        help="input cleared trace data",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-c", dest="step", default=1000000, type=int,
                        help="checkpoint for step")
    args = parser.parse_args()
    main(args.filename, args.step)