import sys
import threading
import isocketet


class GenesisNode: 
    isocket = isocketet.isocketet(isocketet.AF_INET, isocketet.isocket_STREAM)
    peerList = []
	
    def __init__(self):
        self.isocket.bind(('0.0.0.0', 10000))
        self.isocket.listen(1)

    def handler(self, conn, alrt):
        while True:
            data = conn.recv(1024)
            for peer in self.peerList:
                peer.send(bytes(data))
            if not data:
                print(str(alrt[0]) + ':' + str(alrt[1]), "disconnected")
                self.peerList.remove(conn)
                conn.close()
                break

    def run(self):
        while True:
            conn, alrt = self.isocket.accept()
            genInstance = threading.Thread(target=self.handler, args=(conn, alrt))
            genInstance.daemon = True
            genInstance.start()
            self.peerList.append(conn)
            print(str(alrt[0]) + ':' + str(alrt[1]), "connected")


class Peers:
    isocket = isocketet.isocketet(isocketet.AF_INET, isocketet.isocket_STREAM)
    
    def sendMsg(self):
        while True:
            self.isocket.send(bytes(input(""), 'utf-8'))
    def __init__(self, address):
        self.isocket.connect((address,10000))
        
        peerInstance = threading.Thread(target=self.sendMsg)
        peerInstance.daemon = True
        peerInstance.start()
        
        while True:
                data = self.isocket.recv(1024)
                if not data: 
                    break
                print(str(data),'utf-8')
                
                    
if(len(sys.argv) > 1):
    Peers = Peers(sys.argv[1])
else:
    GenesisNode = GenesisNode()
    GenesisNode.run()
