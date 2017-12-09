;w  przypadku testowania regulatora

;to mo¿na dodaæ na koncu pliku

goto     test_koniec
;w przyadku testowania

         movlw    dane_odebraneL
         movwf    FSR0L
         movlw    dane_odebraneH
         movwf    FSR0H
         
        
        movlw      HIGH(tab_test)
        movwf     PCLATH
test_petla        
         
         
        
        ;movf      PCLATH,w,0
         movf     tmp,w
         call     tab_test
         
         
         
         movwf    INDF0
         xorlw    0
         btfsc    STATUS,Z
         goto     test_regulator
         incf     tmp,f
         incf     tmp,f
         incf     FSR0L,f
         goto     test_petla
         
         
tab_test
         addwf    PCL,f
         ;retlw    0x2a
         
         ;retlw    0x43
         ;retlw    0x46
         ;retlw    0x0d
         retlw    _star
         ;retlw    _wiekszosci
         ;retlw    _P     
         retlw    _p
         ;retlw    _1
         
         retlw    0x30
         ;retlw    _
         
         ;retlw    _F
         ;retlw    _
         ;retlw    _F
         retlw    0x32
         ;retlw    _kropka
         retlw    0x30
         retlw    0x36
         ;retlw    _e
         ;retlw    0x34
         ;retlw    0x30
         ;retlw    _A
         ;retlw    0x30
         ;retlw    0x37
         retlw    0
         
         
test_regulator
      ;bsf      markers2,sprawdz_odebrane
         ;goto     test_koniec
         
         movlw    1
         movwf    ile_kanalow
         
         movlw    0
         movwf    ktory_kanal_mierze
         
         ;movwf     ktore_dzielenie_przez2
         
         movlw    0x01
         movwf    jak_duzo_probek
         
         movlw    0x04
         movwf    odstep_pomiarowy
         movlw    0x04
        movwf    aktualny_odstep
         
         
         bsf       markers,czy_usrednianie
         bsf      markers2,pomiary
         bsf      markers,pomiary_zrobione
         bsf      markers,czy_wyswietlam_temp
         ;
         movlw    0x01
         movwf    ADCON0   
               
         movlw    0xf
         movwf    odebrano_liter
         movlw    0xff
         movwf    linia1
         movlw    0xf0
         movwf    linia2
         movlw    0x11
         movwf    znaczniki
         
         