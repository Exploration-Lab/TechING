from PIL import Image
import albumentations as A
import numpy as np


transform = A.Compose([
    A.OneOf([
        A.MotionBlur(p=0.5),
        A.MedianBlur(blur_limit=3, p=0.5),
        A.GaussianBlur(blur_limit=(3, 5), p=0.5),
    ], p=0.7),
    A.OneOf([
        A.RGBShift(r_shift_limit=80, g_shift_limit=80, b_shift_limit=80, p=0.8),
        A.HueSaturationValue(hue_shift_limit=15, sat_shift_limit=25, val_shift_limit=20, p=0.8),
    ], p=0.9),
    A.RandomBrightnessContrast(brightness_limit=0.4, contrast_limit=0.2, p=0.7),
    A.OneOf([
        A.Rotate(limit=30, p=0.5),
        A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.2, rotate_limit=45, p=0.3),
    ], p=0.3),
    A.OneOf([
        A.GridDistortion(p=0.5),   
    ], p=0.2),
    A.Perspective(scale=(0.01, 0.05), p=0.4), 
    A.OneOf([
    A.CoarseDropout(max_holes=4, max_height=16, max_width=16, p=0.3), 
    A.GridDropout(ratio=0.2, p=0.1), 
    ]),
    A.OneOf([
        A.RandomRain(p=0.3), 
        A.RandomFog(p=0.3), 
        A.RandomShadow(p=0.8), 
    ], p=0.4),
    A.CLAHE(p=0.3),
    A.Sharpen(p=0.3),
], p=0.9)

def augment_pil_image(pil_img, transform):
    image_np = np.array(pil_img)
    augmented = transform(image=image_np)
    augmented_image_np = augmented['image']
    return Image.fromarray(augmented_image_np)