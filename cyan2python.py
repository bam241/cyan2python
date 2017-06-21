#! /usr/bin/env python
from __future__ import print_function, unicode_literals
import math
import os
import sys
import subprocess
import io
import copy
import numpy as np
import pandas as pd

def get_timestep():
  cmd = "cyan -db cyclus.sqlite infile |grep duration | cut -d\< -f2 |cut -d\> -f2"
  ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  timestep = int(ps.communicate()[0][:-1])
  return timestep

def cyan(cmd):
    output = subprocess.check_output(cmd.split())
    buf = output.decode("utf-8")
    lines = buf.splitlines()
    matrix = []
    for line in lines:
        cols = line.split()
        matrix.append(cols)
    return matrix[1:]


def translate_info(input, size, lengh):
    output = np.zeros(lengh, dtype=np.float64)
    for couple in input:
        output[int(couple[0])] += float(couple[1])
    return output


def inventories(db='cyclus.sqlite', facilities=(), nucs=()):
    timestep = get_timestep()
    cmd_base = "cyan -db " + db + " inv "
    inv = []
    for name in facilities:
        cmd = cmd_base + name + " "
        inv += cyan(cmd)
    inv = translate_info(inv, 2, timestep)
    df = pd.DataFrame(data=inv)
    df.reset_index(inplace=True)
    df.columns = ['Time', 'Quantity']
    extra = copy.deepcopy(df.iloc[0]['Quantity'])
    return df
