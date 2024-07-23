import numpy as np  
import matplotlib.pyplot as plt  
import tensorflow as tf  
from tensorflow.keras.applications import ResNet50  
from tensorflow.keras.preprocessing.image import load_img, img_to_array  
from tensorflow.keras.preprocessing.text import Tokenizer  
from tensorflow.keras.utils import pad_sequences  
from tensorflow.keras.models import Model  
from tensorflow.keras.layers import Dense, Embedding, LSTM, Add, Input  
from sklearn.model_selection import train_test_split
import os

# Define paths  
image_folder_path = 'image_dataset/images/'  # Use the dataset I provided containing images and captions for them
caption_file_path = 'image_dataset/captions.txt'  

# Initialize a dictionary to hold image filenames and their captions  
captions = {}    

# Open the caption file to read  
with open(caption_file_path, 'r') as f:  
    for line in f:  
        # Split each line into image filename and caption using comma as delimiter  
        image_filename, caption = line.strip().split(',', 1)  # Use maxsplit=1 to only split on the first comma  
        captions[image_filename.strip()] = caption.strip()  # Strip whitespace from both parts  

# captions will now be a dictionary where the key is the image filename and the value is the caption  

# Prepare the list of images and their corresponding captions  
images = []  
captions_list = []  
for filename in os.listdir(image_folder_path):  
    if filename in captions:  
        images.append(os.path.join(image_folder_path, filename))  
        captions_list.append(captions[filename])  

# Prepare the data (e.g., tokenization, padding)  
tokenizer = Tokenizer()  
tokenizer.fit_on_texts(captions)  
vocab_size = len(tokenizer.word_index) + 1  

# Convert captions to sequences of integers  
sequences = tokenizer.texts_to_sequences(captions)  

# Pad the sequences to ensure uniform input size  
max_length = max(len(seq) for seq in sequences)  
padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post')

def extract_features(images):  
    model = ResNet50(weights='imagenet', include_top=False, pooling='avg')  
    features = []  
    for img in images:  
        image = load_img(img, target_size=(224, 224))  
        image = img_to_array(image)  
        image = np.expand_dims(image, axis=0)  
        image = tf.keras.applications.resnet50.preprocess_input(image)  
        feature = model.predict(image)  
        features.append(feature.flatten())  
    return np.array(features)  

image_features = extract_features(images)

X1_train, X1_val, X2_train, X2_val = train_test_split(image_features, padded_sequences, test_size=0.2)

def define_model(vocab_size, max_length):  
    # Image feature input  
    input1 = Input(shape=(2048,))  
    fe1 = Dense(256, activation='relu')(input1)  

    # Sequence input  
    input2 = Input(shape=(max_length,))  
    se1 = Embedding(vocab_size, 256, mask_zero=True)(input2)  
    se2 = LSTM(256)(se1)  

    # Merging  
    decoder1 = Add()([fe1, se2])  
    decoder2 = Dense(256, activation='relu')(decoder1)  
    output = Dense(vocab_size, activation='softmax')(decoder2)  

    model = Model(inputs=[input1, input2], outputs=output)  
    
    model.compile(loss='categorical_crossentropy', optimizer='adam')  
    return model  

model = define_model(vocab_size, max_length)


from tensorflow.keras.utils import to_categorical  

# Prepare output data  
y_train = to_categorical(sequences[:, 1:], num_classes=vocab_size)  # Skip the first word  
y_val = to_categorical(sequences[:, 1:], num_classes=vocab_size)  

# Train the model  
model.fit([X1_train, X2_train], y_train, epochs=10, validation_data=([X1_val, X2_val], y_val))

# Save the model
model.save('image_captioning_model.h5') 

def generate_caption(model, tokenizer, photo, max_length):  
    in_text = '<start>'  # Start with the start token  
    for i in range(max_length):  
        sequence = tokenizer.texts_to_sequences([in_text])[0]  
        sequence = pad_sequences([sequence], maxlen=max_length)  
        yhat = model.predict([photo, sequence], verbose=0)  
        yhat = np.argmax(yhat)  # Get word index with the highest probability  
        word = tokenizer.index_word[yhat]  

        if word == '<end>':  
            break  
        in_text += ' ' + word  
    return in_text  

# Load a new image and generate caption  
# Example usage (provide your image path):  
# photo = extract_features(['path/to/image.jpg'])  
# caption = generate_caption(model, tokenizer, photo, max_length)  
# print(caption)

# Example usage for generating a caption for a new image  
new_image_path = 'image_dataset\Images\12830823_87d2654e31.jpg' 
photo = extract_features([new_image_path])  # Extract features for the new image  
caption = generate_caption(model, tokenizer, photo, max_length)  # Generate caption  
print("Generated Caption:", caption)  # Print the generated caption  

# Optionally, display the image  
img = load_img(new_image_path, target_size=(224, 224))  
plt.imshow(img)  
plt.axis('off')  
plt.show()  