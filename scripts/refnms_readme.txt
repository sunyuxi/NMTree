1、按照data文件夹中README.md文件中说明，组织文件夹
2、去MattNet/tools文件夹，执行extract_mrcn_det_feats_refnms.py（一般不需要执行，因为已经被RefNMS+MAttNet执行过了）
该文件依赖../ref-nms/output/matt_dets_att_vanilla_refnms256_rsvg_0.json
用来生成pool5.mean.mean特征，该特征一般被RefNMS+MAttNet，RefNMS+CM-Erase-Reg生成了，所以一般不需要重复生成。如果需要手动生成，可以执行如下命令：

refnmsFeats=refnms256_res50_dota_v1_0_RoITransformer_det_feats.h5 #changed
detJson=../ref-nms/output/matt_dets_att_vanilla_refnms256_rsvg_0.json #changed
refnmsID=refnms256 #changed
dataset=rsvg

rm -f cache/feats/${dataset}/${refnmsFeats}
python tools/extract_mrcn_det_feats_refnms.py --imdb_name dota_v1_0 --net_name res50 --tag RoITransformer \
            --refnmsdet_jsonpath ${detJson} \
            --refnms_tid ${refnmsID}

3、执行scripts/run_test_dets_refnms.sh
该脚本首先执行MAttNet/tools/save_matt_det_feats_NMTree_refnms.py，
该脚本用来抽取基于MAttNet模型，生成的sub_feat, loc_feat = model.extract_sub_loc_feats(Feats, expanded_labels)
生成文件rsvg_matt_gt_feats.pth和rsvg_matt_det_feats.pth，这两个文件在训练和测试时，都需要

4、python misc/parser.py，生成data_dep.json和data_dep.pth，注意，该脚本只依赖REFER类，不依赖其他数据

5、sh scripts/run_train.sh训练模型
6、评测模型 sh scripts/run_test_dets.sh
该脚本额外依赖MAttNet/tools文件夹中run_detect.py生成的res50_dota_v1_0_RoITransformer_dets.json