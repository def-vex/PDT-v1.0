import os
import pprint
import subprocess
import colorama
import time
from time import sleep
import threading
import subprocess
import winsound
import datetime
import math

output = []
z = 0
avgPing = ""
pktSent = ""
pktRec = ""
pktLost = ""
started = False


def cls():
    os.system("cls")

def mainscreen():

    allServers = ["8.8.4.4", "8.8.8.8", "142.250.181.78", "75.2.105.73", "75.2.66.166", "1.0.0.1", "1.1.1.1", "208.67.222.222", "208.67.220.220"]

    server = "8.8.4.4"
    packetAmt = 4
    packetSize = "32"
    timeoutThresh = "4000"
    
    global pingLocal
    pingLocal = False

    global multipacketStream
    multipacketStream = False

    serverSel = 0
    
    choice = "-1"

    while choice not in ["1", "2", "3"]:
        cls()
        print("""
=======================================================
|           Ping Diagnostics Tool (PDT) v1.0          |
| 1) Start                                            |
| 2) Exit                                             |
| 3) Open Logs                                        |
|                     Made by VEX                     |
=======================================================
""")
        choice = input(">>> Choice: ")
        try:
            int(choice)
        except:
            cls()
            print("ERROR: Enter a valid choice in the integer format!")
            input("\nPress any key to go back...")

    option = "9"

    if choice == "2":
        quit()
    elif choice == "3":
        try:
            os.startfile("pdtLogs.txt")
            restart()
        except:     
            logsFile = os.open("pdtLogs.txt", os.O_CREAT|os.O_RDWR|os.O_APPEND)
            os.close(logsFile)
            os.startfile("pdtLogs.txt")
            restart()

    while choice == "1" and option != "7":
        cls()

        if multipacketStream == False:
            dispMP = "DISABLED"
        else:
            dispMP = "ENABLED"
        
        if pingLocal == False:
            dispLC = "DISABLED"
        else:
            dispLC = "ENABLED"

        serverSel = 0

        print(f"""
===================================================
|   Settings (Press ENTER for default settings)   |     
===================================================
 1) Select Server [{server}]                               
 2) Select Packets Amount [{packetAmt}]                           
 3) Multipacket Streaming ({dispMP})                  
 4) Packet Size [{packetSize}]                                     
 5) Ping localhost (::1) ({dispLC})                  
 6) Select Timeout Threshold [{timeoutThresh}]                        
 7) > Back <        
===================================================
| Type "0" to continue with the selected settings |        
===================================================  
""")
        option = input(">>> Select which setting to change (if any): ")
        cls()
        if option == "":
            return server, int(packetAmt), int(packetSize), int(timeoutThresh)
        elif option == "0":
            return server, int(packetAmt), int(packetSize), int(timeoutThresh)
        elif option == "1":
            while serverSel not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                
                if pingLocal == True:
                    cls()
                    print("ERROR: Server already set to localhost because PingLC is ENABLED! Disable it to set your specified server!")
                    input("\nPress ENTER to continue...")
                    break
                
                cls()
                print("""
===================================================
|                 Server Select                   |                                               
===================================================
 1) 8.8.4.4 (Google DNS)
 2) 8.8.8.8 (Google DNS)
 3) www.google.com
 4) VALORANT (Bahrain)
 5) VALORANT (Mumbai)
 6) 1.0.0.1 (Cloudflare)
 7) 1.1.1.1 (Cloudflare)
 8) 208.67.222.222 (OpenDNS)
 9) 208.67.220.220 (OpenDNS)
 10) Custom Server
===================================================
|   Type out the corresponding number to select   |        
===================================================
    """)
                serverSel = input(">>> Select option: ")

                if serverSel == "10":
                    cls()
                    cusServer = input(">>> Type out your specified server's address: ")
                    server = cusServer
                    break
                
                try:
                    serverSel = int(serverSel)
                    server = allServers[serverSel-1]
                    serverSel = str(serverSel)
                except ValueError:
                    cls()
                    print("ERROR: Input must be in integer form!")
                    input("\nPress ENTER to continue...")
                except IndexError:
                    cls()
                    print("ERROR: Something went wrong! Value must be out of range.")
                    input("\nPress ENTER to continue...")

        elif option == "2":
            cls()
            packetAmt = -1
            while packetAmt < 0 or packetAmt > 200:
                cls()
                try:
                    packetAmt = int(input(">>> Enter a value between 1 and 200: "))
                    if packetAmt > 0 and packetAmt <= 200:
                        print("New packet amount = {} pkts".format(packetAmt))
                        input("\nPress ENTER to continue...")
                    else:
                        cls()
                        print("ERROR: Value not in range!")
                        input("\nPress ENTER to continue...")
                except ValueError:
                    cls()
                    print("ERROR: Input must be in integer form!")
                    input("\nPress ENTER to continue...")
                except:
                    cls()
                    print("ERROR: Something went wrong!")
                    input("\nPress ENTER to continue...")
        
        elif option == "3":
            if packetAmt < 4:
                cls()
                print("ERROR: Multipacket streaming only available for packet amounts greater than or equal to 4!")
                input("\nPress ENTER to continue...")
            else:
                multipacketStream = not(multipacketStream)
        
        elif option == "4":
            cls()
            packetSize = -1
            while packetSize < 0 or packetSize > 1024:
                cls()
                try:
                    packetSize = int(input(">>> Enter a value between 1 and 1024: "))
                    if packetSize > 0 and packetSize <= 1024:
                        print("New packet size = {} bytes".format(packetSize))
                        input("\nPress ENTER to continue...")
                    else:
                        cls()
                        print("ERROR: Value not in range!")
                        input("\nPress ENTER to continue...")
                except ValueError:
                    cls()
                    print("ERROR: Input must be in integer form!")
                    input("\nPress ENTER to continue...")
                except:
                    cls()
                    print("ERROR: Something went wrong!")
                    input("\nPress ENTER to continue...")
        
                    
        elif option == "5":
            pingLocal = not(pingLocal)
            server = "127.0.0.1"
            
        elif option == "6":
            cls()
            timeoutThresh = -1
            while timeoutThresh < 0 or timeoutThresh > 10000:
                cls()
                try:
                    timeoutThresh = int(input(">>> Enter a value between 1 and 10000 (in ms): "))
                    if timeoutThresh > 0 and timeoutThresh <= 10000:
                        print("New timeout threshold = {} seconds".format(timeoutThresh/1000))
                        input("\nPress ENTER to continue...")
                    else:
                        cls()
                        print("ERROR: Value not in range!")
                        input("\nPress ENTER to continue...")
                except ValueError:
                    cls()
                    print("ERROR: Input must be in integer form!")
                    input("\nPress ENTER to continue...")
                except:
                    cls()
                    print("ERROR: Something went wrong!")
                    input("\nPress ENTER to continue...")
        
        elif option == "7":
            restart()
            return
    
