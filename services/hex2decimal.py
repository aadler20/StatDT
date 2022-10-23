def hex2decimal_1(hex_num):
    al = list(hex_num)
    # 定义ABCDEF分别为10，11，12，13，14，15
    b = {'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
    c = 0
    decimal_num = 0

    for i in range(len(hex_num)):
        # 如果al[i]的索引值不在b字典中
        if al[i] in b.keys():
            c = int(b[al[i]])
        # 如果al[i]的索引值不在b字典中，以原数值返回
        else:
            c = int(al[i])
        # 按照改10进制公式计算
        decimal_num += c*16**(len(hex_num)-i-1)
    return decimal_num


hex_num = input('16进制:')
print('十六进制的{}化成十进制为{}.'.format(hex_num,hex2decimal_1(hex_num)))


def hex2decimal_2(hex_num):
    dic = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
    n = len(hex_num)
    decimal_num = 0
    for i in range(n):
        decimal_num +=dic[hex_num[i]]*(16**(n-i-1))
    return decimal_num

hex_num =input('请输入一个十六进制整数:').upper()
print('十六进制的{}化成十进制为{}.'.format(hex_num,hex2decimal_2(hex_num)))


def hex2decimal_3(hex_num):
    n = len(hex_num)
    decimal_num = 0
    for i in range(n):
        if hex_num[i] >= '0' and hex_num[i] <= '9':
            temp = int(hex_num[i])
        elif hex_num[i] >= 'A' and hex_num[i] <= 'F':
            temp = ord(hex_num[i]) - 55
        elif hex_num[i] >= 'a' and hex_num[i] <= 'f':
            temp = ord(hex_num[i]) - 87
        else:
            print('错误: 您的输入中有非十六进制数:' + hex_num[i])
            return hex_num
        decimal_num = decimal_num + temp * (16 ** (n - i - 1))
    return decimal_num

hex_num =input('请输入一个十六进制整数:')
print('十六进制的{}化成十进制为{}.'.format(hex_num,hex2decimal_3(hex_num)))