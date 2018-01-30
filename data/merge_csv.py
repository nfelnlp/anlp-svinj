import sys
import csv
import os
import time
import datetime
from random import shuffle

TRAINING_SIZE_PERCENTAGE = .8

left_wing  = ['derfreitag/derfreitag.csv',
              'nachdenkseiten/nachdenkseiten.csv',
              'neues-deutschland/metadata_nd.csv']
right_wing = ['jungefreiheit/jungefreiheit.csv',
              #'../compact/compact.csv', # Temporarily exclude since csv format needs to be fixed
              'zuerst/zuerst.csv']

def read_csv(csv_paths):
    rows = []
    for path in csv_paths:
        print('Reading:', path)
        rel = '/'.join(path.split('/')[:-1])
        print('Rel:', rel) 
        row_cnt = 0
        with open(path, 'r') as inf:
           reader = csv.reader(inf, delimiter=' ', quotechar='|')
           for row in reader:
                row[0] = '../' + rel + '/' + row[0]
                rows.append(row)
                row_cnt += 1
        print(row_cnt, 'rows read\n')
    return rows


def write_csv(rows, output_path):
    if os.path.isfile(output_path):
        os.remove(output_path)
    print('--> Writing to', output_path)
    with open(output_path, 'a+') as of:
        writer = csv.writer(of, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)
    print(len(rows), 'written\n')
     

if __name__ == "__main__":
    left_wing_rows = read_csv(left_wing)
    right_wing_rows = read_csv(right_wing)

    shuffle(left_wing_rows)
    shuffle(right_wing_rows)

    left_wing_training_split = int(len(left_wing_rows) * TRAINING_SIZE_PERCENTAGE)
    right_wing_training_split = int(len(right_wing_rows) * TRAINING_SIZE_PERCENTAGE)
    
    write_csv(left_wing_rows[:left_wing_training_split], 'train/left_wing_train.csv')
    write_csv(left_wing_rows[left_wing_training_split:], 'test/left_wing_test.csv')

    write_csv(right_wing_rows[:right_wing_training_split], 'train/right_wing_train.csv')
    write_csv(right_wing_rows[right_wing_training_split:], 'test/right_wing_test.csv')
