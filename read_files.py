
# encoding: utf-8
import json
import sys
import shutil
import csv
if sys.version_info[0]==2:
    import cPickle as pickle
else:
    import pickle
import os

def create_folder(filename):
    if "\\" in filename:
        a = '\\'.join(filename.split('\\')[:-1])
    else:
        a = '/'.join(filename.split('/')[:-1])
    if not os.path.exists(a):
        os.makedirs(a)



def save_in_json(filename, array):
    create_folder(filename)
    with open(filename, 'w') as outfile:
        json.dump(array, outfile)
    print("Save into files: ",filename)
    outfile.close()

def read_from_json(filename):
    with open(filename, 'r') as outfile:
        data = json.load(outfile)
    outfile.close()
    return data

def save_in_pickle(file,array):
    create_folder(file)
    with open(file, 'wb') as handle:
        pickle.dump(array, handle)

def read_from_pickle(file):
    with open(file, 'rb') as handle:
        if sys.version_info[0] == 2:
            data = pickle.load(handle)
        else:
            data = pickle.load(handle,encoding='latin1')
    return data

def readfrom_txt(path):
    data =open(path).read()
    return data

def textfile2list(path):
    data = readfrom_txt(path)
    txt_list =list()
    for line in data.splitlines():
        txt_list.append(line)
    return txt_list

def read_from_tsv(filename):
    with open(filename, 'r') as mycsvfile:
        files = csv.reader(mycsvfile, delimiter='\t')
        dataset = list()
        for row in files:
            dataset.append(row)
    return dataset

def read_from_csv(filename):
    with open(  filename, 'r') as mycsvfile:
        files = csv.reader(mycsvfile, delimiter=',')
        dataset = list()
        for row in files:
            dataset.append(row)
    return dataset

def save_in_tsv(filename,items):
    create_folder(filename)
    with open(filename, 'w', encoding='utf8', newline='') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
        for item in items:
            tsv_writer.writerow(item)

def save_in_txt(filename,items):
    create_folder(filename)
    with open(filename, 'w') as f:
        for item in items:
            f.write("%s\n" % item)


def add_dict(term, key, value):
    if key not in term:
        term[key] = [value]
    else:
        term[key].append(value)
    return term

def add_dict(term, key, value):
    if key not in term:
        term[key] = [value]
    else:
        term[key].append(value)
    return term

def add_dict_count(term, key, counts):
    if key not in term:
        term[key] = 1
    else:
        term[key] += 1
    return term