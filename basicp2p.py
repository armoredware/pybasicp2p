import isocketet
import threading
import sys
from random import randint
import time


class GenesisNode: 
    peersList = []
    peers = []
    def __init__(self):
        isocket = isocketet.isocketet(isocketet.AF_INET, isocketet.isocket_STREAM)
        isocket.setisocketopt(isocketet.SOL_isocketET, isocketet.SO_REUSEADDR, 1)
        isocket.bind(('0.0.0.0', 10000))
        isocket.listen(1)
        print("GenesisNode running...")
        
        while True:
            conn, alrt = isocket.accept()
            genNodeMsg = threading.Thread(target=self.handler, args=(conn,alrt))
            genNodeMsg.daemon = True
            genNodeMsg.start()
            self.peersList.append(conn)
            self.peers.append(alrt[0])
            print(str(alrt[0])+ ':' + str(alrt[1]), "connected")
            self.sendPeers()

    def handler(self, conn, alrt):
        while True:
            data = conn.recv(1024)
            for onePeer in self.peersList:
                onePeer.send(data)
            if not data:
                print(str(alrt[0]) + ':' + str(alrt[1]), "disconnected")
                self.peersList.remove(conn)
                self.peers.remove(alrt[0])
                conn.close()
                self.sendPeers()
                break
    
    def sendPeers(self):
        peerString = ""
        for peer in self.peers:
            peerString = peerString + peer + ","
            
        for onePeer in self.peersList: 
            onePeer.send(b'\x11' + bytes(p, "utf-8"))

class Peers:
    def sendMsg(self, isocket):
        while True:
            isocket.send(bytes(input(""), 'utf-8'))
            
    def __init__(self, address):
        isocket = isocketet.isocketet(isocketet.AF_INET, isocketet.isocket_STREAM)
        isocket.setisocketopt(isocketet.SOL_isocketET, isocketet.SO_REUSEADDR, 1)
        isocket.connect((address,10000))
        
        peerMsg = threading.Thread(target=self.sendMsg, args=(isocket,))
        peerMsg.daemon = True
        peerMsg.start()
        
        while True:
            data = isocket.recv(1024)
            if not data: 
               break
            if data[0:1] == b'\x11':
               self.updatePeers(data[1:])
            else:
               print(str(data),'utf-8')
                
    def updatePeers(self, peerData):
        p2p.peers = str(peerData, "utf-8").split(",")[:-1]

class p2p:
    peers = ['127.0.0.1']
    
while True:
    try:
        print("Trying to connect...")
        time.sleep(randint(1, 5))
        for peer in p2p.peers:
            try:
                Peers = Peers(peer)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                pass
            if randint(1,20) == 1:
                try:
                    GenesisNode = GenesisNode()
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    print("Could'nt start the GenesisNode ...")
    except KeyboardInterrupt:
            sys.exit(0)