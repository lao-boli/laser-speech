from paddlespeech.server.bin.paddlespeech_client import TTSOnlineClientExecutor
import json
import os



executor = TTSOnlineClientExecutor()

def num2cn(num):
    units = ['', '十', '百', '千', '万', '十', '百', '千', '亿', '十', '百', '千', '万']
    digits = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    units_count = 0

    chinese_str = ''
    num_str = str(num)

    # 处理整数部分
    integer_part = int(abs(num))
    if integer_part == 0:
        chinese_str = digits[0]

    while integer_part > 0:
        digit = integer_part % 10
        if digit == 0:
            # 如果当前位是0，加上对应的单位
            if units_count % 4 == 0:  # 处理万、亿等单位
                chinese_str = units[units_count] + chinese_str
            elif chinese_str and chinese_str[0] != digits[0]:
                chinese_str = digits[0] + chinese_str
        else:
            chinese_str = digits[digit] + units[units_count] + chinese_str
        integer_part //= 10
        units_count += 1

    # 处理负号
    if num < 0:
        chinese_str = '负' + chinese_str

    # 处理小数部分
    decimal_part = abs(num) - int(abs(num))
    print(integer_part)
    if decimal_part > 0:
        chinese_str += '点'
        decimal_str = ''
        for digit in str(decimal_part)[2:]:
            decimal_str += digits[int(digit)]
        chinese_str += decimal_str

    return chinese_str

def save(input,filename):
    if os.access(f'./laser-audio/number2/{filename}.wav', os.F_OK):
        print("Given file path is exist.")
        return "audio exist"

    executor(
        input=input,
        server_ip="127.0.0.1",
        port=8092,
        protocol="http",
        spk_id=0,
        output=f'./laser-audio/number2/{filename}.wav',
        play=False)
    return "success"

#for i in range(0,180,1):
#    save(str(i),str(i))

#for i in range(1000):
#    s = '点'+'{:03d}'.format(i)
#    name = 'dian'+'{:03d}'.format(i)
#    save(s,name)

for i in range(12578,65535):
    save(num2cn(i),i)
