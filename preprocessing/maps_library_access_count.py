# -*- coding: utf-8 -*-
import argparse
import json
import os
import time

from alive_progress import alive_bar


class ProcessMapping:
    def __init__(self):
        self.process_libraryCount = {}
        self.libraries = []
        self.start_addresses = []
        self.end_addresses = []

    def load_mapping_file(self, read_file_name):
        for line in open(read_file_name, 'r').readlines():
            variables = line.split()
            if variables[-1] == 0:  # indicates that no inode is associated with the memory region
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

    def address_find_library(self, address):
        for index in range(len(self.libraries)):
            if address in range(self.start_addresses[index], self.end_addresses[index]):
                return self.libraries[index]
        return None

    def address_library_access_count(self, address):
        library = self.address_find_library(address)
        self.process_libraryCount[library] = self.process_libraryCount.get(library, 0) + 1


def to_json(write_file_name, process_library_count):
    with open(f"{write_file_name}_library_accessCount.json", 'w') as fp:
        json.dump(process_library_count, fp)
    print("saved", f"{write_file_name}_library_accessCount.json")


def main(read_file_name, mapping_file):
    print("count", read_file_name, "segments divided by", mapping_file)
    index = read_file_name.rfind(".")
    write_file_name = read_file_name[:index]

    process_mapping = ProcessMapping()
    process_mapping.load_mapping_file(mapping_file)

    num_lines = sum(1 for line in open(read_file_name))
    with alive_bar(num_lines, force_tty=True) as bar:
        for line in open(read_file_name, 'r').readlines():
            chunk = line.split()
            if chunk[0].startswith('read') or chunk[0].startswith('write'):
                block_address = int(str(chunk[1]), 16)
                process_mapping.address_library_access_count(block_address)

            time.sleep(.005)
            bar()
    to_json(write_file_name, process_mapping.process_libraryCount)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else:
        return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count the number of segments divided by proc maps')
    parser.add_argument("-logfile", dest="logfile", required=True,
                        help="input trace logfile",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-maps", dest="mapping_file", required=True,
                        help="input proc/process_id/maps memory mapping file",
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    main(args.logfile, args.mapping_file)
