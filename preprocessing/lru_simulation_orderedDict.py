# -*- coding: utf-8 -*-
"""LRU_simulation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FKQIevw4094wCv1kxtDdK6SXBuAtp6sE
"""

from collections import OrderedDict
from alive_progress import alive_bar
import pandas as pd
import argparse
import os
import sys
import time
import json

class LRUCache: # Both reads & writes affect rank changes
    def __init__(self):
        self.cache = OrderedDict()
        # self.capacity = capacity # initialising capacity

    def read(self, key: int) -> int:
        index = 1
        rank = -1
        for i in self.cache.keys(): # return previous rank of key 
          if i == key:
            rank = index
            break
          index += 1
        if rank != -1: # if key in the cache list
          self.cache.move_to_end(key, last=False) # move the key to the front when recently used
        return rank
 
    def write(self, key: int) -> int:
        rank = self.read(key)
        if rank == -1: # if key is not in the cache list
          self.cache[key] = None
          self.cache.move_to_end(key, last=False)
        return rank

def tojson(pointer, write_file_name, ranking_access):
  with open(f"{write_file_name}_LRU_{pointer}.json", 'w') as fp:
    json.dump(ranking_access, fp)
  print("saved", f"{write_file_name}_LRU_{pointer}.json")

def totxt(pointer, write_file_name, ranking_access):
  file_write = open(f"{write_file_name}_LRU_{pointer}.txt", "w");
  file_write.write("rank access_number\n")
  for rank in sorted(ranking_access):
    file_write.write(str(rank)+" "+str(ranking_access[rank])+"\n")
  print("saved", f"{write_file_name}_LRU_{pointer}.txt")
  file_write.close()

def main(read_file_name, STEP):
  print("process", read_file_name, "and save every", str(STEP), "lines.")
  index = read_file_name.rfind(".")
  write_file_name = read_file_name[:index]

  ranking_access = {}
  cache = LRUCache()

  pointer = 0
  num_lines = sum(1 for line in open(read_file_name))
  for chunks in pd.read_csv(read_file_name, chunksize=STEP, skiprows = 1, names=['type', 'address', 'size', 'block_address'], skipinitialspace=True, delim_whitespace=True, lineterminator="\n"):
    with alive_bar(num_lines, force_tty=True) as bar:
      chunks = chunks.reset_index()
      for index, chunk in chunks.iterrows():
        rank = -1
        if chunk['type'].startswith('read'):
          rank = cache.read(chunk['block_address'])
        else: #data_type.startswith('write'):
          rank = cache.write(chunk['block_address'])

        if rank != -1:
          ranking_access.setdefault(rank, 0)
          ranking_access[rank] = ranking_access[rank] + 1
    
        pointer += 1
        time.sleep(.005)
        bar()
      
      tojson(pointer, write_file_name, ranking_access) # check point
  totxt(pointer, write_file_name, ranking_access)

def is_valid_file(parser, arg):
  if not os.path.exists(arg):
      parser.error("The file %s does not exist" % arg)
  else:
      return arg
      
      
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description = 'simulation LRU policy and return ranking - access count txt file')
  parser.add_argument("-i", dest="filename", required=True,
                    help="input cleared trace data",
                    type=lambda x: is_valid_file(parser, x))
  parser.add_argument("-c", dest="step", default=1000000, type=int,
                    help="checkpoint for step")
  args = parser.parse_args()
  main(args.filename, args.step)