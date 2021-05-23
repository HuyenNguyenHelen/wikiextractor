# -*- coding: utf-8 -*-
"""
Python File Template 
"""

import os
import shutil

import numpy as np
import json

__author__ = "Rui Meng"
__email__ = "rui.meng@pitt.edu"

def text2chunks(pars, max_word_per_example=0, verbose=False):
    if max_word_per_example and max_word_per_example > 0 and len(pars) > 0:
        new_pars = []
        tmp_par = []
        tmp_par_len = 0
        for par in pars:
            par = par.strip()
            if len(par) == 0: continue

            if tmp_par_len + len(par.split()) >= max_word_per_example:
                tmp_par = ' \n '.join(tmp_par)
                new_pars.append(tmp_par)
                tmp_par = [par]
                tmp_par_len = len(par.split())
            else:
                tmp_par.append(par)
                tmp_par_len += len(par.split())

        if len(tmp_par) > 0:
            tmp_par = ' \n '.join(tmp_par)
            new_pars.append(tmp_par)

        if verbose:
            print('Merge short paragraphs to up to %d characters' % max_word_per_example)
            print('\t\t#before=%d, avg #word=%d' % (len(pars), np.mean([len(p.split()) for p in pars])))
            print('\t\t#after=%d, avg #word=%d' % (len(new_pars), np.mean([len(p.split()) for p in new_pars])))
        pars = new_pars

    return pars

def ord2name(folder_ord):
    first_ord = folder_ord // 26
    second_ord = folder_ord % 26

    return chr(65+first_ord) + chr(65+second_ord)

if __name__ == '__main__':
    input_dir = '/home/ubuntu/efs/rum20/data/books/dump/'
    output_base_dir = '/home/ubuntu/efs/rum20/data/books/processed/'
    max_word_per_example = 512
    max_example_per_file = 500
    max_file_per_folder = 100

    folder_ord = 0
    file_ord = 0
    num_example = 0

    output_dir = os.path.join(output_base_dir, ord2name(folder_ord))
    if os.path.exists(output_dir): shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    output_file = open(os.path.join(output_dir, 'book_{:02d}.json'.format(file_ord)), 'w')

    for book_id, input_file_name in enumerate(os.listdir(input_dir)):
        file_path = os.path.join(input_dir, input_file_name)

        book_name = input_file_name[: -9]
        lines = open(file_path, 'r').readlines()

        print('*' * 50)
        print('Book:\t', book_name)

        pars = text2chunks(lines, max_word_per_example=max_word_per_example, verbose=True)

        for par in pars:
            ex_dict = {
                'id': 'book_%d_%d' % (book_id, num_example),
                'title': book_name,
                'file': input_file_name,
                'text': par
            }
            # print(ex_dict)
            output_file.write(json.dumps(ex_dict) + '\n')

            num_example += 1
            if num_example > 0 and num_example % max_example_per_file == 0:
                output_file.close()

                new_folder_ord = num_example // max_example_per_file // max_file_per_folder
                if new_folder_ord != folder_ord:
                    folder_ord = new_folder_ord
                    output_dir = os.path.join(output_base_dir, ord2name(folder_ord))
                    if os.path.exists(output_dir): shutil.rmtree(output_dir)
                    os.makedirs(output_dir)

                file_ord = num_example // max_example_per_file % max_file_per_folder
                output_file = open(os.path.join(output_dir, 'book_{:02d}.json'.format(file_ord)), 'w')


    output_file.close()
