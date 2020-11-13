# -*- coding: utf-8 -*-
"""
Python File Template 
"""
import json
import os

__author__ = "Rui Meng"
__email__ = "rui.meng@pitt.edu"

if __name__ == '__main__':
    data_dir = '/home/ubuntu/efs/rum20/data/kp/kp/json/openkp/raw'
    output_data_dir = '/home/ubuntu/efs/rum20/data/kp/kp/json/openkp'

    for file_name in ['train.json', 'valid.json', 'test.json']:
        output_file = open(os.path.join(output_data_dir, file_name), 'w')

        for lid, l in enumerate(open(os.path.join(data_dir, file_name), 'r')):
            ex = json.loads(l)

            del(ex['VDOM'])

            ex['KeyPhrases'] = [' '.join(p) for p in ex['KeyPhrases']]
            ex['KeyPhrases'] = [p.strip().replace(' - ', '-') for p in ex['KeyPhrases'] if len(p.strip()) > 0]
            # if lid >= 10 and lid < 15:
            #     print(json.dumps(ex))

            output_file.write(json.dumps(ex)+'\n')

            # if lid > 15:
            #     break
