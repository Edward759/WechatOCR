import tools.infer.predict_system as predict_system
import tools.infer.utility as utility
import excel.excel as excel
import os

info = {
    '收款人': [],
    '金额': [],
    '当前状态': [],
    '商品': [],
    '商户全称': [],
    '支付时间': [],
    '支付方式': [],
    '交易单号': [],
    '商户单号': []
}
def transfer(single_result):
    i = 0;
    while i < len(single_result):
        if single_result[i] == '当前状态':
            info['收款人'].append(single_result[i - 2])
            info['金额'].append(str(abs(float(single_result[i - 1]))))
            for key in info:
                if key not in ['收款人', '金额']:
                    allKeys = info.keys()
                    j = i + 1
                    s = single_result[j]
                    j += 1
                    finish = False;
                    while single_result[j] not in allKeys:
                        if key == '商户单号':
                            finish = True
                            if '扫码' in s:
                                s = ''
                        s += single_result[j]
                        j += 1
                        if '群收款' in single_result[j]:
                            break
                    info[key].append(s)
                    i = j
                    if finish:
                        return
        else:
            i += 1


if __name__ == "__main__":
    filelist = os.listdir('C:/Users/75926/Desktop/images/')
    for filename in filelist:
        result = predict_system.main(utility.parse_args('C:/Users/75926/Desktop/images/' + filename))
        transfer(result)
    excel.To_Excel(info)
    print(info)