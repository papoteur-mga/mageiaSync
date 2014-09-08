# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 21:42:56 2014

@author: yves
"""

import re, os

from subprocess import Popen, PIPE
from PyQt5.QtCore import QDir, QFileInfo,pyqtSignal,QThread

class checkThread(QThread):
    md5Signal = pyqtSignal(int)
    sha1Signal= pyqtSignal(int)
    dateSignal=pyqtSignal(int)
    sizeSignal=pyqtSignal(int,int)
    checkStartSignal=pyqtSignal(int)

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
        import  datetime as datetime
        import time
        import locale
        locale.setlocale(locale.LC_ALL, 'C')
        #   Get and process the date from the file DATE.txt
        try:
            dateFile=open(str(self.destination)+'/'+self.path+'/DATE.txt','r')
        except:
            return False
        refDate=dateFile.readline()
        lits=re.split("\W+", refDate)
        nums=re.findall("([0-9]+)", refDate)
        refTime=re.findall("[0-9]*:[0-9]*:[0-9]*", refDate)[0]
        refDay=eval(nums[0])
        refYear=eval(nums[-1])
        refMonth=time.strptime(lits[1], "%b").tm_mon
        # Date of file
        info=datetime.datetime.fromtimestamp(os.path.getmtime(str(self.destination)+'/'+self.path+'/'+self.name))
        if(refDay==info.day and refMonth==info.month and refYear==info.year and refTime==info.strftime("%H:%M:%S")):
            return True
        else:
            return False
        
    def setup(self, destination, path,name,isoIndex):
        self.destination=destination
        self.path=path
        self.name=name
        self.isoIndex=isoIndex
        
    def run(self):
        signal=200+self.isoIndex
        isoSize=QFileInfo(str(self.destination)+'/'+self.path+'/' +self.name).size()
        self.sizeSignal.emit(signal, isoSize)
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
        

class syncThread(QThread):
    progressSignal = pyqtSignal(int)
    speedSignal= pyqtSignal(int)
    endSignal=pyqtSignal(int)
    remainSignal=pyqtSignal(str)
    checkSignal=pyqtSignal(int)
    sizeSignal=pyqtSignal(int)
    lvM=pyqtSignal(str)

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
        self.stopped=True
        try:
            self.process.terminate()
            self.lvM.emit("Process rsync stopped")
        except:
            self.lvM.emit("Process rsync already stopped")
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
                        sizeB=re.findall("[1-9](?:\d{0,2})(?:,\d{3})*",buf)
                        if len(progressL) != 0:
                            progress= eval(progressL[0])
                            self.progressSignal.emit(progress)
                            if len(sizeB) != 0:
                               self.sizeSignal.emit(eval(sizeB[0].replace(",","")))
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
        self.sizeSignal.emit(0)
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

class findIsos(QThread):
    endSignal=pyqtSignal(int)
    lvM=pyqtSignal(str)

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
        root=QDir(self.destination)
        root.setFilter(QDir.AllDirs|QDir.NoDot|QDir.NoDotDot)
        dirs=root.entryList()
        for dir in dirs:
            sub=QDir(self.destination+'/'+dir)
            sub.setNameFilters(["*.iso"])
            sub.setFilter(QDir.Files)
            local=sub.entryList()
            if len(local)!=0:
                for iso in local:
                    isoSize=QFileInfo(sub.absolutePath()+'/' +iso).size()
                    self.localList.append([dir,iso,isoSize])
        #   List the remote directory
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