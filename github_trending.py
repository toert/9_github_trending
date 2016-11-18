from os.path import basename, getsize, splitext, join
import os
from collections import Counter
from collections import defaultdict
import re


def are_files_duplicates(file_path1, file_path2):
    name1 = splitext(basename(file_path1))[0]
    name2 = splitext(basename(file_path2))[0]
    return bool(getsize(file_path1) == getsize(file_path2) and (name1 == name2))


def are_files_copies(file_path1, file_path2):
    name1 = splitext(basename(file_path1))[0]
    name2 = splitext(basename(file_path2))[0]
    pattern1 = '{} \(\d\)'.format(name1)
    pattern2 = '{} \(\d\)'.format(name2)
    return bool(getsize(file_path1) == getsize(file_path2) and \
                ((re.match(pattern1, name2)) or (re.match(pattern2, name1))))


def get_all_files(start_filepath):
    all_files = []
    for root, dirs, files in os.walk(start_filepath, topdown=False):
        for current_file in files:
            current_path_of_file = join(str(root), str(current_file))
            all_files.append(current_path_of_file)
    return all_files


def get_dict_with_sizes(filepath):
    dict = {}
    for path in filepath:
        dict[path] = getsize(path)
    return dict


def get_dict_of_copies(paths): #get copies like 17.txt, 17 (1).txt, 17 (2).txt, etc
    struct_files = defaultdict(list)
    only_repeating = defaultdict(list)
    sizes = get_dict_with_sizes(paths)
    were_saved = []
    number_repeat = -1
    for path_number, path in enumerate(paths[:-1]): #because the last will be compared with all other files
        if path not in were_saved:
            number_repeat = number_repeat + 1
            struct_files[number_repeat].append(path)
            does_it_have_a_couple = False
            for other_path_number, other_path in enumerate\
(list(filter(lambda filepath: sizes[filepath] == sizes[path] , paths[path_number + 1:]))):
                if are_files_copies(path, other_path):
                    does_it_have_a_couple = True
                    struct_files[number_repeat].append(other_path)
                    were_saved.append(other_path)
            if does_it_have_a_couple:
                were_saved.append(path)
    for key in struct_files:
        if len(struct_files[key]) > 1:
            only_repeating[key] = struct_files[key]
    return only_repeating


def get_dict_of_duplicates(paths):
    struct_files = defaultdict(list)
    only_repeating = defaultdict(list)
    sizes = get_dict_with_sizes(paths)
    were_saved = []
    number_repeat = -1
    for path_number, path in enumerate(paths[:-1]): #because the last will be compared with all other files
        if path not in were_saved:
            number_repeat = number_repeat + 1
            struct_files[number_repeat].append(path)
            does_it_have_a_couple = False
            for other_path_number, other_path in enumerate\
(list(filter(lambda filepath: sizes[filepath] == sizes[path] , paths[path_number + 1:]))):
                if are_files_duplicates(path, other_path):
                    does_it_have_a_couple = True
                    struct_files[number_repeat].append(other_path)
                    were_saved.append(other_path)
            if does_it_have_a_couple:
                were_saved.append(path)
    for key in struct_files:
        if len(struct_files[key]) > 1:
            only_repeating[key] = struct_files[key]
    return only_repeating


def get_list_repeating_files(filepath_folder):
    filepaths_of_all_files = get_all_files(filepath_folder)
    all_names = []
    for path in filepaths_of_all_files:
        all_names.append(basename(path))
    list_of_counts = Counter(all_names)
    list_of_counts.most_common()
    return list(filter(lambda filepath: list_of_counts[basename(filepath)] > 1\
                       , filepaths_of_all_files))


if __name__ == '__main__':
    filepath_folder = input('Enter filepath to dir: ')
    filepaths = get_all_files(filepath_folder)
    repeating_files = get_dict_of_duplicates(filepaths)
    for key in repeating_files:
        print('File {} is saved in: '.format(basename(repeating_files[key][0])))
        for path in repeating_files[key]:
            print(path)
