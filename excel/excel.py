from pandas import DataFrame

def To_Excel(infoDict):
    df = DataFrame(data=infoDict)
    df.to_excel('test.xlsx', index=None)