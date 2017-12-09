#!/usr/bin/python
# -*- coding: iso8859-2 -*- # 

import sys
import os
import time
import serial
import Tkinter
import threading
import thread
import string
#import Gnuplot,Gnuplot.funcutils

Uref =  2.640


# dodano 2011.05.05
# tu jest mala poprawka w uzyciu tego programu w komunikacji z laptopem Toshiba - nie bardzo chcš działać 
# linie markerow komunikacyjnych - RTS i CTS
# ta wersja ma je wylaczone

#poprawki = [9,0,0,7,6,10,0]
poprawki = [0,0,0,7,6,10,0]
global jak_czesto_na_ekran
jak_czesto_na_ekran=0
global miejsce_czasu
#gplot=Gnuplot.Gnuplot()

class MyThread ( threading.Thread ):
         def stop(self):
                  print "koniec"
                  self._Thread__stop()
                  #thread.exit_thread()                  
         def run ( self):
                  self.koniec=0
                  self.poprzednie_wyswietlenie=time.time()
                  while(self.koniec==0):
                           #print self.koniec
                           
                           line=ser.readline()
                           if len(line)>1:
                                    print str(os.times()[4]-start),line
                                    print line
                                    log.write(str(time.time()-start)+" "+str(line))
                                    tabela=line.split(",")
                                    tabela.pop()
                                    blad=0
                                    for i in tabela:
                                             try:
                                                      if i[0] is not 'i' :
                                                            float(  eval('0x'+i)  )
                                             except:
                                                      print "pomijam:",i
                                                      blad=1
                                    if blad==1:
                                             blad==0
                                             
                                             continue                                                      
                                             
                                    #print tabela
                           #usuwam ostatni znak
                                    
                                    na_ekran=str(time.time()-start)+" "
                                    plik.write(str(time.time()-start)+" ")
                                    polozenie=0
                                    for i in tabela:
                                             #polozenie=tabela.index(i)
                                             #print i.isdigit()
                                             #if i<>:
                                              #        print "zle :",i
                                             #sprawdz czy ktoras z cyfr liczby nie jest cyfra                      
                                             '''for iter in [0,1,2]:
                                                      if (i[iter] in string.hexdigits)==False:
                                                             
                                                             print i
                                                             i=i.replace(i[iter],"0")
                                                             print "poprawiono:",i
                                                             continue'''
                                             if i[0] is not 'i' :
                                                   i=eval('0x'+i)
                                                    
                                                   i=float(i)
                                                   #+poprawki[polozenie]
                                                   #if i>550:
                                                   i=(Uref/1024*(i-512))*100
                                                   
                                                   #else:
                                                        
                                                   #     i=(2.56/1024*i)*100
                                                   #i=(2.56/1024*i)*100
                                                   #i=(2.5/1024*i)*100
                                                   #if (polozenie==0):
                                                                                                      
                                                   
                                             elif i[0] is 'i':
                                                   i=eval('0x'+i[1:])
                                                    
                                                   i=float(i)
                                                   
                                             na_ekran= na_ekran+str(i)+" "
                                             plik.write("\t"+str(i) + "\t")     
                                             polozenie=polozenie+1
                                                   
                                    plik.write("\n")
                                    #gplot.plot(war)
                                    #print divmod(os.times()[4]-start,5)[1]
                                    #if int(divmod(os.times()[4]-start,jak_czesto_na_ekran)[1])==0:
                                    
                                    if round(time.time()-self.poprzednie_wyswietlenie,2)>jak_czesto_na_ekran:
                                             self.poprzednie_wyswietlenie=time.time()
                                             print na_ekran
                  #ser.setRTS(1)
                  #time.sleep(10)
                  ser.write("*P0\n")
                  #ser.setRTS(0)                           
                                   
                  print "koniec"                           
                  plik.close()
                           
                  