def fetchData(outset):

    avpStr, avminStr, avmaxStr, avsStr, avrStr, avlStr = "", "", "", "", "", ""

    if multipacketStream == False:
        avgPing = ""
        minPing = ""
        maxPing = ""
        pktSent = ""
        pktRec = ""
        pktLost = ""
    else:
        
        avgPing = []
        minPing = []
        maxPing = []
        pktSent = []
        pktRec = []
        pktLost = []
    

    for x in outset:
        try:
            index = x.find("Average")
            for y in range(index+10, len(x)):
                try:
                    z = int(x[y])
                    avpStr += x[y]
                except:
                    break
            try:    
                avgPing.append(avpStr)
            except:
                1==1
        
        except:
            avgPing = "N/A"
        index = x.find("Sent")
        for y in range(index+7, len(x)):
            try:
                z = int(x[y])
                avsStr += x[y]
            except:
                break
        try:
            pktSent.append(avsStr)
        except:
            1==1
        
        index = x.find("Received")
        for y in range(index+11, len(x)):
            try:
                z = int(x[y])
                avrStr += x[y]
            except:
                break
        try:
            pktRec.append(avrStr)
        except:
            1==1
        
        index = x.find("Lost")
        for y in range(index+7, len(x)):
            try:
                z = int(x[y])
                avlStr += x[y]
            except:
                break
        try:
            pktLost.append(avlStr) 
        except:
            1==1
        
        try:
            index = x.find("Minimum")
            for y in range(index+10, len(x)):
                try:
                    z = int(x[y])
                    avminStr += x[y]     
                except:
                    break
            try:
                minPing.append(avminStr)
            except:
                1==1
        
        except:
            minPing = "N/A"
        try:        
            index = x.find("Maximum")
            for y in range(index+10, len(x)):
                try:
                    z = int(x[y])
                    avmaxStr += x[y]
                except:
                    break
            try:
                maxPing.append(avmaxStr)
            except:
                1==1
        
        except:
            maxPing = "N/A"

        if multipacketStream == False:
            avgPing = avpStr
            minPing = avminStr
            maxPing = avmaxStr
            pktSent = avsStr
            pktRec = avrStr
            pktLost = avlStr

        avpStr, avminStr, avmaxStr, avsStr, avrStr, avlStr = "", "", "", "", "", ""

    return avgPing, minPing, maxPing, pktSent, pktRec, pktLost

