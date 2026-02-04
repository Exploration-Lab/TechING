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

from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
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

# Assuming processor and model are already loaded before running this script
# from transformers import YourModel, YourProcessor

class DiagramDataset(Dataset):
    def __init__(self, hf_dataset):
        self.dataset = hf_dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        row = self.dataset[idx]
        desc = row["Description"]
        # mermaid_code = row["Mermaid Code"]
        return desc

def collate_fn(args, batch, processor, prompt_template):
    descriptions = batch

    messages = [
        {"role": "user", "content": prompt_template.format(summary=s, diag=args.diag_type)}
        for s in descriptions
    ]
    # Prepare inputs
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text], images=image_inputs, videos=video_inputs, padding=True, return_tensors="pt"
        )
    
    return inputs

def desc2code(args):
    
    load_dotenv()
    os.environ['HF_TOKEN']= os.getenv("HF_ACCESS_TOKEN")
    os.environ["CUDA_VISIBLE_DEVICES"] = f"{args.device}"
    device = torch.device(f"cuda" if torch.cuda.is_available() else "cpu")

    # Load model & processor
    processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct", device_map="auto")
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct", torch_dtype="auto", device_map="auto")
    model.eval()
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
    dataset = DiagramDataset(hf_dataset)

    def dynamic_collate(batch):
        inputs = collate_fn(args, batch, processor, prompt)
        return inputs.to(device)

    dataloader = DataLoader(
        dataset,
        batch_size=1,
        shuffle=False,
        collate_fn=dynamic_collate
    )

    responses = []
    with torch.no_grad():
        set_seed(args.seed)
        for inputs in tqdm(dataloader):
            generated_ids = model.generate(**inputs, max_new_tokens=300,
                                           temperature=0.9)
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            response = processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )
            responses.append(response[0])
            # print(f"Generated Mermaid Code:\n{response[0]}\n")
    # Save results to JSON
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