import json
import requests
import bs4 as bs
import urllib.request
import schedule
import time
import datetime

sauce = [urllib.request.urlopen('https://salvator.net/vp/f2/subst_001.htm').read(), urllib.request.urlopen('https://salvator.net/vp/f2/subst_002.htm').read(), urllib.request.urlopen('https://salvator.net/vp/f2/subst_003.htm').read(), urllib.request.urlopen('https://salvator.net/vp/f2/subst_004.htm').read()]
#sauce = [urllib.request.urlopen('https://salvator.net/vp/f1/subst_001.htm').read(), urllib.request.urlopen('https://salvator.net/vp/f1/subst_002.htm').read(), urllib.request.urlopen('https://salvator.net/vp/f1/subst_003.htm').read(), urllib.request.urlopen('https://salvator.net/vp/f1/subst_004.htm').read()]


ChatURL = "1389299666:AAHffghldF4UPYo58RId44np__-H-6nJnlY"
URL = "https://api.telegram.org/bot{}/".format(ChatURL)
#chat_id = [1275311841, -1001352186886, 502872089]
#chat_id = [-1001262651312, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777, -1001428822777]                                                                                  #Chat IDs zu allen Klassen(stufen)
chat_id = [-1001470454981, -1001226654660, -1001171531731, -1001362114793, -1001226293377, -1001376765426, -1001429436458, -1001413395339, -1001390722825, -1001483677088, -1001285559096, -1001424888279, -1001213070159, -1001432171745, -1001449678976, -1001390488865, -1001395192746, -1001191865475]



