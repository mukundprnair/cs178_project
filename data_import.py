import numpy as np
import pandas as pd
import os
import tensorflow as tf 
from sklearn.preprocessing import LabelEncoder
from PIL import Image
from collections import defaultdict

def read_csv_as_numpy():
    # Load CSV and prepare file paths
    csv_path = './data/legend.csv'
    image_dir = './images'
    df = pd.read_csv(csv_path)
    df['filepath'] = df['image'].apply(lambda x: os.path.join(image_dir, x))

    # Encode labels
    label_encoder = LabelEncoder()
    df['emotion'] = df['emotion'].str.upper()
    df['encoded_label'] = label_encoder.fit_transform(df['emotion'])
    classes = label_encoder.classes_ 

    # Load images and labels into NumPy arrays
    filepaths = df['image'].values
    labels = df['encoded_label'].values

    images = []
    i = 0
    for filepath in filepaths:
        # Load and preprocess image
        image_filepath = "./images/" + filepath
        image = Image.open(image_filepath)
        if image.mode == 'RGB':
            image = image.convert('L')  # 'L' mode is for grayscale

        image_array = np.array(image)
        if image_array.shape != (350, 350):
            continue
        images.append(image_array)  # Convert Tensor to NumPy array
    
    images = np.array(images, dtype=np.float32)  # Convert list to NumPy array
    labels = np.array(labels, dtype=np.int32)   # Convert labels to NumPy array

    # Shuffle the dataset
    indices = np.arange(len(images))
    np.random.shuffle(indices)
    images = images[indices]
    labels = labels[indices]

    # Train-validation split
    train_size = int(0.8 * len(images))
    X_train, X_val = images[:train_size], images[train_size:]
    y_train, y_val = labels[:train_size], labels[train_size:]

    return X_train, y_train, X_val, y_val, classes

if __name__ == '__main__':
    X_tr, Y_tr, X_val, Y_val, classes = read_csv_as_numpy()

    print(X_tr.shape)
    print(X_tr[0, :])
    print(Y_tr.shape)
    print(Y_tr[0])
    
    print(X_val.shape)
    print(Y_val.shape)

    print(classes)