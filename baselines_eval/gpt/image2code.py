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

# Function to encode the image
def encode_hfimage(hf_image):
    if not isinstance(hf_image, Image.Image):
        hf_image = hf_image.convert("RGB")
    else:
        hf_image = hf_image.convert("RGB")
    buffer = BytesIO()
    hf_image.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def image2code(args):
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
    responses = []
    for i in tqdm(range(len(hf_dataset))):
        # Path to your image
        if args.dataset.upper() == "D1":
            hf_image = hf_dataset[i]["Image"]
        elif args.dataset.upper() == "D3":
            hf_image = hf_dataset[i]["Handdrawn_Diag"]
        
        # Getting the Base64 string
        base64_image = encode_hfimage(hf_image)

        text = f"""I am giving you a {diag_type} diagram in the form of an image. 
        Analyze the diagram carefully and provide the mermaid code for the diagram.
        Do not provide steps for your analysis or any other information.
        Just provide the mermaid code in this format:

        ```mermaid

        ```
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": text,
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
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
