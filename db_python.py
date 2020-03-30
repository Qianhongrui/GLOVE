# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 23:08:59 2019

@author: Qian HongRui
"""


# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import MySQLdb
import time

i=0
def num_to_string(num):
    numbers = {
        1 : "加",
        2 : "账单",
        3 : "少",
        4 : "咖啡",
        5 : "杯",
        6 : "饮料",
        7 : "吃",
        8 : "给",
        9 : "好",
        10 : "绿茶",
        11 : "半",
        12 : "热",
        13 : "多少",
        14 : "冰",
        15 : "我",
        16 : "菜单",
        17 : "钱",
        18 : "不",
        19 : "一",
        20 : "吸管",
        21 : "糖",
        22 : "end",
        23 : "谢谢",
        24 : "想",
        25 : "厕所",
        26 : "服务生",
        27 : "要",
        28 : "哪里",
        29 : "你",
        30 : "start",
        31 : "零",
        32 : "二",
        33 : "三",
        34 : "四",
        35 : "五",
        36 : "六",
        37 : "七",
        38 : "八",
        39 : "九",
        40 : "十",
        41 : "二十",
        42 : "三十",
        43 : "四十",
        44 : "五十",
        45 : "六十",
        46 : "七十",
        47 : "八十",
        48 : "九十",
        49 : "一百",
        50 : "酒",
        51 : "葡萄酒",
        52 : "自来水",
        53 : "牛奶",
        54 : "热巧克力",
        55 : "果汁",
        56 : "啤酒",
        57 : "可口可乐",
        58 : "白茶",
        59 : "矿泉水",
        60 : "红酒",
        61 : "红茶",
        62 : "总共",
        63 : "纸巾",
        64 : "这个",
        65 : "早餐",
        66 : "再见",
        67 : "有",
        68 : "小费",
        69 : "喜欢",
        70 : "午餐",
        71 : "位",
        72 : "晚餐",
        73 : "推荐",
        74 : "汤匙",
        75 : "什么",
        76 : "人",
        77 : "请",
        78 : "拿",
        79 : "没有",
        80 : "看",
        81 : "或",
        82 : "欢迎",
        83 : "和",
        84 : "喝",
        85 : "对不起",
        86 : "餐具",
        87 : "玻璃",
        88 : "帮助",
        89 : "一点钟",
        90 : "两点钟",
        91 : "三点钟",
        92 : "四点钟",
        93 : "五点钟",
        94 : "六点钟",
        95 : "七点钟",
        96 : "八点钟",
        97 : "九点钟",
        98 : "十点钟",
        99 : "十一点钟",
        100 : "十二点钟",
        101 : "预约"
    }
    #print(num)
    return numbers.get(num, None)


with tf.Session() as sess:
    new_saver = tf.train.import_meta_graph('E:\\GLOVE\\LSTM-Human-Activity-Recognition-master-11-13\\log_1_2_3\\123model.ckpt.meta')
    new_saver.restore(sess,'E:\\GLOVE\\LSTM-Human-Activity-Recognition-master-11-13\\log_1_2_3\\123model.ckpt')
    y = tf.get_collection('pred_network')
    
    y=tf.arg_max(y,2)+1
    #print (y)
    graph = tf.get_default_graph()
    input_x = graph.get_operation_by_name('input_x').outputs[0]
    keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]
    while i<100:
        db= MySQLdb.connect("127.0.0.1","root", "000000","glove",charset='utf8')
        cursor = db.cursor()
        cursor.execute("select id,data from glove_data")
        results = cursor.fetchall()
        #print(results)
        #if results is None:
           # time.sleep(0.5)
           # continue
        for record in results:
            result_id = record[0]
            result_data = record[1]
            #print (result_data)
            
            
            if (result_data != ''):
                X_ = np.array(
                    [elem for elem in [
                            cloumn.split(' ') for cloumn in result_data.split(',')
                    ]], dtype=np.float32
                )
                #print(X_)
                #X_ = X_.astype(np.float)
                X_ = np.transpose(np.array(X_.reshape(42,1,128)), (1, 2, 0))

                predict_result = sess.run(y, feed_dict={input_x:X_,  keep_prob:1.0})[0]
                #print (predict_result[0])
                
                insert="INSERT INTO return_data(data) VALUES (%s);"
                return_value = num_to_string(predict_result[0])
                print(return_value)
                cursor.execute(insert,(return_value,))
                db.commit()
                
            delete="DELETE FROM glove_data WHERE glove_data.id = %s"
            data = result_id
            cursor.execute(delete,(data,))
            db.commit()
        time.sleep(1)    
    