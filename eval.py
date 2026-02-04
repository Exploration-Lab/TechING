import argparse

def main(args):
    if args.task == "image2code":
        if args.model_name == "llama":
            from baselines_eval.llama.image2code import image2code
            image2code(args)
        elif args.model_name == "gemma":
            from baselines_eval.gemma.image2code import image2code
            image2code(args)
        elif args.model_name == "gpt":
            from baselines_eval.gpt.image2code import image2code
            image2code(args)
        elif args.model_name == "minicpm":
            from baselines_eval.minicpm.image2code import image2code
            image2code(args)
        elif args.model_name == "qwen":
            from baselines_eval.qwen.image2code import image2code
            image2code(args)
        else:
            raise ValueError(f"Unknown model name: {args.model_name}")

    elif args.task == "desc2code":
        if args.model_name == "llama":
            from baselines_eval.llama.desc2code import desc2code
            desc2code(args)
        elif args.model_name == "gemma":
            from baselines_eval.gemma.desc2code import desc2code
            desc2code(args)
        elif args.model_name == "gpt":
            from baselines_eval.gpt.desc2code import desc2code
            desc2code(args)
        elif args.model_name == "minicpm":
            from baselines_eval.minicpm.desc2code import desc2code
            desc2code(args)
        elif args.model_name == "qwen":
            from baselines_eval.qwen.desc2code import desc2code
            desc2code(args)
        else:
            raise ValueError(f"Unknown model name: {args.model_name}")

    elif args.task == "image2desc":
        if args.model_name == "llama":
            from baselines_eval.llama.image2desc import image2desc
            image2desc(args)
        elif args.model_name == "gemma":
            from baselines_eval.gemma.image2desc import image2desc
            image2desc(args)
        elif args.model_name == "gpt":
            from baselines_eval.gpt.image2desc import image2desc
            image2desc(args)
        elif args.model_name == "minicpm":
            from baselines_eval.minicpm.image2desc import maimage2descin
            image2desc(args)
        elif args.model_name == "qwen":
            from baselines_eval.qwen.image2desc import image2desc
            image2desc(args)
        else:
            raise ValueError(f"Unknown model name: {args.model_name}")
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
