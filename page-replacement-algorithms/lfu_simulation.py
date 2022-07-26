# -*- coding: utf-8 -*-
import argparse
import json
import os
import time

from alive_progress import alive_bar


class LFUCache:  # Both reads & writes affect rank changes
    def __init__(self):
        self.blockAddress_accessCount = {}
        self.accessCount_addressCount = {}
        # self.capacity = capacity # initialising capacity

    def read(self, key: int) -> int:
        if key in self.blockAddress_accessCount:  # 이전에 접근한 기록이 있는 경우
            previous_count = self.blockAddress_accessCount.get(key, 0)  # return previous count of key
            current_count = previous_count + 1
            rank = 0
            for count in self.accessCount_addressCount:
                if count > previous_count:
                    rank += self.accessCount_addressCount[count]
            # add key access_count when used
            self.blockAddress_accessCount[key] = current_count
            if previous_count != 0:
                self.accessCount_addressCount[previous_count] = self.accessCount_addressCount.get(previous_count) - 1
            self.accessCount_addressCount[current_count] = self.accessCount_addressCount.get(current_count, 0) + 1
            return rank
        # 이전에 접근한 기록이 없는 경우
        self.blockAddress_accessCount[key] = 1
        self.accessCount_addressCount[1] = self.accessCount_addressCount.get(1, 0) + 1
        return -1

    def write(self, key: int) -> int:
        rank = self.read(key)
        return rank


def to_json(pointer, write_file_name, type, ranking_access):
    with open(f"{write_file_name}_{type}_{pointer}_LFU.json", 'w') as fp:
        json.dump(ranking_access, fp)
    print(f"save {write_file_name}_{type}_{pointer}_LFU.json")


def to_txt(write_file_name, type, ranking_access):
    file_write = open(f"{write_file_name}_{type}_LFU.txt", "w")
    file_write.write("rank access_number\n")
    for rank in sorted(ranking_access):
        file_write.write(str(rank) + " " + str(ranking_access[rank]) + "\n")
    file_write.close()


def main(read_file_name):
    print("process", read_file_name)
    index = read_file_name.rfind(".")
    write_file_name = read_file_name[:index]

    read_ranking_access = {}
    write_ranking_access = {}
    cache = LFUCache()

    pointer = 0
    num_lines = sum(1 for _ in open(read_file_name))
    with alive_bar(num_lines, force_tty=True) as bar:
        with open(read_file_name) as f:
            for line in f:
                if line.startswith('read') or line.startswith('write'):
                    chunk = line.split()
                    block_address = int(chunk.pop())
                    type = chunk[0]
                    rank = -1
                    if type.startswith('read'):
                        rank = cache.read(block_address)
                    elif type.startswith('write'):  # data_type.startswith('write'):
                        rank = cache.write(block_address)

                    if rank != -1:
                        if type.startswith('read'):
                            read_ranking_access.setdefault(rank, 0)
                            read_ranking_access[rank] = read_ranking_access[rank] + 1
                        elif type.startswith('write'):
                            write_ranking_access.setdefault(rank, 0)
                            write_ranking_access[rank] = write_ranking_access[rank] + 1

                    pointer += 1
                    time.sleep(.005)
                    bar()

                if pointer % 1000000 == 0:
                    to_json(pointer, write_file_name, 'read', read_ranking_access)
                    to_json(pointer, write_file_name, 'write', write_ranking_access)
            to_txt(write_file_name, 'read', read_ranking_access)
            to_txt(write_file_name, 'write', write_ranking_access)


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
    args = parser.parse_args()
    main(args.filename)
