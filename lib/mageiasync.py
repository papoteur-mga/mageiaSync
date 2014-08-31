#!/usr/bin/python3
 
from PyQt5.QtWidgets import (  QApplication, QProgressDialog, QMainWindow,
        QDialog, QFileDialog,)
from PyQt5.QtGui import ( QStandardItemModel,QStandardItem,   )
from PyQt5 import QtCore  # , Qt, QThread, QObject, pyqtSignal)
import sys
import mageiaSyncUI
import mageiaSyncExt
import mageiaSyncDBprefs
import mageiaSyncDBrename


class prefsDialog(QDialog,mageiaSyncDBprefs.Ui_prefsDialog ):
   
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.selectDest.clicked.connect(isosSync.selectDestination)

class renameDialog(QDialog,mageiaSyncDBrename.Ui_renameDialog ):
    #   Display a dialog box to choose to rename an old collection of ISOs to a new one
   
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.chooseDir.clicked.connect(isosSync.renameDir)


class LogWindow(QProgressDialog):
    #   Display a box at start during the remote directory list loading
   
    def __init__(self, parent=None):
        super(LogWindow, self).__init__(parent)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle('Loading...')
        self.setLabelText('Loading images list from repository.')
        self.setMinimum(0)
        self.setMaximum(0)
        self.setAutoReset(False)
        self.setAutoClose(False)
        self.setMinimumDuration(1)
 
    def perform(self):
        self.progressDialog.setValue(self.progress)
 
class dbWarning(QProgressDialog):
    #   Display a box at start during the remote directory list loading
   
    def __init__(self, parent=None):
        super(dbWarning, self).__init__(parent)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle('Loading...')
        self.setLabelText('Loading images list from repository.')
        self.setMinimum(0)
        self.setMaximum(0)
        self.setAutoReset(False)
        self.setAutoClose(False)
        self.setMinimumDuration(1)
 
    def perform(self):
        self.progressDialog.setValue(self.progress)
 
