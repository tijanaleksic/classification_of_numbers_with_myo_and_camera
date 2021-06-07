# -*- coding: utf-8 -*-
"""
Created on Thu May 20 22:41:03 2021

@author: LENOVO
"""

# ovaj kod sluzi za predikciju ukoliko imamo sliku koju je potrebno klasifikovati
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import time
# ucitava i sredjuje sliku
def load_image(filename):
    # uciravanje slike
    img = load_img(filename, grayscale=True, target_size=(28, 28))
    # pretvaranje u niz
    img = img_to_array(img)
    # prebacuje u jedan sempl date velicine
    img = img.reshape(1, 28, 28, 1)
    # stavlja vrednosti pixela u normalnu formu
    img = img.astype('float32')
    img = img / 255.0
    return img

# ucitavnaje slike i pokretanje test primera na osnovu toga
def run_example():
    #ucitavanje slike
    img = load_image('output_test.png')
    #ucitavanje modela klasifikatora
    model = load_model('final_model.h5')
    # predikcija klase datog test  primera
    digit = model.predict_classes(img)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Broj koji je klasifikator prepoznao : ")
    #ispis klase
    print(digit[0])
    time.sleep(300)

# entry point, run the example
run_example()