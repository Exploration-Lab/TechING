from dotenv import load_dotenv
load_dotenv()

import os
os.environ['HF_HOME']= os.getenv("HF_DIRECTORY")

import pandas as pd
import re
import tqdm
import evaluate
import argparse
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import json


# Function to extract mermaid code or return "No code found"
def extract_first_mermaid_code(text):
    patterns = [
        r"```mermaid(.*?)```",                      # Pattern 1: ```mermaid ... ```
        r"mermaid code as follows(.*)",             # Pattern 2: Mermaid code as follows ... (everything till the end)
        r"mermaid code for(.*)"                     # Pattern 3: Mermaid code for ... (everything till the end)
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()  # Return the first matched mermaid code
    
    return "No code found"  # Return "No code found" if no mermaid code is found

def get_scores(args, hf_dataset, file_path):
    if args.task == "image2code":
        print("Scoring image2code results...")
    elif args.task == "desc2code":
        print("Scoring desc2code results...")
    else:
        print("Scoring code2desc results...")

    os.environ["CUDA_VISIBLE_DEVICES"] = args.device
    device = torch.device(f"cuda" if torch.cuda.is_available() else "cpu")
    df_response = pd.read_json(file_path)

    if args.task == "image2code" or args.task == "desc2code":
        print("Extracting mermaid code from responses...")
        # Apply the function to the DataFrame
        df_response["cleaned_mermaid_code"] = df_response["Generated Code"].apply(extract_first_mermaid_code)
    else: # code2desc task
        df_response["Generated Description"] = df_response["Generated Description"]
    
    tokenizer = AutoTokenizer.from_pretrained("Elron/bleurt-base-512")
    bleurt_model = AutoModelForSequenceClassification.from_pretrained("Elron/bleurt-base-512").to(device)
    bleurt_model.eval()

    sacrebleu = evaluate.load('sacrebleu')
    bleu = evaluate.load('bleu')
    rouge = evaluate.load('rouge')
    meteor = evaluate.load('meteor')
    chrf = evaluate.load('chrf')

    # True labels
    if args.task == "image2code" or args.task == "desc2code":
        df_true = pd.DataFrame(hf_dataset["Mermaid Code"], columns=["Mermaid Code"])
    else:
        df_true = pd.DataFrame(hf_dataset["Description"], columns=["Description"])
    
    bleu_score_list = []
    sacrebleu_score_list = []
    meteor_score_list = []
    chrf_score_list = []
    bleurt_score_list = []
    rouge_score_list = []
    
    for i in tqdm.tqdm(range(0, len(df_response))):
        ground_truth = df_true.iloc[i, 0]
        generated_code = df_response.iloc[i, 0]
        if i == 0 or i == 1:
            print(ground_truth)
            print(generated_code)
        try:
            bleu_score = bleu.compute(predictions=[generated_code], references=[[ground_truth]])['bleu']
        except:
            print(i)
            bleu_score = 0
        sacrebleu_score = sacrebleu.compute(predictions=[generated_code], references=[[ground_truth]])['score']
        rouge_score = rouge.compute(predictions=[generated_code], references=[ground_truth])['rougeL']
        with torch.no_grad():
            bleurt_score = bleurt_model(**tokenizer([ground_truth], [generated_code], return_tensors='pt', max_length=512, truncation=True).to(device))[0].squeeze().cpu().item()
        meteor_score = meteor.compute(predictions=[generated_code], references=[ground_truth])['meteor']
        chrf_score = chrf.compute(predictions=[generated_code], references=[ground_truth])['score']
        

        sacrebleu_score_list.append(sacrebleu_score)
        bleu_score_list.append(bleu_score)
        rouge_score_list.append(rouge_score)
        bleurt_score_list.append(bleurt_score)
        meteor_score_list.append(meteor_score)
        chrf_score_list.append(chrf_score)

    df = pd.DataFrame()
    df['bleu'] = bleu_score_list
    df['sacrebleu'] = sacrebleu_score_list
    df['meteor'] = meteor_score_list
    df['chrf'] = chrf_score_list
    df['bleurt'] = bleurt_score_list
    df['rouge'] = rouge_score_list

    score_columns = ['bleu', 'sacrebleu', 'meteor', 'chrf', 'bleurt', 'rouge']  # List of score columns
    average_scores = df[score_columns].mean()
    mean_values = average_scores.tolist()
    print(mean_values[0], mean_values[1], mean_values[2], mean_values[3], mean_values[4], mean_values[5])
    return mean_values