dataset=rsvg
refnms_tid=refnms256

cd ../MAttNet

MAttNetID=mrcn_cmr_with_st
MAttNetFeats_output_dir=../NMTree/data/feats
refnmsdet_jsonpath=../ref-nms/output/matt_dets_att_vanilla_${refnms_tid}_rsvg_0.json
refnmsdet_dirpath=hbb_obb_features_refnms_det_selected256
refnmsdet_feats_suffix=hbb_det_res50_dota_v1_0_RoITransformer.hdf5
#note current directory is MAttNet
refnmsdet_MAttNet_feats_filepath=cache/feats/rsvg/${refnms_tid}_res50_dota_v1_0_RoITransformer_det_feats.h5

python tools/save_matt_det_feats_NMTree_refnms.py --dataset ${dataset} --id ${MAttNetID} --output_dir ${MAttNetFeats_output_dir} \
            --refnmsdet_jsonpath ${refnmsdet_jsonpath} --refnmsdet_dirpath ${refnmsdet_dirpath} \
            --refnmsdet_feats_suffix ${refnmsdet_feats_suffix} --refnmsdet_MAttNet_feats_filepath ${refnmsdet_MAttNet_feats_filepath} \
            --refnms_tid ${refnms_tid}
#output:NMTree/data/feats/rsvg/rsvg_matt_det_feats_refnms256.pth
cd ../NMTree

python tools/eval_det_refnms.py \
    --id det_nmtree_01 \
    --log_path log \
    --dataset rsvg \
    --iou_threshold 0.5 \
    --visual_feat_file rsvg_matt_det_feats_${refnms_tid}.pth \
    --det_jsonpath ../ref-nms/output/matt_dets_att_vanilla_${refnms_tid}_rsvg_0.json

python tools/eval_det_refnms.py \
    --id det_nmtree_01 \
    --log_path log \
    --dataset rsvg \
    --iou_threshold 0.25 \
    --visual_feat_file rsvg_matt_det_feats_${refnms_tid}.pth \
    --det_jsonpath ../ref-nms/output/matt_dets_att_vanilla_${refnms_tid}_rsvg_0.json