# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 20:25:42 2019

@author: Qian HongRui
"""

import os

def copyfunction(): 
    finger=""
    
    path = "E:/GLOVE/data_Q_1_2/one"
    
    data_path = "E://GLOVE//LSTM-Human-Activity-Recognition-master-11-13//data//Dataset_1_2_1//"
    
    
    fw_y_test = open(data_path + "test//y_test.txt", "a")
    fw_y_train = open(data_path + "train//y_train.txt", "a")

    test_data_number = 4
    type_num = 18  #the previous last line data's ID
                  # 0/30/40/49/61
    data_per_num = 20
    
    for i in range(0,42):
        finger=str(i)
        txt_path = path  + "/" + finger+".txt"
        number = len(open(txt_path,'rU').readlines())
        
        fw_train = open(data_path + "train//Inertial Signals//"+finger+".txt", "a")
        fw_test = open(data_path + "test//Inertial Signals//"+finger+".txt", "a")
        f = open(txt_path, "r")
        
        for j in range(number):
            result = f.readline().strip()
            
            
            if (j%data_per_num) >= test_data_number:
                fw_train.writelines(result+"\n")  
                
            else :
                fw_test.writelines(result+"\n")
                
            
        if i == 0:
            
            for j in range(number):
                if j%data_per_num == 0:
                    type_num+=1
                if (j%data_per_num) >= test_data_number:
                    fw_y_train.writelines(str(type_num)+"\n")
                else:
                    fw_y_test.writelines(str(type_num)+"\n")                
        f.close()
        fw_train.close()      
        fw_test.close()
        
        type_num = 0
    
    fw_y_test.close()
    fw_y_train.close()
    
copyfunction()