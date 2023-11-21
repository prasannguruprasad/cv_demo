import warnings 
warnings.filterwarnings("ignore", category = FutureWarning)
warnings.filterwarnings("ignore", category = DeprecationWarning)
import os 
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import argparse
from PIL import Image as PILImage
import matplotlib.pyplot as plt
from IPython.display import Image, display

def predict_image(model, class_path, image_path): 
  img1 = PILImage.open(image_path)
  img = tf.keras.preprocessing.image.load_img(image_path,target_size=input_shape)
  img = tf.keras.preprocessing.image.img_to_array(img)
  img = np.expand_dims(img, axis=0)
  img = img/255
  # prediction
  result = model.predict(img)
  lines = [line.replace("\n","") for line in open(class_path,"r").readlines()]
  classes = {i:lines[i] for i in range(len(lines))}
  prediction_probability = {i:j for i,j in zip(classes.values(),result.tolist()[0])}
  max_value = max(prediction_probability.values())
  keys_with_max_value = [k for k, v in prediction_probability.items() if v == max_value]
  print("\n\nPrediction: \n")
  print(os.path.basename(image_path) + " " + keys_with_max_value[0] + " (" + str(max_value) + ")")

def predict_images_in_directory(model, class_path, directory_path): 
  for root, dirs, files in os.walk(directory_path):
    for filename in files: 
      file_path = os.path.join(root, filename)
      if os.path.isfile(file_path):
        predict_image(model, class_path, file_path)

def main():
  parser = argparse.ArgumentParser(description='Argument to collect info')
  parser.add_argument('--model_path', help='path to the downloaded model')
  parser.add_argument('--class_path', help='path to the downloaded classnames file')
  parser.add_argument('--image_path', help='path to the test image')
  args = parser.parse_args()
  model_path = args.model_path
  class_path = args.class_path
  image_path = args.image_path
  #load model
  model = tf.keras.models.load_model(model_path,custom_objects={'KerasLayer':hub.KerasLayer})
  global input_shape
  input_shape = model.input_shape[1:]
  if os.path.isfile(image_path): 
    predict_image(model, class_path, image_path)
  elif os.path.isdir(image_path):
    predict_images_in_directory(model, class_path, image_path)
    # for filename in os.listdir(image_path): 
    #   file_path = os.path.join(image_path, filename)
    #   if os.path.isfile(file_path):
    #     predict_image(model, class_path, file_path)
    #   elif os.path.isdir(file_path):
    #     predict_images_in_directory(model, class_path, image_path)
  else: 
    print("Invalid path: {}".format(image_path))

if __name__ == "__main__": 
  main()