#!/bin/sh

export CUDA_VISIBLE_DEVICES=0

./venv/bin/python analyzetext.py --taskbridgeurl http://127.0.0.1:42000/ --worker SENECA-GPU0 --model llama3.2
