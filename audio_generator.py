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

def save(input,filepath,filename):
    if os.access(f'{filepath}/{filename}.wav', os.F_OK):
        print("Given file path is exist.")
        return "audio exist"
     # 判断目录是否存在
    if not os.path.exists(filepath):
        # 如果目录不存在，则创建目录
        os.makedirs(filepath)

    executor(
        input=input,
        server_ip="127.0.0.1",
        port=8092,
        protocol="http",
        spk_id=0,
        output=f'{filepath}/{filename}.wav',
        play=False)
    return "success"

def save_latlng(filepath='laser-audio/latlng'):
    # integer place
    for i in range(0,180,1):
        save(num2cn(i),filepath,str(i))

    # 3 decimal place
    for i in range(1000):
        s = '点'+'{:03d}'.format(i)
        name = 'dian'+'{:03d}'.format(i)
        save(s,filepath,name)

def save_number(filepath='laser-audio/number'):
    #solider number in range 1-65535
    for i in range(1,65535):
        save(num2cn(i),filepath,i)

def save_regular(filepath='laser-audio/regular2'):
    save('结束训练',filepath,'jieshuxunlian')
    save('开始训练',filepath,'kaishixunlian')
    save('红队的',filepath,'hongduide')
    save('红队',filepath,'hongdui')
    save('蓝队的',filepath,'landuide')
    save('蓝队',filepath,'landui')
    save('的',filepath,'de')
    save('号的',filepath,'haode')
    save('号击中了',filepath,'haojizhongle')
    save('号上线',filepath,'haoshangxian')
    save('号移动至',filepath,'haoyidongzhi')
    save('坐标为',filepath,'zuobiaowei')

    save('友伤',filepath,'youshang')
    # hit part
    save('头部',filepath,'toubu')
    save('腹部',filepath,'fubu')
    save('背甲',filepath,'beijia')
    save('前甲',filepath,'qianjia')
    save('后甲',filepath,'houjia')
    save('右脚',filepath,'youjiao')
    save('右手',filepath,'youshou')
    save('左脚',filepath,'zuojiao')
    save('左手',filepath,'zuoshou')

save_regular()
save_latlng()
save_number()
