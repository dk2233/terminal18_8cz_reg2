
;jezeli ostatni kanal to wyslij wszystkie, jezeli nie ostatni to zmierz kolejny
        
        movf    czy_reguluje2,w
        btfsc   STATUS,Z
        goto    sprawdz_czy_mam_dalej_mierzyc
         
         movf      ktory_czujnik_reguluje2,w
         cpfseq    ktory_kanal
         goto      sprawdz_czy_mam_dalej_mierzyc
         
         
        ;jezeli jest 1 
         movf     czy_reguluje2,w
         xorlw    1
         btfsc    STATUS,Z
         goto     procedura_regulacji_dwu_grzanie2
         
         
         ;jezeli jest 1 
         movf     czy_reguluje2,w
         xorlw    2
         btfsc    STATUS,Z
         goto     procedura_regulacji_dwu_cool2
         
          
         
         
         
         
         
         
procedura_regulacji_dwu_grzanie2         
         
         
         
         movf     jaka_wartosc_regulujeH2,w
         ;pomiarh - jaka_wartosc_regulujeH
         subwf    pomiarH,w
;sprawdz czy to samo czy wieksze
         btfsc    STATUS,Z
         goto     sa_rowne_sprawdz_Lbajt2
         btfss    STATUS,C 
         goto     zalacz_grzanie2
;tzn reguluj<pomiaru w starszym bajcie wiec wylacz grzanie
         bsf      markers_regulacja,wylacz_moc2
         goto     sprawdz_czy_mam_dalej_mierzyc
         
zalacz_grzanie2    
;jezeli jakikolwiek pomiar wykazal ze trzeba wylaczyc to nie wlaczaj grzania
;        
         btfss    markers_regulacja,wylacz_moc2
         bsf      markers_regulacja,zalacz_moc2
         
         goto     sprawdz_czy_mam_dalej_mierzyc

                           
sa_rowne_sprawdz_Lbajt2

         btfsc    port_triak,triak2
         goto     regulacja_dwu_moc_ON2
         
         
regulacja_dwu_moc_OFF2         
         ;je¿eli moc jest wy³¹czona w tej chwili to w³¹cz j¹ dopiero gdy 
         ;pomiar bêdzie mniejszy ni¿ temperatura zadana 
         
         ;histereza dolna
         movf     histereza_R2_2,w
         subwf     jaka_wartosc_regulujeL2,w
             
         
         subwf    pomiarL,w
;sprawdz czy to samo czy wieksze
         btfsc    STATUS,Z
         goto     zalacz_grzanie2
         
         
; je¿eli po odjêciu nie ma C w Statusie, tzn ¿e pomiarL < pomiaru-histerezy
         
         btfss    STATUS,C 
         goto     zalacz_grzanie2
;tzn reguluj>pomiaru w mlodszym bajcie wiec wlacz grzanie
         bsf      markers_regulacja,wylacz_moc2
         goto     sprawdz_czy_mam_dalej_mierzyc
         
         
regulacja_dwu_moc_ON2
         ;je¿eli moc jest w³¹czona w tej chwili to wy³¹cz j¹ dopiero gdy 
         ;pomiar bêdzie wiêkszy ni¿ temperatura zadana + histereza zadana
         
         ;histereza górna
         movf     histereza_R2_1,w
         addwf    jaka_wartosc_regulujeL2,w
         
         ; w WREG jest wartosc  histereza + ustawienie wartosci regulacji
         
       
         subwf    pomiarL,w  
         ;w WREG  jest wartosc   pomiarL  -  (histereza + ustawienie wartosci )
;sprawdz czy to samo czy wieksze
         btfsc    STATUS,Z
         goto     regulacja_dwu_moc_ON_wylacz2

         
         
         ;C pojawia sie tylko gdy 
         
         btfss    STATUS,C 
         goto     zalacz_grzanie2
;tzn reguluj<pomiaru w mlodszym bajcie wiec wylacz grzanie

regulacja_dwu_moc_ON_wylacz2
         bsf      markers_regulacja,wylacz_moc2
         goto     sprawdz_czy_mam_dalej_mierzyc                         
sa_rowne_nic_nie_rob2
         goto     zalacz_grzanie2    
         
         
         ;goto     sprawdz_czy_mam_dalej_mierzyc       

         




         
procedura_regulacji_dwu_cool2
;tutaj zakladam ze dzialanie regulacji jest na chlodzenie

