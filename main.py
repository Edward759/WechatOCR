import tools.infer.predict_system as predict_system
import tools.infer.utility as utility

info = {
    '收款人':'',
    '金额':'',
    '当前状态':'',
    '商品': '',
    '商户全称':'',
    '支付时间': '',
    '支付方式': '',
    '交易单号': '',
    '商户单号': ''
}
def ToExcel(listData):
    i = 0;
    while i < len(listData):
        if listData[i] == '当前状态':
            info['收款人'] = listData[i - 2]
            info['金额'] = listData[i - 1]
            for key in info:
                if key not in ['收款人', '金额']:
                    allKeys = info.keys()
                    j = i + 1
                    s = listData[j]
                    j += 1
                    finish = False;
                    while listData[j] not in allKeys:
                        if key == '商户单号':
                            finish = True
                            if '扫码' in s:
                                s = ''
                        s += listData[j]
                        j += 1
                        if '群收款' in listData[j]:
                            break
                    info[key] = s
                    i = j
                    if finish:
                        return
        else:
            i += 1


if __name__ == "__main__":
    result = predict_system.main(utility.parse_args('C:/Users/75926/Desktop/4.jpg'))
    ToExcel(result)
    print(info)