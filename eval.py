import argparse

def main(args):
    if args.task == "image2code":
        from baselines_eval.llama.image2code import image2code
        image2code(args)
    elif args.task == "desc2code":
        from baselines_eval.llama.desc_to_code import main as desc_to_code_main
        desc_to_code_main(args)
    elif args.task == "image2desc":
        from baselines_eval.llama.image_to_desc import main as image_to_desc_main
        image_to_desc_main(args)
    else:
        raise ValueError(f"Unknown task: {args.task}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=89)
    parser.add_argument("--diag_type", type=str, default="Block", help="Type of diagram to process")
    parser.add_argument("--model_name", type=str, required=True, help="name of the model, gemma, gpt, llama, minicpm, qwen ")
    parser.add_argument("--task", type=str, default="image2code", help="Task to perform, image2code, desc2code, image2desc")
    parser.add_argument("--dataset", type=str, default="d1", help="name of dataset, d1 or d3")
    parser.add_argument("--device", type=str, default="0", help="CUDA device to use")
    args = parser.parse_args()
    main(args)
