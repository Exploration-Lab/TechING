import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Training arguments")

    parser.add_argument("--model_path", type=str, default=None)
    parser.add_argument("--output_dir", type=str, default="checkpoints/")

    parser.add_argument("--seed", type=int, default=89)
    parser.add_argument("--lora_rank", type=int, default=32)
    parser.add_argument("--lora_alpha", type=int, default=16)
    parser.add_argument("--lora_dropout", type=float, default=0.2)
    parser.add_argument("--use_rslora", type=bool, default=True)

    parser.add_argument('--hf_token', type=str, required=False)
    
    args = parser.parse_args()
    return args