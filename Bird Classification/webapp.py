import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow import keras
import tensorflow_hub as hub
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import cv2 as cv
import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)
print ('modules loaded')

# Import model

model = keras.models.load_model('./400_bird_speciesClassification_EFFNetB0V2.h5', custom_objects={'KerasLayer':hub.KerasLayer})

detect_model  = hub.load("https://tfhub.dev/tensorflow/efficientdet/d1/1")

# Create function to extract any bird frame from a picture using the pre-trained model from tensorflow hub

def bird_extractor(detector, image, threshold = 0.5):
    # get image dimentions
    width, height = image.shape[0], image.shape[1]
    
    # Object detection
    detector_output =  detector(np.expand_dims(image, axis = 0))
    
    # For birds, coco dataset assigns the value 16
    bird_ext = detector_output["detection_classes"] == 16
    
    # Apply threshold
    bird_ext = (detector_output["detection_scores"] > threshold) & bird_ext
    
    draw_box = detector_output["detection_boxes"][bird_ext]
    
    # Extract ROI and coordinates for each detection image bird
    bird_image = []
    
    for box in draw_box:
        corner_min = (int(box[1] * height), int(box[0] * width))
        corner_max = (int(box[3] * height), int(box[2] * width))
        bird_image.append((image[corner_min[1] : corner_max[1], corner_min[0] : corner_max[0]],  
                        (corner_min, corner_max)))
        
    return bird_image


# Load and get bird class name list

from tensorflow.keras.preprocessing.image import ImageDataGenerator 
# Get folder for each train, test, and valid pictures
dataset_dir = "100-bird-species"

train_dir = dataset_dir + "/" + "train"

datagen = ImageDataGenerator(
         rescale = 1/255.0)

# Load and iterate training dateset
train_it = datagen.flow_from_directory(train_dir,
                                      target_size = (224,224)
                                      #class_mode = 'categorical',
                                      #color_mode ='rgb'
                                      )

# Get class names
class_names = train_it.class_indices
class_names = list(class_names.keys())


# Create a function that combines classification model and the extract function

def classify_birdSpecies(model, rois):
    
    predictions = [] # list of bird species identified
    
    for roi in rois:
        roi_resized = tf.image.resize(roi[0] / 255.0, (224, 224))
        prediction = tf.argmax(model.predict(tf.expand_dims(roi_resized, axis = 0)), axis = 1)
        predictions.append((class_names[int(prediction)]))

    return predictions

def draw_birdBox(image, rois, predictions):
    image_copy = image.copy()
    
    for n, roi in enumerate(rois):
        cv.rectangle(image_copy, roi[1][0], roi[1][1], (0, 255, 0))
        cv.putText(image_copy, predictions[n], roi[1][0], 
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    
    return image_copy

def bird_detectionClass(image, bird_detector = detect_model, species_classifier = model):
    # detect birds in the image
    rois = bird_extractor(bird_detector, image, threshold = 0.5)
    
    # identify bird species
    species = classify_birdSpecies(species_classifier, rois)
    
    # draw bounding boxes and text
    output_image = draw_birdBox(image, rois, species)
    
    return output_image


# Create a Streamlit Web App

st.write("""
         # Bird Classification Prediction App
         """
         )


st.write("This is a simple image classification web app to predict the name of the species of birds")


file = st.file_uploader("Please upload an image file", type=["jpg"])

if file is None:
    
    st.text("Please upload an image file")

else:
    
    image = plt.imread(file)
    bird_pred = bird_detectionClass(image)
    st.image(bird_pred, use_column_width=True)
    st.text("Name of bird: ")
    rois = bird_extractor(detect_model, bird_pred, threshold=0.5)
    name_pred = classify_birdSpecies(model = model, rois = rois)
    st.write(name_pred)






