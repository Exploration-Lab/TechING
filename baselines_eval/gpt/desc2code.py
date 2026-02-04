from dotenv import load_dotenv
load_dotenv()

import os
os.environ['HF_HOME']= os.getenv("HF_DIRECTORY")

import base64
from openai import OpenAI
import openai
from tqdm import tqdm
import pandas as pd
from PIL import Image
from io import BytesIO

from utils.hf_dataset_download import load_teching_dataset
from utils.scoring import get_scores


def desc2code(args):
    load_dotenv()
    os.environ['HF_TOKEN']= os.getenv("HF_ACCESS_TOKEN")
    os.environ['OPENAI_API_KEY']= os.getenv("OPENAI_API_KEY")
    client = OpenAI()

    diag_type = args.diag_type
    hf_dataset = load_teching_dataset(
        dataset_name=args.dataset.upper(),
        diag_type=args.diag_type, 
        split="test"
        )
    prompt = """You are provided with the following summary of a {diag} diagram:

{summary}

Analyze the summary carefully and provide the Mermaid code for the corresponding diagram.
Do not provide steps for your analysis or any other information.
Just provide the Mermaid code in this format:

```mermaid

```
"""
    responses = []
    for i in tqdm(range(len(hf_dataset))):
        description = hf_dataset[i]["Description"]
        text = prompt.format(diag=args.diag_type, summary=description)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text,
                        }
                    ],
                }
            ],
        )

        responses.append(response.choices[0].message.content)
        # print(f"Response {i+1}: {response.choices[0].message.content}")
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