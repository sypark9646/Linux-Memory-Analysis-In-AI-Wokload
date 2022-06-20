import argparse
import os
import sys

def main(read_file_name, write_file_name, start_time, end_time):
  print("clear", read_file_name)
  write_file_name = write_file_name+"_clear.txt"
  file_write = open(write_file_name, "w");
  file_write.write("type address size block_address\n") # write header
  file_write.close()

  file_write = open(write_file_name, "a");
  with open(read_file_name) as f:
      for line in f:
        if (line.startswith('read') or line.startswith('write')):
          data_line = line.split()
          if float(data_line[-1]) > end_time:
            break
          if float(data_line[-1]) <= start_time:
            data_line.pop()
            block_address = int(str(data_line[1]), 16)
            data_line.append(str(block_address))
            file_write.write(" ".join(data_line)+"\n")
  file_write.close()

def is_valid_file(parser, arg):
  if not os.path.exists(arg):
      parser.error("The file %s does not exist" % arg)
  else:
      return arg


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description = 'remove timestamp and calculate block address')
  parser.add_argument("-input", dest="input", required=True,
                    type=lambda x: is_valid_file(parser, x))
  parser.add_argument("-output", dest="output", required=True,
                    type=str)
  parser.add_argument("-start", dest="start", required=True,
                    type=float)
  parser.add_argument("-end", dest="end", required=True,
                    type=float)
  args = parser.parse_args()
  main(args.input, args.output, args.start, args.end)