def ping(server:str, packetAmt:int, packetSize:int, timeoutThresh:int):

    global outset

    outset = []

    print(server, packetAmt, packetSize, timeoutThresh)

    beep(False)

    if multipacketStream == False:
        proc = subprocess.Popen((f"ping {server} -n {packetAmt} -l {packetSize} -w {timeoutThresh}"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        proc = subprocess.Popen((f"ping {server} -n {packetAmt} -l {packetSize} -w {timeoutThresh}"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        output = out.decode("utf-8")
        output = str(output)
        outset.append(output)

        if output.find("Ping request could not find host") != -1:
            sleep(1)
            cls()
            print("ERROR: Host not found! Try a valid host next time!")
            input("\nPress any key to go back...")
            restart()
            return 

    else:
        if packetAmt < 1:
            proc = subprocess.Popen((f"ping {server} -n {packetAmt} -l {packetSize} -w {timeoutThresh}"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            output = out.decode("utf-8")
            output = str(output)
            outset.append(output)

            if output.find("Ping request could not find host") != -1:
                sleep(1)
                cls()
                print("ERROR: Host not found! Try a valid host next time!")
                input("\nPress any key to go back...")
                restart()
                return
        
        else:
            if packetAmt%4 != 0:
                packetRem = packetAmt - 3*(packetAmt//4)
            else:
                packetRem = packetAmt//4
            packetAmt = packetAmt//4
            proc1 = subprocess.Popen((f"ping {server} -n {packetAmt} -l {packetSize} -w {timeoutThresh}"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc2 = subprocess.Popen((f"ping {server} -n {packetAmt} -l {packetSize} -w {timeoutThresh}"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc3 = subprocess.Popen((f"ping {server} -n {packetAmt} -l {packetSize} -w {timeoutThresh}"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc4 = subprocess.Popen((f"ping {server} -n {packetRem} -l {packetSize} -w {timeoutThresh}"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out1, err1 = proc1.communicate()
            out2, err2 = proc2.communicate()
            out3, err3 = proc3.communicate()
            out4, err4 = proc4.communicate()
            out1 = out1.decode("utf-8")
            out2 = out2.decode("utf-8")
            out3 = out3.decode("utf-8")
            out4 = out4.decode("utf-8")
            outset.append(str(out1))
            outset.append(str(out2))
            outset.append(str(out3))
            outset.append(str(out4))

            if out1.find("Ping request could not find host") != -1:
                sleep(1)
                cls()
                print("ERROR: Host not found! Try a valid host next time!")
                input("\nPress any key to go back...")
                restart()
                return

    avgPing, minPing, maxPing, pktSent, pktRec, pktLost = fetchData(outset)

    parser(avgPing, minPing, maxPing, pktSent, pktRec, pktLost)

def beep(audioPlay):

    if audioPlay == False:
        winsound.PlaySound("start.wav", winsound.SND_FILENAME)
    elif audioPlay == True:
        winsound.PlaySound("end.wav", winsound.SND_FILENAME)

def loadingScr():

    loadSym = ["-", "\\", "|", "/"]

    while outset == []:
        for x in range(0, 4):
            cls()
            print("Loading...[{}]".format(loadSym[x]))
            print("""\n
>>> Settings Used <<<

Server pinged = {}
Packet Amount = {}
Packet Size = {} bytes
Timeout Threshold = {}ms

>>> Kill yourself <<<
            """.format(server, packetAmt, packetSize, timeoutThresh))
            sleep(0.2)
            if outset != []:
                cls()
                break
            

def parser(avgPing, minPing, maxPing, pktSent, pktRec, pktLost):
    
    global connIssue
    connIssue = False

    if multipacketStream == True:

        totalavPing, totalminPing, totalmaxPing, totalpktSent, totalpktRec, totalpktLost = 0, 0, 0, 0, 0, 0
        
        failedAv, failedMin, failedMax = 0,0,0

        for x in avgPing:
            try:
                totalavPing += int(x)
            except:
                totalavPing = totalavPing
                failedAv += 1
        for x in minPing:
            try:
                totalminPing += int(x)
            except:
                totalminPing = totalminPing
                failedMin += 1
        for x in maxPing:
            try:
                totalmaxPing += int(x)
            except:
                totalmaxPing = totalmaxPing
                failedMax += 1
        for x in pktSent:
            totalpktSent += int(x)
        for x in pktRec:
            totalpktRec += int(x)
        for x in pktLost:
            totalpktLost += int(x)

        pktSent, pktRec, pktLost = totalpktSent, totalpktRec, totalpktLost
        
        avgPing, minPing, maxPing = totalavPing//(4-failedAv), totalminPing//(4-failedMin), totalmaxPing//(4-failedMax)
        
    try:
        maxPing = int(maxPing)
        minPing = int(minPing)
        avgPing = int(avgPing)
    except:
        maxPing = "N/A"
        minPing = "N/A"
        avgPing = "N/A"

    try:
        if pingLocal == False:
            pingDev = str(round((((maxPing-minPing)/((maxPing+minPing)/2))*100), 2)) + "%"
        else:
            pingDev = "Should be 0%, you're literally pinging yourself LMFAO"
    except:
        pingDev = "N/A"
    
    for x in outset:
        if x.find("PING: transmit failed. General failure.") != -1:
            connIssue = True
        else:
            connIssue = False

    cls()

    beep(True)

    print("====================================================")
    print("|                      REPORT                      |")
    print("====================================================")
    if pingLocal == True:
        print("[NOTICE] You had PingLC ENABLED!")
    if connIssue == True:
        print("[WARNING] Ping transmission completely failed at some points or throughout execution! You may want to check your internet connection!")
    print()
    print("Ping:", avgPing)
    print("Maximum Ping:", maxPing)
    print("Minimum Ping:", minPing)
    print("Ping Deviation:", pingDev)
    print("Packets Sent:", pktSent)
    print("Packets Recieved:", pktRec)
    print("Packets Lost:", pktLost)
    print("Packet Loss:", str(round((int(pktLost)/int(pktSent))*100, 2)) + "%")
    
    try:
        if int(avgPing) < 20:
            pingStatus = "Excellent"
        elif int(avgPing) < 40:
            pingStatus = "Good"
        elif int(avgPing) < 60:
            pingStatus = "Satisfactory"
        else:
            pingStatus = "Bad"
        
        if (int(pktLost)/int(pktSent))*100 < 2.5:
            pktStatus = "Excellent"
        elif (int(pktLost)/int(pktSent))*100 < 4:
            pktStatus = "Good"
        elif (int(pktLost)/int(pktSent))*100 < 10:
            pktStatus = "Satisfactory"
        else:
            pktStatus = "Bad"
    except:
        pingStatus = "N/A"
        pktStatus = "N/A"

    try:
        
        pingDev = float(pingDev.strip("%"))

        if pingDev < 10:
            devStatus = "No real ping spikes detected!"
        elif pingDev < 20:
            devStatus = "There might be some spikes but not of great magnitude."
        elif pingDev < 30:
            devStatus = "Ping spikes detected but are not of concering magnitude."
        elif pingDev < 50:
            devStatus = "Ping spikes detected, might prove to be annoying."
        else:
            devStatus = "Ping spikes of concerning magnitude detected."
    except:
        devStatus = "N/A"

    print()
    print("====================================================")
    print("|                     PDT v1.0                     |")
    print("====================================================")
    print()
    input(">>> Press any key to continue and see our diagnosis... ")

    cls()

    print("====================================================")
    print("|                     DIAGNOSIS                    |")
    print("====================================================")
    print()
    print("Ping status:", pingStatus)
    print("Packet transmission status:", pktStatus)
    print("Report on any ping spikes:", devStatus)
    print()
    print("====================================================")
    print('|Enter "SAVE" to save this diagnosis in pdtLogs.txt|')
    print("====================================================")
    print()
    print("[If you don't want to save, press ENTER or any other key to continue]")
    print()
    repeat = input('>>> ')
    
    
    if repeat.lower() == "save":
        toWrite = f"""
[{datetime.datetime.utcnow()}] : [{server}]
Average Ping:     {avgPing}ms
Minimum Ping:     {minPing}ms
Maximum Ping:     {maxPing}ms
Ping Deviation:   {str(pingDev).strip("%")}%
Packets Sent:     {pktSent} 
Packets Received: {pktRec} 
Packets Lost:     {pktLost}
Packet Loss:      {round((int(pktLost)/int(pktSent))*100, 2)}%
        """
        logsFile = os.open("pdtLogs.txt", os.O_CREAT|os.O_RDWR|os.O_APPEND)
        os.write(logsFile, bytes(toWrite, "utf-8"))
        os.close(logsFile)

    restart()
    cls()

def restart():
    import sys
    import os
    os.execv(sys.executable, ['python3'] + sys.argv)

if __name__ == '__main__':
    for loops in range(2):
        if loops == 1:
            threading.Thread(target = ping, args=(server, packetAmt, packetSize, timeoutThresh)).start()
            threading.Thread(target = loadingScr).start()
        else:
            server, packetAmt, packetSize, timeoutThresh = mainscreen()