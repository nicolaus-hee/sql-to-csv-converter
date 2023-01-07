#!/usr/bin/env python3
from datetime import datetime
import argparse

def is_insert_line(line: str) -> bool:
    if("INSERT INTO" in line):
        return True
    else:
        return False

def first_insert_line(source_file: str) -> int:
    i = 0
    with open(source_file, "r") as infile:
        for line in infile:
            i += 1
            if(is_insert_line(line)):
                return i
    return -1

def find_nth_occurrence(haystack: str, needle: str, n: int) -> int:
    index = 0
    start_pos = 0
    for i in range(1, n + 1):
        index = haystack.find(needle, start_pos)
        if(i == n):
            return index
        start_pos = index + 1
    return -1

def convert_line(line: str) -> str:
    replace_terms = {
        "(": "",
        "),": "",
        ");": "",
        "	": "",
        "        ": "",
        ", ": ",",
        "`": "",
        ") VALUES": ""
    }

    for r in replace_terms:
        line = line.replace(r, replace_terms[r])

    if(is_insert_line(line)):
        line = line[find_nth_occurrence(line, " ", 3)+1:]

    return line

def convert_file(source_file: str, target_file: str) -> bool:
    i = 0
    skip_lines = first_insert_line(source_file) - 1

    with open(source_file, "r") as infile:
        append_text = ""
        headers_added = False

        for line in infile:
            i += 1
            if(i > skip_lines):
                if not (is_insert_line(line)):
                        append_text += convert_line(line)
                else:
                    if (headers_added == False):
                        append_text += convert_line(line)
                        headers_added = True

            if(i % 10000 == 0):
                append_line(target_file, append_text)
                append_text = ""

            # print status every 10k iterations
            if(i % 10000 == 0):
                print(str(datetime.now()) + " --> " + str(i))

        # append what is left over > 10k lines
        append_line(target_file, append_text)
    return True

def append_line(target_file: str, line: str) -> bool:
    with open(target_file, "a") as file:
        file.write(line)
    return True

def main():   
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--source_file', type=str, help='name of input file', required=True)
    parser.add_argument('-t','--target_file', type=str, help='name of output file', required=True)
    args = parser.parse_args()

    print(str(datetime.now()) + " --> start")
    convert_file(args.source_file, args.target_file)
    print(str(datetime.now()) + " --> end")

if __name__ == "__main__":
    main()