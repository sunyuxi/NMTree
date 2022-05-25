python tools/train.py \
    --id det_nmtree_01 \
    --dataset rsvg \
    --grounding_model NMTree \
    --data_file data_dep \
    --batch_size 128 \
    --glove glove.840B.300d_dep \
    --visual_feat_file rsvg_matt_gt_feats.pth