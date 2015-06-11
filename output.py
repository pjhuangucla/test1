# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 10:28:20 2015

@author: PengJun
"""

import os
import re
import json
import numpy as np
import pandas as pd
import argparse
from sklearn.externals import joblib
import shutil
import os.path


import Train_placementagg
import Train_preprocess
import Train_model_revised
import Test_placementagg
import Test_preprocess
import Test_output
#model_dir = 'C:/Users/PengJun/Documents/Rule14/BACLatest/IOProcess/Models/'
#train_dir = 'C:/Users/PengJun/Documents/Rule14/BACLatest/IOProcess/Training/'
#test_dir = 'C:/Users/PengJun/Documents/Rule14/BACLatest/IOProcess/Testing/'


def Output(directory):
    #Train if needed
    model_dir = os.path.join(directory, 'Models/Models.pkl')
    fail = 0
    try:
        joblib.load(model_dir)
    except:
        print 'Exception in model loading'
        merged_placement = Train_placementagg.train_placementagg(directory)
        BACsub = Train_preprocess.Train_preprocess(merged_placement, directory)
        Train_model_revised.Train_model(BACsub, directory)
        #model = joblib.load(model_dir)
        fail = 1

    try:
        test_merged_placement = Test_placementagg.Test_placementagg(directory)
        print 'Placement merged'
        try:
            testsample = Test_preprocess.Test_preprocess(test_merged_placement, directory)
            print 'Testdata preprocess finished'
            try:
                output = Test_output.Test_output(testsample, directory)
                output.to_csv(os.path.join(directory, 'Result/test.csv'), index = False)
                print 'Test result is ready in the Result folder'
            except: 
                print 'Test process failed'
                fail = 1
        except:
            print 'Testdata preprocess failed'
            fail = 1
    except:
        print 'Placement merged failed'
        fail = 1

    scr = os.path.join(directory, 'Testing/Input')
    dst1 = os.path.join(directory, 'Testing/Processed')
    dst2 = os.path.join(directory, 'Testing/Unprocessed')
    for f in os.listdir(scr):
        scr_file = os.path.join(scr, f)
        if not (fail):
            dst_file= os.path.join(dst1, f)
        else:
            dst_file= os.path.join(dst2, f)
        shutil.move(scr_file, dst_file)


#directory = os.path.abspath(os.getcwd())
#merged_placement = Train_placementagg.train_placementagg(directory)
#BACsub = Train_preprocess.Train_preprocess(merged_placement, directory)
#Train_model_revised.Train_model(BACsub, directory)

#test_merged_placement = Test_placementagg.Test_placementagg(directory)
#testsample = Test_preprocess.Test_preprocess(test_merged_placement, directory)
#output = Test_output.Test_output(testsample, directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='. Intelligent Collections script.')
    parser.add_argument('directory',
                        metavar='project_dir',
                        help='directory of the project')
#    parser.add_argument('trainpath',
#                       metavar='train_dir',
#                        help='directory of train files')
#    parser.add_argument('modelpath',
#                       metavar='model_dir',
#                        help='directory of model files')  
    args = parser.parse_args()
    Output(directory = args.directory)
                        
                        
                        
                        
        
    
        
        
        
