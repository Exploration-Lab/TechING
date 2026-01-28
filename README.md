# TechING (Technical Image Understanding)

<img src="TechING_overview.png">

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