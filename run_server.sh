set -x
CHECKPOINT_DIR=~/.llama/checkpoints/Llama3.2-1B-Instruct
PYTHONPATH=$(git rev-parse --show-toplevel) torchrun llama_models/scripts/example_chat_completion.py $CHECKPOINT_DIR
set +x