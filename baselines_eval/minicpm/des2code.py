import os
from dotenv import load_dotenv
load_dotenv()

import os
import torch
import argparse
import pandas as pd
from tqdm import tqdm
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from huggingface_hub import login
from transformers import AutoTokenizer, AutoModel
import random
from transformers import set_seed as hf_set_seed
import numpy as np
from utils.hf_dataset_download import load_teching_dataset
from utils.scoring import get_scores

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # if using multi-GPU

    # Make CUDA and cuDNN deterministic
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    hf_set_seed(seed)

def image2code(args):
    set_seed(args.seed)
    load_dotenv()
    os.environ['HF_TOKEN']= os.getenv("HF_ACCESS_TOKEN")
    #os.environ["CUDA_VISIBLE_DEVICES"] = f"{args.device}"
    device = torch.device(f"cuda" if torch.cuda.is_available() else "cpu")

    # Load model & processor

    model = AutoModel.from_pretrained(
        "openbmb/MiniCPM-V-2_6",
        trust_remote_code=True,
        attn_implementation='sdpa',
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained("openbmb/MiniCPM-V-2_6", trust_remote_code=True)
    
    model.eval()

    prompt = f"""You are provided with the following summary of a {diag} diagram:

{summary}

Analyze the summary carefully and provide the Mermaid code for the corresponding diagram.
Do not provide steps for your analysis or any other information.
Just provide the Mermaid code in this format:

```mermaid

```
"""
    hf_dataset = load_teching_dataset(
        dataset_name=args.dataset.upper(),
        diag_type=args.diag_type, 
        split="test"
        )
    
    responses = []
    for idx in tqdm(range(len(hf_dataset))):
        description = hf_dataset[idx]["Description"]
        prompt = prompt_template.format(summary=description ,diag=diag_type)
        messages = [{'role': 'user', 'content': [ prompt]}]

        response = model.chat(
                    image=None,  # Image is passed within msgs
                    msgs=messages,
                    tokenizer=tokenizer,
                    max_new_tokens=args.max_tokens,  
                    temperature=0.9
                )
        responses.append(response)       

    # 🔹 Save JSON after every iteration
    df = pd.DataFrame(responses, columns=["Generated Code"])
    os.makedirs(f"baselines_eval/{args.model_name}/results", exist_ok=True)
    output_path = os.path.join(f"baselines_eval/{args.model_name}/results", f"{args.dataset.upper()}_{args.diag_type}_{args.task}_Responses.json")
    df.to_json(output_path, orient='records', lines=False, indent=4)
    print(f"Saved results to {output_path}")

    # Score the results
    scores = get_scores(args, hf_dataset, output_path)
    print("Evaluation Scores:")
    print(f"BLEU: {scores[0]}")
    print(f"SacreBLEU: {scores[1]}")
    print(f"METEOR: {scores[2]}")
    print(f"CHR-F: {scores[3]}")
    print(f"BLEURT: {scores[4]}")
    print(f"ROUGE-L: {scores[5]}")




