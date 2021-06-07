# The MIT License (MIT)
# The MIT License (MIT)
#
# Copyright (c) 2017 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHEHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
"""
This example displays the orientation, pose and RSSI as well as EMG data
if it is enabled and whether the device is locked or unlocked in the
terminal.
Enable EMG streaming with double tap and disable it with finger spread.
"""


from __future__ import print_function
from myo.utils import TimeInterval
import myo
import sys

import re
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import os


ime_ispitanika = 'Sara.txt'

emgIme_pesnica = 'EMG_pesnica_'+ime_ispitanika
emgIme_ostalo = 'EMG_ostalo' + ime_ispitanika 


def test_custom(model,arr):
    out = model.predict(arr);
    #print(model.predict(arr))
    return out

def get_model():
    #lokacije unapred snimljenih podataka
    dir_path = os.getcwd()+'\\test_set'
    file_loc = dir_path + '\\set_pesnica.txt'
    file_loc1 = dir_path + '\\set_ostalo.txt'
    
    
    
    #obrada prvog fajla
    f = open(file_loc, 'r')
    arr_1,arr_2,arr_3,arr_4,arr_5,arr_6,arr_7,arr_8,klasa = [],[],[],[],[],[],[],[],[]
    matrix = [];
    for line in f.readlines():
        fields = re.split(r'\s+', line)
        arr_1.append(float(fields[0]))
        arr_2.append(float(fields[1]))
        arr_3.append(float(fields[2]))
        arr_4.append(float(fields[3]))
        arr_5.append(float(fields[4]))
        arr_6.append(float(fields[5]))
        arr_7.append(float(fields[6]))
        arr_8.append(float(fields[7]))
        klasa.append('pesnica');
    f.close()

    #obrada drugog fajla
    #za opustenu ruku ubacivanje stvari
    f1 = open(file_loc1, 'r')
    for line in f1.readlines():
        fields = re.split(r'\s+', line)
        arr_1.append(float(fields[0]))
        arr_2.append(float(fields[1]))
        arr_3.append(float(fields[2]))
        arr_4.append(float(fields[3]))
        arr_5.append(float(fields[4]))
        arr_6.append(float(fields[5]))
        arr_7.append(float(fields[6]))
        arr_8.append(float(fields[7]))
        klasa.append('ostalo');
    f1.close()


    #kreiranje matrice koja se parcionise na trening i test primere
    matrix.append(arr_1);
    matrix.append(arr_2);
    matrix.append(arr_3);
    matrix.append(arr_4);
    matrix.append(arr_5);
    matrix.append(arr_6);
    matrix.append(arr_7);
    matrix.append(arr_8);
    
    
    #okretanje matrice jer je potrebno biti po kolonama a ne po vrstama
    rez = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

    #razdvajanje testa za validaciju i trening seta
    X_train, X_test, y_train, y_test = train_test_split(rez, klasa, test_size = 0.20);

    #pravljenje klasifikatora sa kernelom 
    svclassifier = SVC(kernel = 'rbf')
    
    #treniranje klasifikatora na trening podacima
    svclassifier.fit(X_train, y_train)
    
    y_pred = svclassifier.predict(X_test);
    
    
    #validacioni parametri klasifikatora , koji je koriscen
    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test,y_pred))

    #vraca gotov klasifikator za koriscenje
    return svclassifier
class Listener(myo.DeviceListener):

    def __init__(self):
        self.interval = TimeInterval(None, 0.05)
        self.orientation = None
        self.gyroscope = None
        self.acceleration = None
        self.pose = myo.Pose.rest
        self.emg_enabled = True
        self.locked = False
        self.rssi = None
        self.emg = None

  
    def output(self):
        if not self.interval.check_and_reset():
           return
    
        parts = []
        #parts_= []
        parts_emg = []
        parts_emg_matrix = [[]]
        parts.append(str(self.pose).ljust(10))
        parts.append('E' if self.emg_enabled else ' ')
        parts.append('L' if self.locked else ' ')
        parts.append(self.rssi or 'NORSSI')
        
        #trenunta klasa po njihovom klasifikatoru
        pose_now = str(self.pose)#.ljust(10)
        if (pose_now=="Pose.fist"):
            print('uso sam u if \n')
            if self.emg:
                for comp in self.emg:
                    parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
                    emgFile_pesnica.write(str(comp) + ' ')
                    parts_emg.append(float('{}{:.4f}'.format(' ' if comp >= 0 else '', comp)))
                    parts_emg_matrix[0].append(float('{}{:.4f}'.format(' ' if comp >= 0 else '', comp)))
            emgFile_pesnica.write('\n')
        else:
            if self.emg:
                for comp in self.emg:
                    parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
                    emgFile_ostalo.write(str(comp) + ' ')
                    parts_emg.append(float('{}{:.4f}'.format(' ' if comp >= 0 else '', comp)))
                    parts_emg_matrix[0].append(float('{}{:.4f}'.format(' ' if comp >= 0 else '', comp)))
            emgFile_ostalo.write('\n')
            print(pose_now);
        
        if(len(parts_emg_matrix[0])!=0):
            out = test_custom(klasifikator,parts_emg_matrix)
        else:
            out="fejl"
        print('Dobijeno = '+str(out)+', ocekivano je = '+str(self.pose).ljust(10))
        
        
        sys.stdout.flush()


    def on_connected(self, event):
        event.device.request_rssi()
        event.device.stream_emg(True)

    def on_rssi(self, event):
        self.rssi = event.rssi
        self.output()

    def on_pose(self, event):
        self.pose = event.pose
        self.output()

    def on_orientation(self, event):
        self.acceleration = event.acceleration
        self.gyroscope = event.gyroscope
        self.output()

    def on_emg(self, event):
        self.emg = event.emg
        self.output()

    def on_unlocked(self, event):
        self.locked = False
        self.output()

    def on_locked(self, event):
        self.locked = True
        self.output()


if __name__ == '__main__':
  klasifikator = get_model()
  #emgFile = open(emgIme , 'w')
  #accFile = open(accIme , 'w')
  #gyrFile = open(gyrIme , 'w')
  #myfile = open(myname ,'w')
  #myfile_ag = open(name_ag , 'w')
  #calibration_file = open(calibration_name_file, 'w')
  emgFile_pesnica = open(emgIme_pesnica, 'w')
  emgFile_ostalo = open(emgIme_ostalo, 'w')
  
  
  
  myo.init(sdk_path='./myo-sdk-win-0.9.0')
  hub = myo.Hub()
  listener = Listener()

  try:
    while hub.run(listener.on_event, 500):
      pass
  except KeyboardInterrupt:
    print("Quitting...")
  finally:
    emgFile_pesnica.close()
    emgFile_ostalo.close()
    #emgFile.close()
    #accFile.close()
    #gyrFile.close()
    #myfile.close()
    #myfile_ag.close()
    #calibration_file.close()