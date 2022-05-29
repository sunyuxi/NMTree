1、按照data文件夹中README.md文件中说明，组织文件夹
2、去MattNet/tools文件夹，执行
prepro.py
extract_mrcn_ann_feats.py，该文件需要事先抽取所有gt bbox的特征，并存放到指定文件夹
run_detect.py和extract_mrcn_det_feats.py，run_detect.py依赖det_instances_rsvg.json文件，并生成pool5.mean.mean特征


3、去MAttNet/tools执行python save_matt_gt_feats_NMTree.py和save_matt_det_feats_NMTree.py
这两个脚本是用来抽取基于MAttNet模型，生成的sub_feat, loc_feat = model.extract_sub_loc_feats(Feats, expanded_labels)
生成文件rsvg_matt_gt_feats.pth和rsvg_matt_det_feats.pth，这两个文件在训练和测试时，都需要

4、python misc/parser.py，生成data_dep.json和data_dep.pth，注意，该脚本只依赖REFER类，不依赖其他数据

5、sh scripts/run_train.sh训练模型
6、评测模型 sh scripts/run_test_dets.sh
该脚本额外依赖MAttNet/tools文件夹中run_detect.py生成的res50_dota_v1_0_RoITransformer_dets.json