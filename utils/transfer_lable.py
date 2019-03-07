#coding:utf-8
"""
将图片的labels文件翻译对照字典，翻译成对应的训练数据格式
"""

import re

def get_dict(char_file='../train/char_std_25_date.txt',debug=False):
    """
    将文本文件翻译成字典
    :param char_file:
    :return:
    """
    char_set = open('../train/char_std_25_date.txt', 'r', encoding='utf-8').readlines()
    print('char_set总大小包含了空格：:', len(char_set), char_set)
    char_set = [ch.strip('\n') if ch.strip('\n')!='' else ' ' for ch in char_set][0:]
    char_idx_dic = {}  # 最终的字典，内容对应序号
    idx_char_dic = {}  # 最终的字典，需要对应内容
    for idx, c in enumerate(char_set):
        char_idx_dic[c] = idx
        idx_char_dic[idx] = c
    if debug:
        print('char_idx_dic:', char_idx_dic)
        print('idx_char_dic:', idx_char_dic)
    return char_idx_dic, idx_char_dic

def containenglish(str0):
    return re.search('[a-zA-Z]', str0)

def transfer_labels(label_file, result_label_file='result_lables.txt'):
    """
    转换label文件，将真实的数据转换成对应的idx
    :param label_file:需要转换的标注文件
    :param result_label_file: 转换后的标注文件
    :return:
    """
    char_idx_dic, idx_char_dic = get_dict(debug=True)
    result_writer = open(result_label_file, 'w')
    labels_lines = open(label_file, 'r', encoding='utf-8').readlines()
    for labels_line in labels_lines:
        labels_arr = labels_line.split(" ")
        wate_transfer = [x.strip('\n') for x in labels_arr[1:]]
        wate_transfer = " ".join(wate_transfer)
        transfered_arr = []
        if not containenglish(wate_transfer):  # 不包含英文，逐个翻译
            transfered_arr = [str(char_idx_dic[ch]) for ch in wate_transfer]
        else:  # 包含英文，逐个翻译
            wate_transfer = wate_transfer.upper()
            pattern = re.compile(r'[a-zA-Z]+')  # 查找所有的英文
            en_res = pattern.findall(wate_transfer)
            if len(en_res) == 1 : # 只包含一段英文
                tmp_char_idx = char_idx_dic[en_res[0]]
                tmp_arr = wate_transfer.split(en_res[0])
                transfered_arr = [str(char_idx_dic[ch]) for ch in tmp_arr[0]]
                transfered_arr += [str(tmp_char_idx)]
                transfered_arr += [str(char_idx_dic[ch]) for ch in tmp_arr[1]]
            else:
                print('~~~~~~~~~~~~~有多个英文的数据',labels_arr)


        result_arr = [labels_arr[0]]+ transfered_arr
        result_writer.write( " ".join(result_arr))
        result_writer.write("\n")
    result_writer.close()


if __name__ == '__main__':
    # # print(containenglish('1312z31'))
    # a = "12312123"
    # if not containenglish(a):
    #    print(1)
    # pattern = re.compile(r'[a-zA-Z]+')  # 查找数字
    # result1 = pattern.findall('17 FEBd 2018')
    # print(result1)
    #
    # print(re.search(result1[0], '17 FEBd 2018').span())
    transfer_labels('label_file.txt')
