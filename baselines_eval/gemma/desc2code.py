from dotenv import load_dotenv
load_dotenv()

import os
os.environ['HF_HOME']= os.getenv("HF_DIRECTORY")
import torch
import argparse
import pandas as pd
from tqdm import tqdm
from PIL import Image
from torch.utils.data import Dataset, DataLoader

from transformers import AutoProcessor, Gemma3ForConditionalGeneration
from accelerate import Accelerator
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


def desc2code(args):
    set_seed(args.seed)
    load_dotenv()
    os.environ['HF_TOKEN']= os.getenv("HF_ACCESS_TOKEN")
    os.environ["CUDA_VISIBLE_DEVICES"] = f"{args.device}"
    device = torch.device(f"cuda" if torch.cuda.is_available() else "cpu")

    # Load model & processor

    model_id = "google/gemma-3-12b-it"
    model = Gemma3ForConditionalGeneration.from_pretrained(
    model_id, device_map="auto"
    ).eval()

    processor = AutoProcessor.from_pretrained(model_id)

    prompt = """You are provided with the following summary of a {diag} diagram:

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
        text = prompt.format(diag=args.diag_type, summary=description)
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a helpful assistant."}]
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": text}]
            }
        ]

        inputs = processor.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=True,
            return_dict=True, return_tensors="pt"
            ).to(model.device, dtype=torch.bfloat16)

        input_len = inputs["input_ids"].shape[-1]

        with torch.inference_mode():
            generation = model.generate(**inputs, max_new_tokens=300, temperature=0.9)
            generation = generation[0][input_len:]

        decoded = processor.decode(generation, skip_special_tokens=True)
        # print(f"Generated Mermaid Code:\n{decoded}\n")
        responses.append(decoded)

    # Save results to JSON
    df = pd.DataFrame(responses, columns=["Generated Code"])
    os.makedirs(f"baselines_eval/{args.model_name}/results", exist_ok=True)
    output_path = os.path.join(f"baselines_eval/{args.model_name}/results", f"{args.diag_type}_{args.task}_Responses.json")
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