class MyApp:                        
         def __init__(self, parent):
                  self.kanal="1"
                  self.czas="1"
                  self.srednia="1"
                  self.myParent=parent
                  self.myContainer1 = Tkinter.Frame(self.myParent)
                  #self.myContainer1.pack()
                  self.myContainer1.grid()
                  
                  self.button1 = Tkinter.Button(self.myContainer1)
                  self.button1["text"]= "Pomiary"
                  self.button1["background"] = "green"
                  #self.button1.pack()
                  self.button1.grid(column=0,row=0)
                  self.button1.bind("<Button-1>",self.PushButton1)
                  
                  
                  self.button22= Tkinter.Button(self.myContainer1)
                  self.button22["text"]= "Srednia"
                  
                  #self.button22.pack()
                  self.button22.grid(column=1,row=0)
                  self.button22.bind("<Button-1>",self.PushButton22)         
                  
                  self.button2 = Tkinter.Button(self.myContainer1)
                  self.button2["text"]= "Pomiary Stop"
                  self.button2["background"] = "green"
                  #self.button2.pack(side=Tkinter.LEFT)
                  self.button2.grid(column=2,row=0)
                  self.button2.bind("<Button-1>",self.PushButton2)
                  
                  self.button3 = Tkinter.Button(self.myContainer1)
                  self.button3.configure(text= "Quit")
                  #self.button3.pack(side=Tkinter.LEFT)
                  self.button3.grid(column=3,row=0)
                  self.button3.bind("<Button-1>",self.PushButton3)
                                                
                  
                  
                  self.lab1=Tkinter.Label(self.myParent, text="Wybierz ilosc kanalow")
                  #self.lab1.pack(side=Tkinter.LEFT)
                  self.lab1.grid(column=0,row=1)
                  self.listbox=Tkinter.Listbox()
                  for i in range (1,9):
                           self.listbox.insert(Tkinter.END, str(i))
                  #self.listbox.pack(side=Tkinter.LEFT)
                  self.listbox.grid(column=0,row=2)
                  self.listbox.bind("<ButtonRelease-1>",self.Wybor_1_listy)
                  
                  self.lab2=Tkinter.Label(self.myParent, text="Wybierz ilosc 1/16 s")
                  #self.lab2.pack(side=Tkinter.LEFT)
                  self.lab2.grid(column=1,row=1)
                  
                  self.listbox2=Tkinter.Listbox(selectmode=Tkinter.EXTENDED)
                  for i in (1,2,4,8,16,32,64):
                           self.listbox2.insert(Tkinter.END, str(i))
                  #self.listbox2.pack(side=Tkinter.LEFT)
                  self.listbox2.grid(column=1,row=2)
                  self.listbox2.bind("<ButtonRelease-1>",self.Wybor_2_listy)
                   
                  self.entry0=Tkinter.Entry()
                  self.entry0.insert(Tkinter.END,"ile 1/16 s")
                  #self.entry0.pack(side=Tkinter.TOP)
                  self.entry0.grid(column=1,row=3)
                  self.entry0.bind("<Return>",self.Przyjmij_Czas)
                                                     
                  self.lab3=Tkinter.Label(self.myParent, text="Wybierz srednia")
                  #self.lab3.pack()
                  self.lab3.grid(column=2,row=1)
                  
                  self.listbox3=Tkinter.Listbox(selectmode=Tkinter.EXTENDED)
                  for i in (1,2,4,8,16,32,64,128):
                           self.listbox3.insert(Tkinter.END, str(i))
                  #self.listbox3.pack()
                  self.listbox3.grid(column=2,row=2)
                  self.listbox3.bind("<ButtonRelease-1>",self.Wybor_3_listy)
                  #self.myParent.after_idle(dane_z_portu)  
                  self.entry1=Tkinter.Entry()
                  self.entry1.insert(Tkinter.END,"podaj nazwe pliku")
                  #self.entry1.pack(side=Tkinter.LEFT)
                  
                  self.entry1.grid(column=2,row=3)
                  self.entry1.bind("<Return>",self.Przyjmij_Tekst)
                  
                  self.entry2=Tkinter.Entry()
                  self.entry2.insert(Tkinter.END,"polecenie")
                  #self.entry0.pack(side=Tkinter.TOP)
                  self.entry2.grid(column=3,row=3)
                  self.entry2.bind("<Return>",self.Przyjmij_Polecenie)
                  0
                   
                  self.entry3=Tkinter.Entry()
                  self.entry3.insert(Tkinter.END,"polecenie2")
                  
                  self.entry3.grid(column=3,row=4)
                  self.entry3.bind("<Return>",self.Przyjmij_Polecenie2)
                  
                  self.entry4=Tkinter.Entry()
                  self.entry4.insert(Tkinter.END,"polecenie3")
                  
                  self.entry4.grid(column=3,row=5)
                  self.entry4.bind("<Return>",self.Przyjmij_Polecenie3)
                  
                  self.znacznik_zapisu=Tkinter.StringVar()
                  #self.znacznik_zapisu="a"
                  self.radion_button1=Tkinter.Radiobutton(self.myParent,text="kontynuacja pliku",variable=self.znacznik_zapisu,value="a",command=self.wypisz)
                  self.radion_button1.grid(column=2,row=4)
                  self.radion_button2=Tkinter.Radiobutton(self.myParent,text="nowy plik",variable=self.znacznik_zapisu,value="w",command=self.wypisz)
                  self.radion_button2.grid(column=2,row=5)
                  
          

         def wypisz(self):
                 self.znacznik_zapisue=self.znacznik_zapisu.get()
                 print self.znacznik_zapisu.get()
                  #," ",self.znacznik_zapisu.get()
                  
         def PushButton1(self,event):
                  
                  
                  #kanal=int(kanal)
                  print self.kanal," ",self.czas
                  self.czas=int(self.czas)
                  
                  if self.czas<16:
                           self.czas=hex(self.czas)
                           polecenie="*P"+self.kanal+".0"+str(self.czas)[2:]+"\n"
                  else:
                           self.czas=hex(self.czas)
                           polecenie="*P"+self.kanal+"."+str(self.czas)[2:]+"\n"
                           
                  print polecenie
                    #ser.
                  self.Sprawdz_czy_mozna_wysylac()
                  
                  #ser.setRTS(1)    
                  #time.sleep(10)                          
                  ser.write(polecenie)
                  
                  #ser.setRTS(0)
                  
         def PushButton22(self,event):
                  srednia=int(self.srednia)
                  if srednia<16:
                           srednia=hex(srednia)
                           srednia=str(srednia)
                           srednia="0"+srednia[2:]
                  else:
                           srednia=hex(srednia)
                           srednia=str(srednia)                          
                           srednia=srednia[2:]
                  polecenie="*S"+srednia+"\n"
                  #print polecenie
                    #ser.setRTS(0)
                  '''jezeli CTS==5V to wysylaj jezeli jest 0V tzn getCTS() daje TRUE to nie wysylaj czekaj az CTS=FALSE'''
                  self.Sprawdz_czy_mozna_wysylac()
                  #ser.setRTS(0)
                  ser.write(polecenie)
                  time.sleep(0.05)               
                  #ser.setRTS(1)
                  #print ser
         def PushButton2(self,event):
                  
                  self.Sprawdz_czy_mozna_wysylac()
                  
                  
                  #print "koniec ma wartosc ",self.pomiary.koniec
                  self.pomiary.koniec=1
                  #print "a teraz",self.pomiary.koniec
                  #self.pomiary.isAlive()
                  #self.pomiary.end()
                  
         def PushButton3(self,event):
                  print "Bye" 
                  ser.close()
                  log.close()
                  if dir('__main__')=="plik":
                           print "jest otwarty"
                           plik.close()
                        
                  #self.pomiary.koniec=1
                  print __name__
                  try:
                           if self.pomiary.isAlive():
                                    print "wciaz zyje"
                                    self.pomiary.stop()
                  except:
                           print "error"                                    
                  self.myParent.destroy()
                  
                  
                  sys.exit() 
                  
         def Wybor_1_listy(self,event):
                  self.kanal=self.listbox.selection_get()
                  #print self.kanal
                  #self.a=self.listbox2.curselection()
                  #print self.a
         def Wybor_2_listy(self,event):
                  self.czas=self.listbox2.selection_get()
         def Wybor_3_listy(self,event):
                  self.srednia=self.listbox3.selection_get()         
                  #print self.czas
         def Sprawdz_czy_mozna_wysylac(self):
                  while(ser.getCTS()==True):
                           #time.sleep(0.5)
                           print "moze za chwile"
                           pass               
         def Przyjmij_Tekst(self,event):
                  global start
                  global plik
                  #global gplot
                  global war
                  #global koniec
                  start=time.time()
                  #os.times()[4]
                  nazwa_pliku=self.entry1.get()
                  print nazwa_pliku," jako :",self.znacznik_zapisu.get()
                  
                  plik=open(nazwa_pliku,self.znacznik_zapisu.get(),12)
                  #wykonaj="ser2.py "+str(plik)
                  #os.popen3(wykonaj)
                  #war=Gnuplot.File(str(nazwa_pliku),with="line",using="1:2")
                  try:
                           if self.pomiary.isAlive():
                                             print "wciaz zyje"
                                             self.pomiary.stop()
                  except:
                           pass                                             
                  self.pomiary=MyThread()
                  self.pomiary.start()
         def Przyjmij_Czas(self,event):
                  self.czas=self.entry0.get()         
                  
         def Przyjmij_Polecenie(self,event):
                  polecenie_do_wyslania=self.entry2.get()
                  print polecenie_do_wyslania
                  # self.Sprawdz_czy_mozna_wysylac()
                  # ser.setRTS(1)
                  ser.write(polecenie_do_wyslania+"\n")
                  pass
                  pass
                  ser.setRTS(0)
         def Przyjmij_Polecenie2(self,event):
                  polecenie_do_wyslania=self.entry3.get()
                  print polecenie_do_wyslania
                  self.Sprawdz_czy_mozna_wysylac()
                  ser.setRTS(1)
                  ser.write(polecenie_do_wyslania+"\n")
                  pass
                  pass
                  ser.setRTS(0)
                  
         def Przyjmij_Polecenie3(self,event):
                  polecenie_do_wyslania=self.entry4.get()
                  print polecenie_do_wyslania
                  self.Sprawdz_czy_mozna_wysylac()
                  ser.setRTS(1)
                  ser.write(polecenie_do_wyslania+"\n")
                  pass
                  pass
                  ser.setRTS(0)                  
if __name__=="__main__":    
         
      
         
         ser=serial.Serial(port=3,baudrate=19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,rtscts=0,xonxoff=0,timeout=3000,writeTimeout=50)
         #19200
         log=open("log","w",12)
         
         ser.setRTS(1)#ustawiam RTS na 5V tzn na        
         root = Tkinter.Tk()
         myapp = MyApp(root)
         #root.after(100,dane_z_portu)
         root.mainloop()
      
