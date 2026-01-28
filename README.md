# TechING

This is the official Github repo of the paper:  

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

The following figure gives a complete overview of our paper:
<img src="TechING_overview.png">