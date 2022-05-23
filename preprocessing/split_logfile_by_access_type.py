# -*- coding: utf-8 -*-
import argparse
import os

from alive_progress import alive_bar


def split_by_type(read_file_name):
    index = read_file_name.rfind(".")
    write_file_name = read_file_name[:index]
    write_file_names = {'readi': write_file_name + "_readi.txt", 'readd': write_file_name + "_readd.txt", 'write': write_file_name + "_write.txt"}
    write_file_counts = {}
    write_file_pointers = {}
    for access_type in write_file_names.keys():
        write_file_pointers[access_type] = open(write_file_names.get(access_type), "a")

    num_lines = sum(1 for _ in open(read_file_name))
    with alive_bar(num_lines, force_tty=True) as bar:
        with open(read_file_name) as f:
            for line in f:
                if line.startswith('read') or line.startswith('write'):
                    data_line = line.split()
                    data_line.pop()  # time
                    data_line.pop()  # size
                    block_address = int(data_line[1], 16)
                    access_type = data_line.pop(0)  # type
                    data_line.insert(0, str(write_file_counts.get(access_type, 0)))  # index
                    write_file_counts[access_type] = write_file_counts.get(access_type, 0) + 1
                    data_line.append(str(block_address))
                    write_file_pointers.get(access_type).write(" ".join(data_line) + "\n")  # index address block_address
                bar()

    for pointer in write_file_pointers.keys():
        write_file_pointers[pointer].close()
    for access_type in write_file_counts.keys():
        print(access_type, str(write_file_counts[access_type]+1))


def main(read_file_name):
    print("split", read_file_name, "by access type")
    split_by_type(read_file_name)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else:
        return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='preprocess to draw block number - logical time reference graph')
    parser.add_argument("-i", dest="read_file_name", required=True,
                        help="input trace data",
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    main(args.read_file_name)
