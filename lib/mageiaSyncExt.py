# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 21:42:56 2014

@author: yves
"""

import re, os

from subprocess import Popen, PIPE
from PyQt5 import QtCore

class checkThread(QtCore.QThread):
    md5Signal = QtCore.pyqtSignal(int)
    sha1Signal= QtCore.pyqtSignal(int)
    dateSignal=QtCore.pyqtSignal(int)
    checkStartSignal=QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(checkThread, self).__init__(parent)

    def processSum(self,sumType):
        import hashlib
        if sumType=='sha1':
            hashfunc = hashlib.sha1()
        if sumType=='md5':
            hashfunc = hashlib.md5()
        try:
            with open(self.destination+'/'+self.path+'/'+self.name, 'rb') as f:
                while True:
                    block = f.read(2**10) 
                    if not block: break
                    hashfunc.update(block)
                sumcalc=hashfunc.hexdigest()
        except:
            return False
        try:
            fs=open(self.destination+'/'+self.path+'/'+self.name+'.'+sumType,'r')
        except:
            #   reference file not found
            return False
        sumcheck=(fs.readline()).split()[0]
        if sumcalc==sumcheck:
            return True
        return False
        
    def processDate(self):
#        import  datetime as datetime
#        try:
#            dateFile=open(str(self.destination)+'/DATE.txt','r')
#        except:
#            return False
#        refDate=dateFile.readline()
#        info=os.path.getmtime(str(self.destination)+'/'+self.name)
#        fileDate= (datetime.fromtimestamp(info)).strftime("%c")
#        if (fileDate==refDate):
#            return True
#        else:
        return False
        
    def setup(self, destination, path,name,isoIndex):
        self.destination=destination
        self.path=path
        self.name=name
        self.isoIndex=isoIndex
        
    def run(self):
        signal=500+self.isoIndex
        self.checkStartSignal.emit(signal)
        checkMd5=self.processSum('md5')
        self.md5Signal.emit(self.isoIndex+128*checkMd5)
        signal=400+self.isoIndex
        self.checkStartSignal.emit(signal)
        checkSha1=self.processSum('sha1')
        self.sha1Signal.emit(self.isoIndex+128*checkSha1)
        signal=300+self.isoIndex
        self.checkStartSignal.emit(signal)
        checkDate=self.processDate()
        self.dateSignal.emit(self.isoIndex+128*checkDate)
        self.quit()
        

class syncThread(QtCore.QThread):
    progressSignal = QtCore.pyqtSignal(int)
    speedSignal= QtCore.pyqtSignal(int)
    endSignal=QtCore.pyqtSignal(int)
    remainSignal=QtCore.pyqtSignal(str)
    checkSignal=QtCore.pyqtSignal(int)
    lvM=QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(syncThread, self).__init__(parent)
        self.stopped=False
        self.list=[]

    def setup(self,nameWithPath, destination,row,):
        #   row is the index in 'model'
        iso={'nameWithPath':str(nameWithPath),'destination':str(destination),'row':row}
        self.list.append(iso)

    def params(self, password, bwl):
        self.password=password
        self.bwl=bwl    #   Bandwith limit
        
    def stop(self):
        self.lvM.emit("Process rsync stopped")
        self.stopped=True
        try:
            self.process.terminate()
        except:
            print "Echec"
            pass
        # Init progressbar and speed counter
        self.endSignal.emit(0)
        
    def run(self):
        if len(self.list)==0:
            self.lvM.emit("No entry selected")
        for iso in self.list:
            errorOccured=True
            self.lvM.emit("Starting rsync with "+iso['nameWithPath'])
            if self.bwl!=0:
                commande=['rsync','-avHP',"--bwlimit="+str(self.bwl), iso['nameWithPath'], iso['destination']]
            else:
                commande=['rsync','-avHP', iso['nameWithPath'], iso['destination']]
            print commande
            try:
                if self.password != "":
                    envir = os.environ.copy()
                    envir['RSYNC_PASSWORD']=str(self.password)
                    self.process = Popen(commande, shell=False, stdout=PIPE, stderr=PIPE, env=envir)
                else:
                    self.process = Popen(commande, shell=False, stdout=PIPE, stderr=PIPE)
                errorOccured=False
            except OSError as e:
                self.endSignal.emit(1)
#                self.lvM.emit("Command rsync not found: "+str(e))
            except ValueError as e:
                self.endSignal.emit(2)
#                self.lvM.emit("Error in rsync parameters: "+str(e))
            except Exception as e  :
                self.endSignal.emit(3)
                self.lvM.emit("Error in rsync: "+str(e))
            if not errorOccured:
                buf=''
                while not self.stopped:
                    letter=self.process.stdout.read(1)
                    buf=buf+letter
                    if letter=='\n' or letter=='\r':
                        progressL=re.findall("([0-9]*)%", buf)
                        speedK=re.findall("([0-9.]*)kB/s", buf)
                        speedM=re.findall("([0-9.]*)MB/s", buf)
                        remain=re.findall("[0-9]*:[0-9]*:[0-9]*",buf)
                        if len(progressL) != 0:
                            progress= eval(progressL[0])
                            self.progressSignal.emit(progress)
                        else:
                            if (len(buf) !=0):
                                self.lvM.emit(buf.rstrip())
                        if len(speedK) != 0:
                            speed= eval(speedK[0])
                            self.speedSignal.emit(speed)
                        if len(speedM) != 0:
                            speed= 1024*eval(speedM[0])
                            self.speedSignal.emit(speed)
                        if len(remain) != 0:
                            self.remainSignal.emit(remain[0])
                        buf=""
                    self.process.poll()
                    if self.process.returncode != None:
                        break
                self.lvM.emit("Ending with "+iso['nameWithPath'])
                self.checkSignal.emit(iso['row'])
                if self.stopped:
                    break
        self.endSignal.emit(0)
        self.speedSignal.emit(0)
        self.progressSignal.emit(0)
        self.stopped=False
        self.list=[]
        self.quit()

def rename(directory,oldRelease,newRelease):
    options=['d', 'f']
    for option in options:
        commande=['find', directory, '-type' ,option, '-exec','rename',oldRelease,newRelease, '{}', '+']
        process = Popen(commande, shell=False, stdout=PIPE, stderr=PIPE)
        process.poll()
        while True :
            item=process.stdout.readline().rstrip()
            print item
            process.poll()
            if process.returncode != None:
                if process.returncode!=0:
                    item=process.stderr.readline().rstrip()
                    return 'Error ', item
                else:
                    return "Success"
                break

class findIsos(QtCore.QThread):
    endSignal=QtCore.pyqtSignal(int)
    lvM=QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(findIsos, self).__init__(parent)
        self.list=[]
        self.localList=[]

    def setup(self,path, password, destination):
        self.path=path
        self.password=password
        self.destination=destination

    def getList(self):
        return self.list

    def getLocal(self):
        return self.localList
        
    def run(self):
        #   Lists ISO files in local directory
        root=QtCore.QDir(self.destination)
        root.setFilter(QtCore.QDir.AllDirs|QtCore.QDir.NoDot|QtCore.QDir.NoDotDot)
        dirs=root.entryList()
        for dir in dirs:
            sub=QtCore.QDir(self.destination+'/'+dir)
            sub.setNameFilters(["*.iso"])
            sub.setFilter(QtCore.QDir.Files)
            local=sub.entryList()
            if len(local)!=0:
                for iso in local:
                    self.localList.append([dir,iso])
        commande = ['rsync', '-avHP', '--list-only',str(self.path)]
        try:
            if self.password != "":
                envir = os.environ.copy()
                envir['RSYNC_PASSWORD']=str(self.password)
                process = Popen(commande, shell=False, stdout=PIPE, stderr=PIPE, env=envir)
            else:
                process = Popen(commande, shell=False, stdout=PIPE, stderr=PIPE)
        except OSError as e:
            self.lvM.emit("Command rsync not found: "+str(e))
            self.endSignal.emit(1)
            return 
        except ValueError as e:
            self.lvM.emit("Error in rsync parameters: "+str(e))
            self.endSignal.emit(2)
            return
        except Exception as e:
            # Unknown error in rsync
            self.lvM.emit("Error in rsync: "+str(e))
            self.endSignal.emit(3)
            return
        process.poll()
        while True :
            item=process.stdout.readline().rstrip()
            if item.lower().endswith('.iso') :
                words=item.split()
                self.list.append(words[-1])
            process.poll()
            if process.returncode != None:
                break
        self.endSignal.emit(0)

#syncIso('rsync://ftp5.gwdg.de/pub/linux/mageia/iso/4.1/Mageia-4.1-LiveCD-GNOME-en-i586-CD/', "/documents/Mageia-4/Mageia-4.1-LiveCD-GNOME-en-i586-CD/", "y8d5qr38728128I")