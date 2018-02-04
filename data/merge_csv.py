import sys
import csv
import os
import time
import datetime
from random import shuffle
from nltk.tokenize import word_tokenize

TRAINING_SIZE_PERCENTAGE = .8

NUM_ARTICLES = 1200

left_wing  = ['derfreitag/derfreitag.csv',
              'nachdenkseiten/nachdenkseiten.csv',
              'neues-deutschland/metadata_nd.csv',
              'jungle/jungle.csv']
right_wing = ['jungefreiheit/jungefreiheit.csv',
              'compact/compact.csv', 
              'zuerst/zuerst.csv',
              'pi-news/metadata_pi.csv']

def read_csv(csv_paths):
    rows = []
    for path in csv_paths:
        print('Reading:', path)
        rel = '/'.join(path.split('/')[:-1])
        print('Rel:', rel) 
        my_rows = []
        row_cnt = 0
        with open(path, 'r') as inf:
           reader = csv.reader(inf, delimiter=' ', quotechar='|')
           for row in reader:
                pth = rel + '/' + row[0]
                row[0] = '../' + pth
                try:
                    with open(pth) as f:
                        content = f.read()
                        tokens = word_tokenize(content)
                        my_rows.append((row, len(tokens)))
                except:
                    print('skipping file')
        my_rows.sort(key=lambda x: x[1])
        my_rows = [x[0] for x in my_rows[-NUM_ARTICLES:]]
        rows += my_rows
        print(len(my_rows), 'rows read\n')
    print('total rows:', len(rows))
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