;tzn jesli temperatura jest powyzej wartosci zadanej to uruchom 
;wentylator         
         
         movf     jaka_wartosc_regulujeH2,w
         ;pomiarh - jaka_wartosc_regulujeH
         subwf    pomiarH,w
;sprawdz czy to samo czy wieksze
         btfsc    STATUS,Z
         goto     sa_rowne_sprawdz_Lbajt_cool2
         
         ;jesli jest wylaczony C
         ;tzn ze 
         ;pomiarH  - jaka_wartosc_regulujeH1  
         ;jesli C jest ustawione
         ;to pomiarH> jaka_wartosc_regulujeH1
         btfsc    STATUS,C 
         goto     zalacz_chlodzenie2
;tzn reguluj<pomiaru w starszym bajcie wiec wylacz grzanie
         bsf      markers_regulacja,wylacz_moc2
         goto     sprawdz_czy_mam_dalej_mierzyc
         
zalacz_chlodzenie2
;jezeli jakikolwiek pomiar wykazal ze trzeba wylaczyc to nie wlaczaj grzania
;        
         btfss    markers_regulacja,wylacz_moc2
         bsf      markers_regulacja,zalacz_moc2
         
         goto     sprawdz_czy_mam_dalej_mierzyc

                           
sa_rowne_sprawdz_Lbajt_cool2
;tak samo
         ;movf     histereza,w
         ;sprawdz czy moc wylaczona - jezeli tak to wlacz 1  stopien nizej czyli 4 nizej
;jezeli jest wlaczona energia to dodaj wartosc histerezy tj wylacza pozniej
         ;btfsc    latch_moc,lampka2
         btfsc    port_triak,triak2
         goto     regulacja_dwu_moc_cool_ON2
         
         
regulacja_dwu_moc_cool_OFF2        
         ;je¿eli moc jest wy³¹czona w tej chwili to w³¹cz j¹ dopiero gdy 
         ;pomiar bêdzie wiekszy ni¿ temperatura zadana 
         
         ;histereza dolna
         ;jezeli ustawilem chlodzenie po 
         ;temp 40
         ;histereza 0,5 st
         ;to wlacz dopiero jesli temp wzrosnie powyzej 40,5
         movf     histereza_R2_1,w
         addwf     jaka_wartosc_regulujeL2,w
             
         
         subwf    pomiarL,w
;sprawdz czy to samo czy wieksze
         btfsc    STATUS,Z
         goto     zalacz_chlodzenie2
         
         ;pomiarL - jaka_wartosc_regulujeL1
; je¿eli po odjêciu jest C w Statusie, tzn ¿e pomiarL > pomiaru+histerezy
         
         btfsc    STATUS,C 
         goto     zalacz_chlodzenie2
;tzn reguluj>pomiaru w mlodszym bajcie wiec wlacz grzanie
         bsf      markers_regulacja,wylacz_moc2
         goto     sprawdz_czy_mam_dalej_mierzyc
         
         
regulacja_dwu_moc_cool_ON2
         ;je¿eli moc jest w³¹czona w tej chwili to wy³¹cz j¹ dopiero gdy 
         ;pomiar bêdzie mniejszy ni¿ temperatura zadana - histereza zadana
         
         ;histereza dolna
         ;
         movf     histereza_R2_2,w
         subwf    jaka_wartosc_regulujeL2,w
         
         ; w WREG jest wartosc  histereza - ustawienie wartosci regulacji
         ;np 40 ustawiona
         ;40 - 0,5 (histereza)
       
         subwf    pomiarL,w  
         ;w WREG  jest wartosc   pomiarL  -  ( ustawienie wartosci -histereza )
;sprawdz czy to samo czy wieksze, jesli jest wieksze to C ustawione
         btfsc    STATUS,Z
         goto     regulacja_dwu_moc_ON_wyl_cool2

         ;jesli pomiarL < ust_warto   ->  C nie ustawione
         
         btfsc    STATUS,C 
         goto     zalacz_chlodzenie2
;tzn reguluj<pomiaru w mlodszym bajcie wiec wylacz grzanie

regulacja_dwu_moc_ON_wyl_cool2
         bsf      markers_regulacja,wylacz_moc1
         goto     sprawdz_czy_mam_dalej_mierzyc                         
         

         goto     zalacz_chlodzenie2
         ;goto     procedura_regulacji_dwu_2       




