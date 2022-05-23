# -*- coding: utf-8 -*-
import argparse
import os


def main(read_file_name, TIMESTAMP):
    print("split", read_file_name, "by", str(TIMESTAMP))
    index = read_file_name.rfind(".")
    write_before_file_name = read_file_name[:index] + "_load_data.txt"
    write_after_file_name = read_file_name[:index] + "_train.txt"
    file_before_write = open(write_before_file_name, "w");
    file_after_write = open(write_after_file_name, "w");
    file_before_write.write("type address size block_address\n")  # write header
    file_after_write.write("type address size block_address\n")  # write header
    file_before_write.close()
    file_after_write.close()

    file_before_write = open(write_before_file_name, "a")
    file_after_write = open(write_after_file_name, "a")
    with open(read_file_name) as f:
        for line in f:
            if line.startswith('read') or line.startswith('write'):
                data_line = line.split()
                current_time = data_line.pop()
                block_address = int(str(data_line[1]), 16)
                data_line.append(str(block_address))
                if float(current_time) < TIMESTAMP:
                    file_before_write.write(" ".join(data_line) + "\n")
                else:
                    file_after_write.write(" ".join(data_line) + "\n")
    file_before_write.close()
    file_after_write.close()


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else:
        return arg


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='divide file by time & remove timestamp and calculate block address')
    parser.add_argument("-i", dest="filename", required=True,
                        help="input raw trace data",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-t", dest="timestamp", required=True,
                        help="input time basis(sec)", type=float)
    args = parser.parse_args()
    main(args.filename, args.timestamp)
