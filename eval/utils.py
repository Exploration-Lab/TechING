import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluation arguments")

    parser.add_argument("--hf_token", type=str)
    parser.add_argument("--do_train", action="store_true")
    parser.add_argument("--do_eval", action="store_true")
    parser.add_argument("--per_device_train_batch_size", type=int, default=1)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=1)
    parser.add_argument("--learning_rate", type=float, default=2e-5)
    parser.add_argument("--weight_decay", type=float, default=0.05)
    parser.add_argument("--num_train_epochs", type=float, default=1)
    parser.add_argument("--lr_scheduler_type", type=str, default="cosine", choices=["linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup"])
    parser.add_argument("--warmup_ratio", type=float, default=0.2)
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument("--save_strategy", type=str, default="steps", choices=["no", "epoch", "steps"])
    parser.add_argument("--save_steps", type=int, default=1000)
    parser.add_argument("--logging_steps", type=int, default=10)
    parser.add_argument("--dataloader_num_workers", type=int, default=8)
    parser.add_argument("--report_to", type=str, default="none", choices=['wandb', 'none'])
    parser.add_argument("--run_name", type=str, default='training')
    parser.add_argument("--seed", type=int, default=89)
    parser.add_argument("--lora_rank", type=int, default=32)
    parser.add_argument("--lora_alpha", type=int, default=16)
    parser.add_argument("--lora_dropout", type=float, default=0.2)
    parser.add_argument("--use_rslora", type=bool, default=True)
    parser.add_argument("--ddp_backend", type=str, default="nccl", choices=["nccl", "c10d"])
    
    args = parser.parse_args()
    return args