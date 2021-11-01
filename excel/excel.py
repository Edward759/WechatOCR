from pandas import DataFrame

def To_Excel(info_dict, dist_path):
    df = DataFrame(data=info_dict)
    df.to_excel(dist_path + '/result.xlsx', index=None)