def scan():
    m = 0
    soup1 = bs.BeautifulSoup(sauce[0], 'lxml')
    soup2 = bs.BeautifulSoup(urllib.request.urlopen('https://salvator.net/vp/ticker.htm').read(), 'lxml')
    div = str(soup1.find_all('div'))
    div = div.split(')')
    div2 = div[0].split('>')
    div1 = div[0].split(' ')

    textall = str(soup1.find_all('body'))
    text = textall.split('</p>')
    text = text[0].split('\n')
    div2 = div2[1].split(' ')
    print(text)

    if len(div1) == 7:
        seiten = int(div1[6]) - 1  # Div Container ausgelesen und zurechtkonvertiert (Seitenzahl ausgelesen)
        divdate = div2[1]
    else:
        seiten = 0
        divdate = div2[1].split('</div')
        divdate = divdate[0]

    ticker = str(soup2.find_all('marquee'))
    ticker = ticker.split('<')
    ticker = ticker[1].split('>')
    ticker = ticker[1]
    print(ticker)

    vp = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']                                       #Vertretungsplanplatzreservierungen
    klassen = ['12', '11', '10a', '10b', '10m', '10s', '9a', '9b', '9c', '9s', '8a', '8b', '8m', '8s', '7a', '7b', '7m', '7s'] #Klassen
    vobj = [open("12", 'w'), open("11", 'w'), open("10a", 'w'), open("10b", 'w'), open("10m", 'w'), open("10s", 'w'), open("9a", 'w'), open("9b", 'w'), open("9m", 'w'), open("9s", 'w'), open("8a", 'w'), open("8b", 'w'), open("8m", 'w'), open("8s", 'w'), open("7a", 'w'), open("7b", 'w'), open("7m", 'w'), open("7s", 'w')] #Dateien zum Öffnen vorbereiten
    aobj = open("Abwesenheit", 'w')
    atext = ''                                                                                                          #Abwesenheitplatzreservierung


    while m <= seiten:                                                                                                  #Tabellen auslesen


        print('Seite ' + str(m))
        soup = bs.BeautifulSoup(sauce[m], 'lxml')
        vtable = soup.find_all('table')
        if m == 0:
            aobj.write('Vertretungsplan für ' + divdate + ' den ' + div2[0] + '\n')
            atext += 'Vertretungsplan für ' + divdate + ' den ' + div2[0] + '\n'
            aobj.write(text[2] + '\n' + '\n')
            atext += text[2] + '\n' + '\n'
        for table in vtable:
            table_rows = table.find_all('tr')
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]

                if row != []:                                                                                           #Abwesende Lehrer & Klassen (In Klassenplatzhalter und Datei schreiben)
                    if row[0] == 'Abwesende Lehrer\xa0' and m == 0:
                        abwesenheit = str('Abwesende Lehrer: \n' + str(row[1]) + '\n' + '\n')
                        aobj.write(abwesenheit)
                        atext += abwesenheit
                    elif row[0] == 'Abwesende Klassen\xa0' and m == 0:
                        abwesenheit = str('Abwesende Klassen: \n' + str(row[1]))
                        aobj.write(abwesenheit)
                        atext += abwesenheit


                    elif row[1] != '\xa0':                                                                              #Vertretungsplan (In Klassenplatzhalter und Datei schreiben)
                        f12 = 0
                        v12 = 0
                        f10 = 0
                        v10 = 0
                        f9 = 0
                        v9 = 0
                        f8 = 0
                        v8 = 0
                        f7 = 0
                        v7 = 0

                        for Klassenstufe in range(0, 18):
                            if row[1] == klassen[Klassenstufe] and row[1]:
                                if row[5] == '---':
                                    vertretung = str(str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | FREI' + "\n")
                                    vobj[Klassenstufe].write(vertretung)
                                    vp[Klassenstufe] += vertretung
                                else:
                                    vertretung = str(
                                        str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | Vertreter(in): ' + str(
                                            row[4]) + ' | Raum: ' + str(row[5]) + "\n")
                                    vobj[Klassenstufe].write(vertretung)
                                    vp[Klassenstufe] += vertretung

                            elif row[1] == '11, 12':                                                                    #Sonderfall: zusammengelegte Kurse
                                if row[5] == '---':
                                    vertretung = str(str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | FREI' + "\n")
                                    #for zehnte in range(2, 4):
                                    if f12 == 0:
                                        vobj[0].write(vertretung)
                                        vp[0] += vertretung
                                        vobj[1].write(vertretung)
                                        vp[1] += vertretung
                                        f12 += 1
                                else:
                                    vertretung = str(
                                        str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | Vertreter(in): ' + str(
                                            row[4]) + ' | Raum: ' + str(row[5]) + "\n")
                                    if v12 == 0:
                                        vobj[0].write(vertretung)
                                        vp[0] += vertretung
                                        vobj[1].write(vertretung)
                                        vp[1] += vertretung
                                        v12 += 1

                            elif row[1] == '10a, 10b, 10m':                                                             #Sonderfall: zusammengelegte Kurse
                                if row[5] == '---':
                                    vertretung = str(str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | FREI' + "\n")
                                    #for zehnte in range(2, 4):
                                    if f10 == 0:
                                        vobj[2].write(vertretung)
                                        vp[2] += vertretung
                                        vobj[3].write(vertretung)
                                        vp[3] += vertretung
                                        vobj[4].write(vertretung)
                                        vp[4] += vertretung
                                        f10 += 1
                                else:
                                    vertretung = str(
                                        str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | Vertreter(in): ' + str(
                                            row[4]) + ' | Raum: ' + str(row[5]) + "\n")
                                    #for zehnte in range(2, 4):
                                    if v10 == 0:
                                        vobj[2].write(vertretung)
                                        vp[2] += vertretung
                                        vobj[3].write(vertretung)
                                        vp[3] += vertretung
                                        vobj[4].write(vertretung)
                                        vp[4] += vertretung
                                        v10 += 1

                            elif row[1] == '9a, 9b, 9m' or row[1] == '9a, 9b, 9c':
                                if row[5] == '---':
                                    vertretung = str(str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | FREI' + "\n")
                                    #for zehnte in range(6, 8):
                                    if f9 == 0:
                                        vobj[6].write(vertretung)
                                        vp[6] += vertretung
                                        vobj[7].write(vertretung)
                                        vp[7] += vertretung
                                        vobj[8].write(vertretung)
                                        vp[8] += vertretung
                                        f9 += 1
                                else:
                                    vertretung = str(
                                        str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | Vertreter(in): ' + str(
                                            row[4]) + ' | Raum: ' + str(row[5]) + "\n")
                                    #for zehnte in range(6, 8):
                                    if v9 == 0:
                                        vobj[6].write(vertretung)
                                        vp[6] += vertretung
                                        vobj[7].write(vertretung)
                                        vp[7] += vertretung
                                        vobj[8].write(vertretung)
                                        vp[8] += vertretung
                                        v9 += 1

                            elif row[1] == '8a, 8b, 8m':
                                if row[5] == '---':
                                    vertretung = str(str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | FREI' + "\n")
                                    #for zehnte in range(9, 11):
                                    if f8 == 0:
                                        vobj[10].write(vertretung)
                                        vp[10] += vertretung
                                        vobj[11].write(vertretung)
                                        vp[11] += vertretung
                                        vobj[12].write(vertretung)
                                        vp[12] += vertretung
                                        f8 += 1
                                else:
                                    vertretung = str(
                                        str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | Vertreter(in): ' + str(
                                            row[4]) + ' | Raum: ' + str(row[5]) + "\n")
                                    #for zehnte in range(9, 11):
                                    if v8 == 0:
                                        vobj[10].write(vertretung)
                                        vp[10] += vertretung
                                        vobj[11].write(vertretung)
                                        vp[11] += vertretung
                                        vobj[12].write(vertretung)
                                        vp[12] += vertretung
                                        v8 += 1

                            elif row[1] == '7s1' or row[1] == '7s2' or row[1] == '7s1, 7s2':
                                if row[5] == '---':
                                    vertretung = str(str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | FREI' + "\n")
                                    #for zehnte in range(9, 11):
                                    if f7 == 0:
                                        vobj[17].write(vertretung)
                                        vp[17] += vertretung
                                        f7 += 1

                                else:
                                    vertretung = str(
                                        str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | Vertreter(in): ' + str(
                                            row[4]) + ' | Raum: ' + str(row[5]) + "\n")
                                    #for zehnte in range(9, 11):
                                    if v7 == 0:
                                        vobj[17].write(vertretung)
                                        vp[17] += vertretung
                                        v7 += 1

                            elif row[1] == '8s1' or row[1] == '8s2' or row[1] == '8s1, 8s2':
                                if row[5] == '---':
                                    vertretung = str(str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | FREI' + "\n")
                                    #for zehnte in range(9, 11):
                                    if f7 == 0:
                                        vobj[13].write(vertretung)
                                        vp[13] += vertretung
                                        f7 += 1

                                else:
                                    vertretung = str(
                                        str(row[0]) + '. Stunde | Fach: ' + str(row[2]) + ' | Vertreter(in): ' + str(
                                            row[4]) + ' | Raum: ' + str(row[5]) + "\n")
                                    #for zehnte in range(9, 11):
                                    if v7 == 0:
                                        vobj[13].write(vertretung)
                                        vp[13] += vertretung
                                        v7 += 1

        m += 1
    else:
        for klasse in range(0, 18):                                                                                     #Dokumente spiechern und falls Platzhalter leer sein sollten: Keine weitereren Einträge
            if vp[klasse] == '':
                vp[klasse] = 'Keine weiteren Einträge'
                vobj[klasse].write('Keine weiteren Einträge')
            vobj[klasse].close()

        print(atext)
        aobj.close()
        print(vp)
                                                                                                                        #Vertretungsplan- und Abwesenheitplatzhalter zum Versand vorgereiten

        send_message(atext, vp, chat_id, ticker)

#m = 0

def get_url(urla, urlvp, urlt):
    responsea = requests.get(urla)
    responset = requests.get(urlt)
    responsevp = requests.get(urlvp)
    contenta = responsea.content.decode("utf8")
    contentt = responset.content.decode("utf8")
    contentvp = responsevp.content.decode("utf8")
    return contenta and contentt and contentvp

def send_message(atext, vp, chat_id, ticker):                                                                                   #Nachrichten versenden
    for klasse in range(0, 18):
        urla = URL + "sendMessage?text={}&chat_id={}".format(atext, chat_id[klasse])
        urlt = URL + "sendMessage?text={}&chat_id={}".format(ticker, chat_id[klasse])
        urlvp = URL + "sendMessage?text={}&chat_id={}".format(vp[klasse], chat_id[klasse])
        get_url(urla, urlvp, urlt)


schedule.every().monday.at("18:00").do(scan)
schedule.every().tuesday.at("18:00").do(scan)
schedule.every().wednesday.at("18:00").do(scan)
schedule.every().thursday.at("17:16").do(scan)
schedule.every().sunday.at("18:00").do(scan)



def schleife():
    
    while True:
        schedule.run_pending()
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(5)






schleife()
