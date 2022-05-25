python tools/eval_det.py \
    --id det_nmtree_01 \
    --log_path log \
    --dataset rsvg \
    --iou_threshold 0.5 \
    --visual_feat_file rsvg_matt_det_feats.pth

python tools/eval_det.py \
    --id det_nmtree_01 \
    --log_path log \
    --dataset rsvg \
    --iou_threshold 0.25 \
    --visual_feat_file rsvg_matt_det_feats.pth