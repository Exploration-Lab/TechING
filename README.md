# TechING (Technical Image Understanding)

<img src="images/TechING_overview.png">

**Picture**: Overview of TechING

This repository contains the official implementation of the following paper:  
***TechING: Towards Real World Technical Image Understanding via VLMs***

**Authors:** *Tafazzul Nadeem\*, Bhavik Shangari\*, Manish Rai, Gagan Raj Gupta, Ashutosh Modi*

**Abstract:** *Professionals working in technical domain typically hand-draw 
(on whiteboard, paper, etc.) technical diagrams (e.g., flowcharts, block diagrams, 
etc.) during discussions; however, if they want to edit these later, it needs to 
be drawn from scratch. Modern day VLMs have made tremendous progress in image 
understanding but they struggle when it comes to understanding technical diagrams. 
One way to overcome this problem is to fine-tune on real world hand-drawn images, 
but it is not practically possible to generate large number of such images. 
In this paper, we introduce a large synthetically generated corpus (reflective 
of real world images) for training VLMs and subsequently evaluate VLMs on a 
smaller corpus of hand-drawn images (with the help of humans). We introduce 
several new self-supervision tasks for training and perform extensive experiments 
with various baseline models and fine-tune Llama 3.2 11B-instruct model on 
synthetic images on these tasks to obtain LLama-VL-TUG, which significantly 
improves the ROUGE-L performance of Llama 3.2 11B-instruct by 2.14x and achieves 
the best all-round performance across all baseline models. On real-world images, 
human evaluation reveals that we achieve minimum compilation errors across all 
baselines in 7 out of 8 diagram types and improve the average F1 score of Llama 
3.2 11B-instruct by 6.97x.*

\*Equal Contribution

## Training Methodology
We fine-tuned Llama3.2-11B-Vision-Instruct using LoRA (image encoder as well as
text decoder) on the combination of Primary and Self Supervision tasks (described below)
using D1 and D2 corpus of [TechING](https://huggingface.co/datasets/Exploration-Lab/TechING) dataset.

**Primary Tasks**
1. **Image2Code**: Generating corresponding [Mermaid](https://mermaid.js.org/) code for a given image.
2. **Description2Code**: Converting natural language descriptions into Mermaid code.
3. **Image2Description**: Generating Descriptions from technical diagram images.
4. **Image Enhancement via Prompt**: Generating Mermaid code of the updated image, given
   an image and a natural language enhancement prompt.

**Self Supervision Tasks**
1. **Image Enhancement via Description**: Given an image along with a textual
   description of the target image, produce code that reflects the enhanced description.
2. **Code Enhancement via Prompt**: Given a Mermaid code along with an enhancement
   prompt, update the code accordingly.
3. **Code Enhancement via Description**: Given a Mermaid code snippet along with a natural
  language description of the target image, enhance the code to accurately reflect
  the changes present in the description.
4. **Positive/Negative Image–Code Pair Q&A**: Predict given image–code pair
   constitutes a valid match or a mismatch.
5. **Partial Match Image–Code Pair Q&A**: Identify partial matches between incomplete
   and complete image-code pairs.
## How to run experiments

### 1. Training (train/train.py):
To train [meta-llama/Llama-3.2-11B-Vision](https://huggingface.co/meta-llama/Llama-3.2-11B-Vision) (LLama-VL-TUG base model) on [TechING](https://huggingface.co/datasets/Exploration-Lab/TechING) dataset, run the following bash script.  
**Example Usage**
```bash
torchrun --nproc_per_node=1 -m train.train \
  --output_dir checkpoints/ \
  --per_device_train_batch_size 1 \
  --gradient_accumulation_steps 1 \
  --learning_rate 2e-5 \
  --weight_decay 0.05 \
  --num_train_epochs 1 \
  --lr_scheduler_type cosine \
  --warmup_ratio 0.2 \
  --save_strategy steps \
  --save_steps 1000 \
  --logging_steps 10 \
  --dataloader_num_workers 8 \
  --report_to none \
  --run_name training \
  --seed 89 \
  --lora_rank 32 \
  --lora_alpha 16 \
  --lora_dropout 0.2 \
  --use_rslora True \
  --ddp_backend nccl \
```

### 2. Evaluation Scripts for Llama-VL-TUG:
| Script | Task | Evaluation Dataset|
|----------|-------------| -------- |
|eval/eval_imagetocode.py| Image2Code | D1 |
|eval/eval_desctocode.py| Desc2Code  | D1 |
|eval/eval_imagetodesc.py| Image2Desc | D1 |
|eval/eval_imagetocodeRealWorld.py| Image2Code | D3 |

**Example Usage**  
For running Image2Code on D1 Dataset, use the script eval_imagetocode.py and run it as 
  a python module. Arguments will remain same for all the evaluation scripts.
```bash
python3 -m eval.eval_imagetocode \
    --output_dir checkpoints \
    --model_path Exploration-Lab/LLama-VL-TUG
```

### 3. Evaluation Arguments for baselines (eval.py):

| Argument | Description | Possible Values |
|----------|-------------|---------|
| `--seed` | Random seed for reproducibility | `Any number` |
| `--diag_type` | Diagram type | `Block` `C4` `Class` `Flowchart` `Graph` `Packet` `Sequence` `State` |
| `--model` | Model name | `llama` `gemma` `qwen` `minicpm` `gpt` `llamavltug` |
| `--task` | Task type | `image2code` `desc2code` `image2desc` |
| `--dataset` | Dataset identifier | `D1` `D3`|
| `--device` | GPU device ID | `0` `1` `0,1,2` `0,2` `etc` |

**Example Usage**
```bash
python eval.py \
  --seed 89 \
  --diag_type Block \
  --model llama \
  --task image2code \
  --dataset D1 \
  --device 0
```

## Evaluation Results
The radar charts present ROUGE-L performance across the 
three primary tasks on the D1 test set, comparing LLama-VL-TUG 
against baselines of comparable model size. Detailed results are 
provided in our paper, [TechING: Towards Real World Technical Image Understanding via VLMs](https://arxiv.org/abs/2601.18238).
<img src="images/evaluation_results.png">

## Citation

[**TechING: Towards Real World Technical Image Understanding via VLMs**](https://2026.eacl.org/), In the 19th Conference of the 
European Chapter of the Association for Computational Linguistics (EACL) to be held in Rabat, Morocco, from March 24–29, 2026.
```
@misc{nadeem2026techingrealworldtechnical,
      title={TechING: Towards Real World Technical Image Understanding via VLMs}, 
      author={Tafazzul Nadeem and Bhavik Shangari and Manish Rai and Gagan Raj Gupta and Ashutosh Modi},
      year={2026},
      eprint={2601.18238},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2601.18238}, 
}
```