class IsosViewer(QMainWindow, mageiaSyncUI.Ui_mainWindow):
    #   Display the main window
    def __init__(self, parent=None):
        super(IsosViewer, self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
        self.IprogressBar.setMinimum(0)
        self.IprogressBar.setMaximum(100)
        self.IprogressBar.setValue(0)
        self.IprogressBar.setEnabled(False)
        self.selectAllState=True
        self.stop.setEnabled(False)
        self.destination=''
        self.rsyncThread = mageiaSyncExt.syncThread(self)    # create a thread to launch rsync
        self.rsyncThread.progressSignal.connect(self.setProgress) 
        self.rsyncThread.speedSignal.connect(self.setSpeed) 
        self.rsyncThread.sizeSignal.connect(self.setSize) 
        self.rsyncThread.remainSignal.connect(self.setRemain) 
        self.rsyncThread.endSignal.connect(self.syncEnd) 
        self.rsyncThread.lvM.connect(self.lvMessage)
        self.rsyncThread.checkSignal.connect(self.checks)
        self.checkThreads=[]    #   A list of thread for each iso

 #      Model for list view in a table       
        self.model = QStandardItemModel(0, 6, self)
        headers=["Directory","Name","Size","Date","SHA1","MD5"]
        i=0
        for label in headers:
            self.model.setHeaderData(i, QtCore.Qt.Horizontal,label )
            i+=1

#       settings for the list view
        self.localList.setModel(self.model)
        self.localList.setColumnWidth(0,220)
        self.localList.setColumnWidth(1,220)
        self.localList.horizontalHeader().setStretchLastSection(True)
        # settings for local iso names management
        self.localListNames=[]

    def multiSelect(self):
    #   allows to select multiple lines in remote ISOs list
        self.listIsos.setSelectionMode(2)
        
    def add(self, iso):
    #   Add an remote ISO in list
         self.listIsos.addItem(iso)

    def localAdd(self, path,iso,isoSize):
        #   Add an entry in local ISOs list, with indications about checking
        itemPath=QStandardItem(path)
        itemIso=QStandardItem(iso)
        if isoSize==0:
            itemSize=QStandardItem('--')
        else:
            formatedSize='{:n}'.format(isoSize) #.replace(","," ")
            itemSize=QStandardItem(formatedSize)
        itemSize.setTextAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignHCenter)
        itemDate=QStandardItem("--/--/--")
        itemDate.setTextAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignHCenter)
        itemCheck1=QStandardItem("--")
        itemCheck1.setTextAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignHCenter)
        itemCheck5=QStandardItem("--")
        itemCheck5.setTextAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignHCenter)
        self.model.appendRow([itemPath,itemIso,itemSize,itemDate, itemCheck1, itemCheck5,])
        self.localListNames.append([path,iso])
    
    def setProgress(self, value):
        #   Update the progress bar
        self.IprogressBar.setValue(value)

    def setSpeed(self, value):
        #   Update the speed field
        self.speedLCD.display(value)

    def setSize(self, value):
        #   Update the size field
        self.Lsize.setText(str(value)+" bytes")
    
    def setRemain(self,remainTime):
        content=QtCore.QTime.fromString(remainTime,"h:mm:ss")
        self.timeRemaining.setTime(content)
        
    def checks(self,isoIndex):
        #   process a checking for each iso
        #   launches a thread for each iso
        newThread=mageiaSyncExt.checkThread(self)
        self.checkThreads.append(newThread)
        self.checkThreads[-1].setup(self.destination,self.model.data(self.model.index(isoIndex,0)) ,self.model.data(self.model.index(isoIndex,1)),isoIndex)
        self.checkThreads[-1].md5Signal.connect(self.md5Check)
        self.checkThreads[-1].sha1Signal.connect(self.sha1Check)
        self.checkThreads[-1].dateSignal.connect(self.dateCheck)
        self.checkThreads[-1].sizeSignal.connect(self.sizeUpdate)
        self.checkThreads[-1].checkStartSignal.connect(self.checkStart)
        self.checkThreads[-1].start()

    def checkStart(self,isoIndex):
        #   the function indicates that checking is in progress
        #   the hundred contains index of the value to check, the minor value contains the row
        col=(int)(isoIndex/100)
        row=isoIndex-col*100
        self.model.setData(self.model.index(row, col, QtCore.QModelIndex()), "Checking")
        
    def md5Check(self,check):
        if check>=128:
            val="OK"
            row=check-128
        else:
            val="Failed"
            row=check
        self.model.setData(self.model.index(row, 5, QtCore.QModelIndex()), val)

    def sha1Check(self,check):
        if check>=128:
            val="OK"
            row=check-128
        else:
            val="Failed"
            row=check
        self.model.setData(self.model.index(row, 4, QtCore.QModelIndex()), val)
    
    def dateCheck(self,check):
        if check>=128:
            val="OK"
            row=check-128
        else:
            val="Failed"
            row=check
        self.model.setData(self.model.index(row, 3, QtCore.QModelIndex()), val)

    def sizeUpdate(self,signal,isoSize):
        col=(int)(signal/100)
        row=signal-col*100
        self.model.setData(self.model.index(row, col, QtCore.QModelIndex()), '{:n}'.format(isoSize))
        
    def syncEnd(self, rc):
        if rc==1:
            self.lvMessage("Command rsync not found")
        elif rc==2:
            self.lvMessage("Error in rsync parameters")
        elif rc==3:
            self.lvMessage("Unknown error in rsync")
        self.IprogressBar.setEnabled(False)
        self.syncGo.setEnabled(True)
        self.listIsos.setEnabled(True)
        self.selectAll.setEnabled(True)
        self.stop.setEnabled(False)

    def prefsInit(self):
    #   Load the parameters at first
        params=QtCore.QSettings("Mageia","mageiaSync")
        try:
            #   the parameters already initilised?
            self.user=params.value("user", type="QString")
        except:
            # Values are not yet set
            self.pd=prefsDialog()
            #   Set values which are already defined
            try:
                self.pd.release.setText(params.value("release", type="QString"))
            except:
                pass
            try:
                self.pd.password.setText(params.value("password", type="QString"))
            except:
                pass
            try:
                self.pd.location.setText(params.value("location", type="QString"))
            except:
                pass
            try:
                self.pd.selectDest.setText(params.value("destination", type="QString"))
            except:
                self.pd.selectDest.setText(QtCore.QDir.currentPath())
            try:
                self.pd.bwl.setText(params.value("bwl", type="QInt"))
            except:
                pass
            try:
                self.pd.password.setText(params.value("password", type="QString"))
            except:
                pass
            answer=self.pd.exec_()
            if answer:                
                #   Update params
                params=QtCore.QSettings("Mageia","mageiaSync")
                params.setValue("release", self.pd.release.text())
                params.setValue("user",self.pd.user.text())
                params.setValue("password",self.pd.password.text())
                params.setValue("location",self.pd.location.text())
                params.setValue("destination",self.pd.selectDest.text())
                params.setValue("bwl",str(self.pd.bwl.value()))
                self.user=self.pd.user.text()
            else:
                pass
