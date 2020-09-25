import os
import re
import sys
import argparse


def word_counter(file):
    # 检查文件是否存在，如果不存在，抛出文件不存在异常
    if not os.path.isfile(file):
        raise FileNotFoundError()

    """
    单词计数器字典
    # key: 单词
    # value: 该单词个数
    """
    counter_dic = dict() # {}

    # 打开文件
    with open(file) as f:
        for line in f:  # 从文件流中读取一行文本,赋值到变量line
            # 使用正则表达式替换文本中的字符，将\r, \n, ., " 替换为空格
            line = re.sub('\r|\n|\.|,|\"', ' ', line)
            # 将文本中连续的空格去除
            line = re.sub(' +', ' ', line)
            # 将替换好的文本的字符转换为小写
            line = line.lower()
            # 将文本按空格分割为单词
            words = line.split(" ")

            for word in words:  # 处理每一个词
                if len(word) == 0:
                    """
                    如果单词长度为0,跳过这个词不处理
                    会出现这样的原因是可能出现纯空格的行
                    """
                    continue
                if word in counter_dic.keys():  # 检查单词是否在字典中
                    # 在，该词对应的值加1
                    counter_dic[word] = counter_dic[word] + 1 # counter_dic.get(word)
                else:
                    # 不在，向字典添加这个词，并将对应的值赋值为1
                    counter_dic[word] = 1

    # 向调用函数返回单词计数器字典
    return counter_dic


# 程序参数
parser = argparse.ArgumentParser(description='本程序用于统计文本单词数量')
# 添加程序参数
parser.add_argument('folder', type=str, help='指定文件夹名', nargs='?')
parser.add_argument('-s', type=str, help='指定文件名')
# 匹配程序参数
args = parser.parse_args()

if __name__ == "__main__":
    if not args.folder is None:
        # 文件夹参数不为空，处理
        if not os.path.isdir(args.folder):
            # 文件不存在，抛出文件不存在异常
            print(f"文件夹 {args.folder} 不存在，请检查后重试。", file=sys.stderr)
            sys.exit(-1)

        # 文件夹存在，处理每一个文件
        # 列出文件夹的全部文件
        files = os.listdir(args.folder)
        # for file in files:
        for i, file in enumerate(files):
            try:
                counter = word_counter(os.path.join(args.folder, file))
                # 按counter字典的值对字典进行倒序排序，获取排序后的字典key
                keys = sorted(counter, key=counter.get, reverse=True)
                # 输出结果
                print(file)  # 打印文件名
                print(f"total {len(counter.keys())}\n")  # 打印总词数
                # 打印前20个词的信息
                for key in keys[:20]:
                    print(f"{key} {counter[key]}")
                # 如果不是最后一个文件，打印分割线
                if i < len(files) - 1:
                    print("------")
            except Exception:
                print(f"{file} fail, ignored.", file=sys.stderr)
    elif not args.s is None:
        # 检查文件是否存在
        if not os.path.isfile(args.s):
            print(f"文件 {args.s} is inexistence.", file=sys.stderr)
            #exit(-1)
        try:
            counter = word_counter(args.s)
            keys = sorted(counter, key=counter.get, reverse=True)
            print(f"total {len(counter.keys())}\n")  # 打印总词数
            # 打印前20个词的信息
            for key in keys[:20]:
                print(f"{key} {counter[key]}")
        except Exception:
            print(f"{args.s} fail.")
    else:
        text = input()

        counter_dic = dict()
        words = re.sub(' +', ' ', re.sub('\r|\n|\.|,|\"',
                                         ' ', text)).lower().split(" ")
        for word in words:  # 处理每一个词
            if len(word) == 0:
                """
                如果单词长度为0,跳过这个词不处理
                会出现这样的原因是可能出现纯空格的行
                """
                continue
            if word in counter_dic.keys():  # 检查单词是否在字典中
                # 在，该词对应的值加1
                counter_dic[word] = counter_dic[word] + 1
            else:
                # 不在，向字典添加这个词，并将对应的值赋值为1
                counter_dic[word] = 1

        counter = counter_dic
        keys = sorted(counter, key=counter.get, reverse=True)
        print(f"total {len(counter.keys())}\n")  # 打印总词数
        # 打印前20个词的信息
        for key in keys[:20]:
            print(f"{key} {counter[key]}")

    #exit(0)
