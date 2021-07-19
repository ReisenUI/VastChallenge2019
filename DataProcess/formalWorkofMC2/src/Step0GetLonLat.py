import json

data_file_path = r'../data'

pos = []

point_lr_min = 9999999999
point_ud_min = 9999999999
point_lr_max = -9999999999
point_ud_max = -9999999999

if __name__ == '__main__':
    with open(data_file_path + '/polygon.txt', 'r', encoding='utf-8') as f:
        for rows in f:
            # print(rows.replace("POLYGON", "").replace("((", "").replace("))", "").strip())
            temp_pos = rows.replace("POLYGON", "").replace("((", "").replace("))", "").strip()
            pos_arr = temp_pos.split(",")
            temp_arr = []
            for items in pos_arr:
                t_arr = []
                temp_items = items.strip().split(" ")
                t_arr.append(float(temp_items[0].strip()))
                t_arr.append(float(temp_items[1].strip()))
                temp_arr.append(t_arr)
            pos.append(temp_arr)
        f.close()

    with open(data_file_path + '/PolygonPoints.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(pos, indent=4))
        f.close()

    for arrays in pos:
        for items in arrays:
            if items[0] <= point_lr_min:
                point_lr_min = items[0]
            if items[0] > point_lr_max:
                point_lr_max = items[0]
            if items[1] <= point_ud_min:
                point_ud_min = items[1]
            if items[1] > point_ud_max:
                point_ud_max = items[1]
    print(point_lr_min, point_lr_max)
    print(point_ud_min, point_ud_max)
