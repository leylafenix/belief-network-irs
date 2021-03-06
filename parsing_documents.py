__author__ = 'Jose Gabriel'

import os
import pprint


def read_block(f):
    s = ""
    line = f.readline()
    while line and not line.startswith("."):
        s += line
        line = f.readline()
    return s, line


def read_doc(f):
    doc = {"title": "", "authors": "", "content": ""}

    line = f.readline()
    while line and not line.startswith(".I"):
        if line.startswith(".T"):
            doc["title"], line = read_block(f)
        elif line.startswith(".A"):
            doc["authors"], line = read_block(f)
        elif line.startswith(".W"):
            doc["content"], line = read_block(f)
        else:
            _, line = read_block(f)
    return doc, line


def create_doc(data, out_folder, name):
    with open(out_folder + os.sep + name, 'w') as f:
        f.write(data["title"] + "\n")
        f.write(data["content"] + "\n")
        f.write(data["authors"])


def parse_all(s, out_folder):
    with open(s) as f:
        line = f.readline()  # .I
        while line:
            doc_name = "d%03d.txt" % (int(line.strip().split()[-1]))
            doc, line = read_doc(f)
            create_doc(doc, out_folder, doc_name)
            # print("**********************************")


if __name__ == '__main__':
    s = "adi" + os.sep + "ADI.ALL"
    out_folder = "test_index"

    try:  # averiguar como preguntar si una carpeta o fichero existe en python
        os.mkdir(out_folder)
    except FileExistsError:
        pass

    parse_all(s, out_folder)
