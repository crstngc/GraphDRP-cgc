#!/bin/bash --login

dev=$1
cdd=$2

# Runs training for 2 epochs and dums predictions and scores into ap_res
# python training.py --model 0 --train_batch 1024 --val_batch 1024 --test_batch 1024 --lr 0.0001 --num_epoch 2 --log_interval 20 --cuda_name "cuda:0" --set drug

# python training.py --model 0 --train_batch 1024 --val_batch 1024 --test_batch 1024 --lr 0.0001 --num_epoch 2 --log_interval 20 --cuda_name "cuda:0" --set drug

# ep=2
# root=data_processed/mix_drug_cell
# tr_file=train_data

# python -m pdb training.py --model 0 --train_batch 1024 --val_batch 1024 --test_batch 1024 --lr 0.0001 --num_epoch $ep --log_interval 20 --cuda_name "cuda:0" --tr_file $tr_file --vl_file val_data --te_file test_data --gout out --set mix --root $root

# python -m pdb graphdrp_baseline_pytorch.py --model 0 --cuda_name "cuda:6"

# test_candle.sh 0 candle_data_dir
# CUDA_VISIBLE_DEVICES=$1 CANDLE_DATA_DIR=$2 python -m pdb graphdrp_baseline_pytorch.py --modeling 0
CUDA_VISIBLE_DEVICES=$1 CANDLE_DATA_DIR=$2 python graphdrp_baseline_pytorch.py --modeling 0
