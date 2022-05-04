import argparse
import csv
import os

from alive_progress import alive_bar


def txt_to_csv(filename):
    index = filename.rfind(".")
    write_file_name = filename[:index] + ".csv"

    with open(filename, 'r') as in_file:
        lines = in_file.read().splitlines()
        stripped = [line.replace(",", " ").split() for line in lines]
        grouped = zip(*[stripped] * 1)
        with open(write_file_name, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('index', 'block_number'))
            for group in grouped:
                writer.writerows(group)


def preprocess_block_number(read_file_name):
    write_file_name_read = 'gnu_block_read_' + read_file_name
    write_file_name_readi = 'gnu_block_readi_' + read_file_name
    write_file_name_readd = 'gnu_block_readd_' + read_file_name
    write_file_name_write = 'gnu_block_write_' + read_file_name

    file_write_read = open(write_file_name_read, "a")
    file_write_readi = open(write_file_name_readi, "a")
    file_write_readd = open(write_file_name_readd, "a")
    file_write_write = open(write_file_name_write, "a")

    index = 0
    block_num_map = {}
    block_number = 0
    num_lines = sum(1 for line in open(read_file_name))
    with alive_bar(num_lines, force_tty=True) as bar:
        with open(read_file_name) as f:
            for line in f:
                if (line.startswith('read') or line.startswith('write')):
                    data_line = line.split()
                    data_line.pop()  # time
                    data_line.pop()  # size
                    block_address = int(data_line[1], 16)
                    data_line.pop()  # address
                    type = data_line.pop()  # type
                    data_line.insert(0, str(index))
                    index += 1
                    if block_address not in block_num_map:
                        block_number += 1
                        block_num_map[block_address] = block_number
                    data_line.append(str(block_num_map[block_address]))

                    if type.startswith('read'):
                        file_write_read.write(" ".join(data_line) + "\n")
                    if type.startswith('readi'):
                        file_write_readi.write(" ".join(data_line) + "\n")
                    if type.startswith('readd'):
                        file_write_readd.write(" ".join(data_line) + "\n")
                    if type.startswith('write'):
                        file_write_write.write(" ".join(data_line) + "\n")
                bar()

    file_write_read.close()
    file_write_readi.close()
    file_write_readd.close()
    file_write_write.close()
    print(len(block_num_map))


def main(read_file_name):
    write_file_name_read = 'gnu_block_read_' + read_file_name
    write_file_name_readi = 'gnu_block_readi_' + read_file_name
    write_file_name_readd = 'gnu_block_readd_' + read_file_name
    write_file_name_write = 'gnu_block_write_' + read_file_name

    preprocess_block_number(read_file_name)
    txt_to_csv(write_file_name_read)
    txt_to_csv(write_file_name_readi)
    txt_to_csv(write_file_name_readd)
    txt_to_csv(write_file_name_write)


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
    args = parser.parse_args()
    main(args.read_file_name)
