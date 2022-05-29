# -*- coding:utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import json
import argparse

import torch

this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(this_dir, '../'))

import models
from utils.det_loader import DetLoader
import utils.eval_utils as eval_utils


def parse_eval_opt():
    parser = argparse.ArgumentParser()

    # General Settings
    parser.add_argument('--id', type=str, required=True)
    parser.add_argument('--dataset', type=str, default='rsvg')
    parser.add_argument('--visual_feat_file', type=str, default='matt_res_det_feats.pth')
    parser.add_argument('--load_best', type=bool, default=True)
    parser.add_argument('--split', type=str, default='all', help="val/test/all")
    
    parser.add_argument('--iou_threshold', type=float, default=0.5, help='iou threshold')
    parser.add_argument('--det_jsonpath', type=str, default='../ref-nms/output/matt_dets_att_vanilla_refnms256_rsvg_0.json', help="generated by ../ref-nms/tools/save_matt_dets.py")

    parser.add_argument('--log_path', type=str, default='log')
    parser.add_argument('--dump_json', type=bool, default=True)

    args = parser.parse_args()
    return args


def show_acc(acc, n, split='test', iou_threshold=0.5, dataset='rsvg', f_handle=None):
    eval_accuracy = acc / n
    print("%s set evaluated. acc = %d / %d = %.2f%%" % (split, acc, n, eval_accuracy*100))
    if f_handle is not None:
        f_handle.write('[%s][%s], acc@{%.2f} is %.2f%%\n' % \
          (dataset, split, iou_threshold, eval_accuracy*100.0))

def split_eval(opt):
    # Set path
    infos_file = 'infos-best.json' if opt.load_best else 'infos-best.json'
    model_file = 'model-best.pth' if opt.load_best else 'model.pth'
    infos_path = os.path.join(opt.log_path, opt.dataset +'_'+opt.id, infos_file)
    model_path = os.path.join(opt.log_path, opt.dataset + '_' + opt.id, model_file)

    # Load infos
    with open(infos_path, 'rb') as f:
        infos = json.load(f)

    ignore = ['visual_feat_file']
    for k in infos['opt'].keys():
        if k not in ignore:
            if k in vars(opt):
                assert vars(opt)[k] == infos['opt'][k], k + ' option not consistent'
            else:
                vars(opt).update({k: infos['opt'][k]})  # copy over options from model

    # set up loader
    data_json = os.path.join(opt.feats_path, opt.dataset_split_by, opt.data_file + '.json')
    data_pth = os.path.join(opt.feats_path, opt.dataset_split_by, opt.data_file + '.pth')
    visual_feats_dir = os.path.join(opt.feats_path, opt.dataset_split_by, opt.visual_feat_file)
    dets_json = opt.det_jsonpath
    #dets_json = os.path.join('data/detections', opt.dataset_split_by, \
    #                            'matt_dets_att_vanilla_refnms_rsvg_0.json')

    if os.path.isfile(data_pth):
        loader = DetLoader(data_json, dets_json, visual_feats_dir, opt, data_pth)
        opt.tag_vocab_size = loader.tag_vocab_size
        opt.dep_vocab_size = loader.dep_vocab_size
    else:
        loader = DetLoader(data_json, dets_json, visual_feats_dir, opt)

    opt.word_vocab_size = loader.word_vocab_size
    opt.vis_dim = loader.vis_dim

    # Print out the option variables
    print("*" * 20)
    for k, v in opt.__dict__.items():
        print("%r: %r" % (k, v))
    print("*" * 20)

    # set up model and criterion
    model = models.setup(opt, loader).cuda()
    print(model_path)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # Evaluate all sets
    f = open(os.path.join(opt.log_path, opt.dataset +'_'+opt.id, 'refnms_det_results.txt'), 'a')

    acc = {}
    print("Start evaluating %s" % opt.dataset)
    if opt.split in ['all', 'val']:
        acc, n, _ = eval_utils.eval_det_split(loader, model, None, 'val', vars(opt), opt.dump_json)
        show_acc(acc, n, split='val', iou_threshold=opt.iou_threshold, dataset=opt.dataset, f_handle=f)

    if opt.split in ['all', 'test']:
        if opt.dataset in ['rsvg']:
            acc, n, _ = eval_utils.eval_det_split(loader, model, None, 'test', vars(opt), opt.dump_json)
            show_acc(acc, n, split='test', iou_threshold=opt.iou_threshold, dataset=opt.dataset, f_handle=f)          
        else:
            print('Not Implemented')
            assert False
    
    f.close()

    print("All sets evaluated.")

    return acc


if __name__ == '__main__':
    opt = parse_eval_opt()
    acc = split_eval(opt)