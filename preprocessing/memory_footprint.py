import argparse
import os

from alive_progress import alive_bar


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else:
        return arg


def main(read_file_name):
    print("process", read_file_name)

    read = set()
    write = set()
    entire = set()

    num_lines = sum(1 for line in open(read_file_name))
    with alive_bar(num_lines, force_tty=True) as bar:
        with open(read_file_name) as f:
            for line in f:
                if line.startswith('read') or line.startswith('write'):
                    chunk = line.split()
                    type = chunk[0]
                    address = chunk[1]
                    block_address = int(str(address), 16) >> 12
                    if type.startswith('read'):
                        read.add(block_address)
                    elif type.startswith('write'):
                        write.add(block_address)
                    entire.add(block_address)
                    bar()


    print('read: ' + str(len(read)*4))
    print('write: ' + str(len(write)*4))
    print('entire: ' + str(len(entire)*4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='remove timestamp and calculate block address')
    parser.add_argument("-input", dest="input", required=True,
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    main(args.input)
