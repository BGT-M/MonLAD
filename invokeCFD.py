import sys
sys.path.append("../")

import os
import numpy as np
import pandas as pd
from MonLAD import ZeroOutCoreCFD
from MonLAD.util import call_pareto, cal_f1
import argparse
from tqdm import tqdm
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('--delta', '-d', default=10000)
parser.add_argument('--output_count', '-oc', default='False')
parser.add_argument('--epsilon', '-e', default=10000)
parser.add_argument('--inputData', '-i', default='./data/') # './CFDRes/trans.csv'
parser.add_argument('--outpath', '-o', default='./CFDRes/')
args = parser.parse_args()


delta = int(args.delta)
if args.output_count == 'True':
    output_count = True
else:
    output_count = False
epsilon = int(args.epsilon)
inputData = args.inputData
outpath = args.outpath

print('delta:', delta)
print('output_count:', output_count)
print('epsilon:', epsilon)
print('inputData:', inputData)
print('outpath:', outpath)

def main():
    dataAddr = inputData
    outfile = outpath
    deltaUp = deltaDown = delta
    smd = ZeroOutCoreCFD(deltaUp, deltaDown, epsilon)
    dataFile = 'exp_data.csv'
    print(dataFile)

    pass_header = True
    with open(os.path.join(dataAddr, dataFile), 'r') as f1:
        total = len(f1.readlines())
    with open(os.path.join(dataAddr, dataFile), 'r') as f2:
        t1 = time()
        for _ in tqdm(range(total), unit_scale=True):
            data = f2.readline().split(',')
            if pass_header:
                pass_header = False
                continue

            acc_id = int(data[0])
            transaction_type = data[2]
            weight = int(float(data[3]))
            acc_count, acc_countIn = smd(acc_id, transaction_type, weight)
            if acc_count == -1:
                continue
        t2 = time()
        print('duration:', round(t2 - t1, 4))

    count_df = pd.DataFrame()
    acc_id_series = np.array(list(smd.countDict.keys()))
    count_df['acc_id'] = acc_id_series
    count_df['count'] = np.array(list(smd.countDict.values()))
    count_df['countIn'] = np.array(list(smd.countInDict.values()))

    if not os.path.exists(outfile):
        os.makedirs(outfile)

    if output_count:
        count_fileName = os.path.join(outfile, 'CFD_count' + str(delta // 1000) + 'k.csv')
        print('Output count.csv to: ', count_fileName)
        count_df.to_csv(count_fileName, index=False)

    # evaluation
    count_df['IMinusC'] = count_df['countIn'] - count_df['count']
    count_df = count_df[count_df['count'] > 0]
    anomalous_acc, higher_q_B, higher_q_F, tail_B, tail_F = call_pareto(count_df, alpha_c=0.5, p_c=0.8, alpha_i=0.5, p_i=0.8, k=1, outpath=outpath,
                                output=False,
                                detect_part=[1, 2, 3, 4])  # 1: part1; 2: part3; 3: part2-1; 4:part2-2

    if outpath:
        np.save(os.path.join(outpath, 'res.npy'), anomalous_acc)

if __name__ == '__main__':
    main()