#                answer=QDialogButtonBox(QDialogButtonBox.Ok)
                # the user must set values or default values
            self.pd.close()
        self.release=params.value("release", type="QString")
        self.location=params.value("location", type="QString")
        self.password=params.value("password", type="QString")
        self.destination=params.value("destination", type="QString")
        self.bwl=params.value("bwl",type=int)
        self.localDirLabel.setText("Local directory: "+self.destination)
        if self.location !="":
            self.remoteDirLabel.setText("Remote directory: "+self.location)

    def selectDestination(self):
        #   dialog box to select the destination (local directory)
        directory = QFileDialog.getExistingDirectory(self, 'Select a directory','~/') 
        isosSync.destination = directory   
        self.pd.selectDest.setText(isosSync.destination)

        
    def selectAllIsos(self):
        #   Select or unselect the ISOs in remote list
        if self.selectAllState :
            for i in range(self.listIsos.count()):
                self.listIsos.item(i).setSelected(True)
            self.selectAll.setText("Unselect all")
        else:
            for i in range(self.listIsos.count()):
                self.listIsos.item(i).setSelected(False)
            self.selectAll.setText("Select all")
        self.selectAllState=not self.selectAllState

    def connectActions(self):
        self.actionQuit.triggered.connect(app.quit)
        self.actionRename.triggered.connect(self.rename)
        self.actionUpdate.triggered.connect(self.updateList)
        self.actionPreferences.triggered.connect(self.prefs)
        self.syncGo.clicked.connect(self.launchSync)
        self.selectAll.clicked.connect(self.selectAllIsos)
 
    def updateList(self):
        # From the menu entry
        self.lw = LogWindow()
        self.lw.show()
        self.listIsos.clear()
        self.model.removeRows(0,self.model.rowCount())
        if self.location  == "" :
            self.nameWithPath='rsync://'+self.user+'@bcd.mageia.org/isos/'+self.release+'/'
            print self.nameWithPath
        else:
            self.nameWithPath=self.location+'/'
        self.fillList = mageiaSyncExt.findIsos()
        self.fillList.setup(self.nameWithPath, self.password,self.destination)
        self.fillList.endSignal.connect(self.closeFill)
        self.fillList.start()
        
    def lvMessage( self,message):
        #   Add a line in the logview 
        self.lvText.append(message)
    
    def renameDir(self):
        #   Choose the directory where isos are stored
        directory = QFileDialog.getExistingDirectory(self, 'Select a directory',self.destination) 
        self.rd.chooseDir.setText(directory)

    def rename(self):
        #   rename old isos and directories to a new release
        self.rd=renameDialog()
        loc=[]
        loc=self.location.split('/')
        self.rd.oldRelease.setText(loc[-1])
        self.rd.newRelease.setText(loc[-1])
        self.rd.chooseDir.setText(self.location)
        answer=self.rd.exec_()
        if answer:
            returnMsg=mageiaSyncExt.rename(self.rd.chooseDir.text(),self.rd.oldRelease.text(),self.rd.newRelease.text())
            self.lvMessage(returnMsg)
        self.rd.close()
    
    def prefs(self):
        # From the menu entry
        self.pd=prefsDialog()
        self.pd.release.setText(self.release)
        self.pd.password.setText(self.password)
        self.pd.user.setText(self.user)
        self.pd.location.setText(self.location)
        self.pd.selectDest.setText(self.destination)
        self.pd.bwl.setValue(self.bwl)
        params=QtCore.QSettings("Mageia","mageiaSync")
        answer=self.pd.exec_()
        if answer:
            params.setValue("release", self.pd.release.text())
            params.setValue("user",self.pd.user.text())
            params.setValue("password",self.pd.password.text())
            params.setValue("location",self.pd.location.text())
            params.setValue("destination",self.pd.selectDest.text())
            params.setValue("bwl",str(self.pd.bwl.value()))
        self.prefsInit()
        self.pd.close()
        
    
    def launchSync(self):
        self.IprogressBar.setEnabled(True)
        self.stop.setEnabled(True)
        self.syncGo.setEnabled(False)
        self.listIsos.setEnabled(False)
        self.selectAll.setEnabled(False)
        # Connect the button Stop
        self.stop.clicked.connect(self.stopSync)
        self.rsyncThread.params(self.password, self.bwl)
        for iso in self.listIsos.selectedItems():
            path,name=iso.text().split('/')
            try:
                #   Look for ISO in local list
                item=self.model.findItems(name,QtCore.Qt.MatchExactly,1)[0]
            except:
                #   Remote ISO is not yet in local directory. We add it in localList and create the directory
                self.localAdd(path,name,0)
                basedir=QtCore.QDir(self.destination)
                basedir.mkdir(path)
                item=self.model.findItems(name,QtCore.Qt.MatchExactly,1)[0]
            row=self.model.indexFromItem(item).row()
            if self.location  == "" :
                self.nameWithPath='rsync://'+self.user+'@bcd.mageia.org/isos/'+self.release+'/'+path
            else:
                self.nameWithPath=self.location+path
            if (not str(path).endswith('/')):
                    self.nameWithPath+='/'
            self.rsyncThread.setup(self.nameWithPath, self.destination+'/'+path+'/',row)
        self.rsyncThread.start()             # start the thread
        # Pour les tests uniquement
            #rsync://$user@bcd.mageia.org/isos/$release/
        #self.nameWithPath='rsync://ftp5.gwdg.de/pub/linux/mageia/iso/4.1/Mageia-4.1-LiveCD-GNOME-en-i586-CD/'

    def closeFill(self,code):
        if code==0: #   list returned
            list=self.fillList.getList()
            for iso in list:
                self.add(iso)
        elif code==1:
            self.lvMessage("Command rsync not found")
        elif code==2:
            self.lvMessage("Error in rsync parameters")
        elif code==3:
            self.lvMessage("Unknown error in rsync")
        list=self.fillList.getList()

        list=self.fillList.getLocal()
        for path,iso,isoSize in list:
            self.localAdd(path,iso, isoSize)
        self.fillList.quit()
        self.lw.hide()
        
    def stopSync(self):
        self.rsyncThread.stop()
        self.IprogressBar.setEnabled(False)
        self.stop.setEnabled(False)
        self.syncGo.setEnabled(True)
        self.listIsos.setEnabled(True)
        self.selectAll.setEnabled(True)


    def main(self):
        self.show()
        #   Load or look for intitial parameters
        self.prefsInit()
        # look for Isos list and add it to the isoSync list. Update preferences
        self.updateList()
        self.multiSelect()
    
    def close(self):
        self.rsyncThread.stop()
        exit(0)
        
     
if __name__=='__main__':
    app = QApplication(sys.argv)
    isosSync = IsosViewer()
    isosSync.main()
    sys.exit(app.exec_())
