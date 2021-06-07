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
import cv2
import threading


ime_ispitanika = 'Tijana.txt'

emgIme_pesnica = 'EMG_pesnica_'+ime_ispitanika
emgIme_ostalo = 'EMG_ostalo' + ime_ispitanika 
global_flag = 0



def tred(stop):
    global flg_zapoceto_snimanje
    global stop_threads
    while True:
        #otvaranje video_show
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        #cap = cv2.VideoCapture(0)
        
        # kreiranje video rekoredera
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output_br_test.avi',fourcc, 0.005, (640,480))
        
        
        while(cap.isOpened()):
            #ucitavanje frejma
            ret, frame = cap.read()
            if ret==True:
                #okretanje frejma jer je naopako snimljeno
                frame = cv2.flip(frame,1)
        
                #ispis frejma
                out.write(frame)
        
                cv2.imshow('frame',frame)
                
                #ovo je za prekidanje niti koja se paralelno izvrsava
                if (flg_zapoceto_snimanje==2):
                    print(" plakyyy")
                    cap.release()
                    out.release()
                    cv2.destroyAllWindows()
                    t1.join()
                    break
                if stop_threads:
                    print("to treba da radim al sam plakyyy")
                    cap.release()
                    out.release()
                    cv2.destroyAllWindows()
                    #t1.join()
                    break
            else:
                break
        
    


        
#funkcija koja ako mu prosledimo model klasifikatora i trenutne vrednosti sa 
# emgova vraca klasu koja je najslicnija po tom klasifikatoru
def test_custom(model,arr):
    out = model.predict(arr);
    return out

#u ovooj funkciji ucitavam test podatke koji se koriste za klasifikaciju i 
#pravljenje samog modela
def get_model():
    #lokacije unapred snimljenih podataka
    
    #lokacija test podataka se nalaze u direktorijumu pod nazivom test_set
    dir_path = os.getcwd()+'\\test_set'
    file_loc = dir_path + '\\test_pesnica.txt'
    file_loc1 = dir_path + '\\test_ostalo.txt'
    
    
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

    #parcionisanje podataka za validaciju i treniranje
    X_train, X_test, y_train, y_test = train_test_split(rez, klasa, test_size = 0.20);

    # pravljenje klasifikatora
    svclassifier = SVC(kernel='rbf')
    
    
    #treniranje klasifikatora 
    svclassifier.fit(X_train, y_train)
    
    
    #testiranje na test setu da bi se znalo koliko dobro klasifikuje 
    y_pred = svclassifier.predict(X_test);
    
    #ispis validacije
    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test,y_pred))
    
    #povratak klasifikatora
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
        global brojac;
        global niz_proslosti
        global flg_zapoceto_snimanje
        global global_flag
        parts = []
        parts_emg = []
        parts_emg_matrix=[[]]
        parts.append(str(self.pose).ljust(10))
        parts.append('E' if self.emg_enabled else ' ')
        parts.append('L' if self.locked else ' ')
        parts.append(self.rssi or 'NORSSI')
        
        
        #poza koju je njihov klasifikator odredio
        pose_now = str(self.pose)
        
        #upisivanje emg signala koji nam trebaju da bi prosledili nasem 
        #klasifikatoru te na osnovu njih preoznali trenutni polozaj ruke
        if self.emg:
            for comp in self.emg:
                    parts.append('{}{:.4f}'.format(' ' if comp >= 0 else '', comp))
                    parts_emg.append(float('{}{:.4f}'.format(' ' if comp >= 0 else '', comp)))
                    parts_emg_matrix[0].append(float('{}{:.4f}'.format(' ' if comp >= 0 else '', comp)))
            #emgFile_pesnica.write('\n')
            
        #provera da l moze uopste da se prosledi jer ima problem da  
        #samo ponekad ne ucita lepo podatke, ako su ok podaci salje ih 
        #klasifikatoru da ih prepozna    
        if(len(parts_emg_matrix[0]) != 0):
            out = test_custom(klasifikator,parts_emg_matrix)
        else:
            out="fejl"
        print('Dobijeno = '+str(out[0])+', ocekivano je = '+str(pose_now))
        
        
        #pravljenje istorije podataka da bi se minimizovala greska da se 
        #prepozna kratkotrajno lose
        if(out[0] == 'pesnica'):
            niz_proslosti[(brojac % 10)] = 1
        else:
            niz_proslosti[(brojac % 10)] = 0 
            
            
            
        #na osnovu poslednjih 10 odbiraka biramo da li snimamo ili ne
        if(sum(niz_proslosti)>3):
            print('snimam trenutno')
            #ako je zapoceto snimanje u datom trenutku tada pozivamo 
            #izvrsavanje paralelne niti koja pravi snimak dok glavna nit 
            #za ucitavanje podataka sa emg i dalje nastavlja da radi
            if(flg_zapoceto_snimanje == 0):
                #zapocinjanje niti paralelno da radi
                t1.start()
            #postavljanje flega na vrednost 1 jer ne treba vise od 
            #jednom da pozove prethodnu nit
            flg_zapoceto_snimanje = 1
            
        else:
            if(flg_zapoceto_snimanje == 1):
                
                print('krajjj snimanjaaaaaaaaaa')
                print("pre ubijanja ")
                
                #ovo je za zavrsavanje niti malo hardkodvano
                flg_zapoceto_snimanje = 2
                #stop_threads = True;
                
                #t1.join()
                print("ubijen sam oh nooooooooo")
                
        
                #pozivanje dalje klasifikacije (obrade snimka koji je snimnljen)
                os.system('python -W ignore long_exposure.py')
        
        #ovo sluzi da bi moglo lepo da se vrsi zadnjih 10 koraka
        brojac = brojac + 1
               
        
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
  #pravljenje kalsifikatora  
  klasifikator = get_model()
  
  
  #emgFile_pesnica = open(emgIme_pesnica, 'w')
  #emgFile_ostalo = open(emgIme_ostalo, 'w')
  
  #iinicijalizovanje proslosti i brojaca kao i identifikatora za zapoceto snimanje
  brojac = 0
  niz_proslosti= [0,0,0,0,0,0,0,0,0,0]
  flg_zapoceto_snimanje = 0
  
  #ovo mu je potrebno da bi dobio sve funkcije koje je MIT implmentirao
  myo.init(sdk_path='./myo-sdk-win-0.9.0')
  hub = myo.Hub()
  listener = Listener()

  #pravljenje niti kooja sluzi za pozivanje video rekordera
  stop_threads = False
  t1 = threading.Thread(target = tred, args =(lambda : stop_threads, ))

  try:
    while hub.run(listener.on_event, 500):
      pass
  except KeyboardInterrupt:
    print("Quitting...")
  #finally:
    #emgFile_pesnica.close()
    #emgFile_ostalo.close()
   