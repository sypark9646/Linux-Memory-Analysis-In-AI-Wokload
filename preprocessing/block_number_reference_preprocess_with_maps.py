# -*- coding: utf-8 -*-
import argparse
import csv
import os
import json
from aenum import Enum

from alive_progress import alive_bar


class Type(Enum):
    READI = 1
    READD = 2
    WRITE = 3

    @classmethod
    def _missing_name_(cls, name):
        for member in cls:
            if member.name.lower() == name.lower():
                return member


class ProcessMapping:
    def __init__(self):
        self.libraries = []
        self.start_addresses = []
        self.end_addresses = []
        self.library_to_int = {}

    def load_mapping_file(self, read_file_name):
        print("load mapping file", read_file_name)
        for line in open(read_file_name, 'r').readlines():
            variables = line.split()
            if variables[-1] == '0':  # indicates that no inode is associated with the memory region
                continue
            start_address, end_address = variables[0].split('-')
            start_block_address = int(str(start_address), 16)
            end_block_address = int(str(end_address), 16)
            library = variables[-1]
            if not self.libraries or variables[-1] != self.libraries[-1]:  # if maps empty
                self.libraries.append(library)
                self.start_addresses.append(start_block_address)
                self.end_addresses.append(end_block_address)
            else:
                self.end_addresses[-1] = end_block_address

        for index in range(len(self.libraries)):
            self.library_to_int[self.libraries[index]] = index

        print("load mapping file end!!!")

    def get_library_name(self, block_address):
        for index in range(len(self.start_addresses)):
            if self.start_addresses[index] <= block_address < self.end_addresses[index]:
                return self.libraries[index]
        return None


def txt_to_csv(filename):
    index = filename.rfind(".")
    write_file_name = filename[:index] + ".csv"

    with open(filename + ".txt", 'r') as in_file:
        lines = in_file.read().splitlines()
        stripped = [line.replace(",", " ").split() for line in lines]
        grouped = zip(*[stripped] * 1)
        with open(write_file_name, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('index', 'type', 'library_number', 'block_number'))
            for group in grouped:
                writer.writerows(group)


def to_json(file_name, dictionary):
    with open(f"{file_name}_dictionary.json", 'w') as fp:
        json.dump(dictionary, fp)
    print("saved", f"{file_name}_library_accessCount.json")


def preprocess_block_number(write_file_name, read_file_name, process_mapping):
    file_write = open(write_file_name + ".txt", "a")

    index = 0
    block_num_map = {}
    block_number = 0
    num_lines = sum(1 for _ in open(read_file_name))
    with alive_bar(num_lines, force_tty=True) as bar:
        with open(read_file_name) as f:
            for line in f:
                if line.startswith('read') or line.startswith('write'):
                    data_line = line.split()
                    data_line.pop()  # time
                    data_line.pop()  # size
                    block_address = int(data_line[1], 16)
                    data_line.pop()  # address
                    data_line.insert(0, str(index))

                    access_type = data_line.pop()
                    type_to_int = Type[access_type].value  # type
                    data_line.append(str(type_to_int))

                    library_name = process_mapping.get_library_name(block_address)
                    if library_name:
                        data_line.append(str(process_mapping.library_to_int[library_name]))

                    index += 1
                    if block_address not in block_num_map:
                        block_number += 1
                        block_num_map[block_address] = block_number
                    data_line.append(str(block_num_map[block_address]))

                    file_write.write(" ".join(data_line) + "\n")
                bar()

    file_write.close()
    print(len(block_num_map))


def main(read_file_name, mapping_file):
    print("block number reference", read_file_name, "split by", mapping_file)
    index = read_file_name.rfind(".")
    write_file_name = "block_number_reference_" + read_file_name[:index]

    process_mapping = ProcessMapping()
    process_mapping.load_mapping_file(mapping_file)
    to_json(write_file_name, process_mapping.library_to_int)

    preprocess_block_number(write_file_name, read_file_name, process_mapping)
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
    parser.add_argument("-maps", dest="mapping_file", required=True,
                        help="input proc/process_id/maps memory mapping file",
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    main(args.read_file_name, args.mapping_file)
