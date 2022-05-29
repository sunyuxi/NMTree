# -*- coding:utf8 -*-

import json

def tj_det_ids():
    filepath = 'data/detections/rsvg/matt_dets_att_vanilla_refnms_rsvg_0.json'

    with open(filepath, 'r') as f:
        json_data = json.load(f)
        detid_list=list()
        for one_item in json_data:
            if one_item['image_id'] == 3272:
                detid_list += [one_item['det_id']]
        print(len(detid_list))
        print(sorted(set(detid_list)))
        [19790, 19791, 19792, 19793, 19794, 19795, 19796, 19797, 19798, 19799, 19800, 19801, 19802, 19803, 19804, 19805, 19806, 19807, 19808, 19809, 19810, 19811, 19812, 19813, 19814, 19815, 19816]
        print('[1285, 1286, 1287, 1288, 1289, 1290, 1291, 1292, 1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307, 1308, 1309, 1310, 1311, 1312, 1313]')

tj_det_ids()