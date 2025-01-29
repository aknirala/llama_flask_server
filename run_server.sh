set -x
CHECKPOINT_DIR=~/.llama/checkpoints/Llama3.2-1B-Instruct
torchrun multimedia_server.py $CHECKPOINT_DIR
set +x
