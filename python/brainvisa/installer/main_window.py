from PyQt4.uic import loadUi
from PyQt4.QtGui import QMainWindow, QTableView, QDialog, QMenu, QAction, QCursor, QAbstractItemView, QColor
from PyQt4.QtCore import SIGNAL, QVariant
import os
from aptget import AptGet
from soma.qt4gui.simple_table import SimpleTable
from soma.html import htmlEscape
from PyQt4.QtCore import Qt
    
    

class MainWindow( object ):
  def __init__( self, packageManager, parent=None ):
    self.packageManager = packageManager
    self.mainWindow = QMainWindow( parent )
    loadUi( os.path.join( os.path.dirname( __file__ ), 'main_window-b.ui' ), self.mainWindow )
    self.mainWindow.Reload.connect( self.mainWindow.Reload, SIGNAL( 'clicked( bool )' ), self.update )
    self.mainWindow.MarkAll.connect( self.mainWindow.MarkAll, SIGNAL( 'clicked( bool )' ), self.markAll )
    self.mainWindow.unMarkAll.connect( self.mainWindow.unMarkAll, SIGNAL( 'clicked( bool )' ), self.unMarkAll )
    self.mainWindow.Properties.connect( self.mainWindow.Properties, SIGNAL( 'clicked( bool )' ), self.showProperties )
    self.mainWindow.Upgrade.connect( self.mainWindow.Upgrade, SIGNAL( 'clicked( bool )' ), self.MarkUpgrade )
    self.mainWindow.Apply.connect( self.mainWindow.Apply, SIGNAL( 'clicked( bool )' ), self.apply )

  
    self.mainWindow.TableView.setModel( self.packageManager.table )
    self.mainWindow.TableView.resizeColumnsToContents()  
    self.mainWindow.TableView.setAlternatingRowColors( True )
    self.updateColors()

    self.mainWindow.TableView.mousePressEvent = self.mousePressEvent



  def update( self ):
    self.packageManager.update() 
    self.updateColors()

    
  def updateColors( self ):
    # if install : and Up to date -> ligne in blue, and if Upgradable -> ligne in yellow
    NumberOfRow = self.packageManager.table.rowCount( self.packageManager.table ) 
    for n in range ( NumberOfRow ):
      status = self.packageManager.table.row( n )[ 0 ]
      if status == 'Up to date':
        self.packageManager.table.setRowBackgroundColor( n, QColor(0, 0, 255, 100) )
      elif status == 'Upgradable':
        self.packageManager.table.setRowBackgroundColor( n, QColor(255, 255, 0, 100) )
      else:  
        self.packageManager.table.setRowBackgroundColor( n, None )


  def show( self ):
    self.mainWindow.show()


  def mousePressEvent(self, event):
    QTableView.mousePressEvent( self.mainWindow.TableView, event )
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      index = indexes[ 0 ].row()
      status = self.packageManager.table.row( index )[ 0 ]
#      print status
  
    if (event.button() == 2):
#      print 'droite'
#      print event.pos()
      menu = QMenu( self.mainWindow )
      if status == 'Not Installed':
        menu.addAction( 'Mark for Install', self.MarkOneForInstall )
      elif status == 'Up to date':
        menu.addAction(  'Mark for UnInstall', self.MarkOneForUninstall )
      elif status == 'Upgradable':
        menu.addAction( 'Mark for Upgrade', self.MarkOneForUgrade )
        menu.addAction(  'Mark for UnInstall', self.MarkOneForUninstall )
      elif status == 'Mark for Install':
        menu.addAction(  'UnMark for Install', self.UnMarkOneForInstall )
      elif status == 'Mark for UnInstall':
        menu.addAction( 'UnMark for UnInstall', self.UnMarkOneForUninstall )
      elif status == 'Mark for Upgrade':
        menu.addAction( 'UnMark for Upgrade', self.UnMarkOneForUpgrade ) 
     
 
 
      menu.addAction( 'Show Properties', self.showProperties )       
      menu.popup( event.globalPos() )   

  def MarkOneForInstall( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      index = indexes[ 0 ].row()
      status = self.packageManager.table.row( index )[ 0 ]
      dependencies = self.showRequiredDependencies()
      if dependencies != 'Cancel':
        packageSelected = self.packageManager.table.row( index )[ 1 ]
        self.packageManager.table.setRowBackgroundColor( index, QColor(0, 255, 0, 100) )   
        self.packageManager.table.setRow( index, ( 'Mark for Install', ) + self.packageManager.table.row( index )[ 1: ] )     
        if dependencies != []: 
          for type, package in dependencies:
            NumberOfRow = self.packageManager.table.rowCount( self.packageManager.table ) 
            for n in range ( NumberOfRow ):
              statu = self.packageManager.table.row( n )[ 0 ]
              namePackage = self.packageManager.table.row( n )[ 1 ]
              if namePackage == package:
                if statu == 'Not Installed':
                  self.packageManager.table.setRowBackgroundColor( n, QColor(0, 255, 0, 100) )   
                  self.packageManager.table.setRow( n, ( 'Mark for Install', ) + self.packageManager.table.row( n )[ 1: ] )        
                


  def UnMarkOneForInstall( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      index = indexes[ 0 ].row()
      self.packageManager.table.setRowBackgroundColor( index, None )   
      self.packageManager.table.setRow( index, ( 'Not Installed', ) + self.packageManager.table.row( index )[ 1: ] )     


  def MarkOneForUninstall( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      index = indexes[ 0 ].row()
      status = self.packageManager.table.row( index )[ 0 ]
#     reverse dependencies...
      rev_dependencies = self.showReverseDependencies()
      if rev_dependencies != 'Cancel':
        self.packageManager.table.setRowBackgroundColor( index, QColor(255, 0, 0, 100) )  
        self.packageManager.table.setRow( index, ( 'Mark for UnInstall', ) + self.packageManager.table.row( index )[ 1: ] )     
        if rev_dependencies != []: 
          for type, package in rev_dependencies:
            NumberOfRow = self.packageManager.table.rowCount( self.packageManager.table ) 
            for n in range ( NumberOfRow ):
              statu = self.packageManager.table.row( n )[ 0 ]
              namePackage = self.packageManager.table.row( n )[ 1 ]
              if namePackage == package:
                if statu == 'Up to date':
                  self.packageManager.table.setRowBackgroundColor( n, QColor(255, 0, 0, 100) )   
                  self.packageManager.table.setRow( n, ( 'Mark for UnInstall', ) + self.packageManager.table.row( n )[ 1: ] )
                elif statu == 'Upgradable':
                  self.packageManager.table.setRowBackgroundColor( n, QColor(255, 0, 0, 100) )   
                  self.packageManager.table.setRow( n, ( 'Mark for UnInstall', ) + self.packageManager.table.row( n )[ 1: ] )
                elif statu == 'Mark for Upgrade':
                  self.packageManager.table.setRowBackgroundColor( n, QColor(255, 0, 0, 100) )   
                  self.packageManager.table.setRow( n, ( 'Mark for UnInstall', ) + self.packageManager.table.row( n )[ 1: ] )              
                elif statu == 'Mark for Install':
                  self.packageManager.table.setRowBackgroundColor( n, None )   
                  self.packageManager.table.setRow( n, ( 'Not Installed', ) + self.packageManager.table.row( n )[ 1: ] ) 


  def MarkOneForUgrade( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      index = indexes[ 0 ].row()
      status = self.packageManager.table.row( index )[ 0 ]
      self.packageManager.table.setRowBackgroundColor( index, QColor(0, 255, 0, 100) )  
      self.packageManager.table.setRow( index, ( 'Mark for Upgrade', ) + self.packageManager.table.row( index )[ 1: ] )     


  def UnMarkOneForUninstall( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      index = indexes[ 0 ].row()
      status = self.packageManager.table.row( index )[ 0 ]
      versAvail = self.packageManager.table.row( index )[ 3 ]
      versioNow = self.packageManager.table.row( index )[ 2 ]
      print versAvail
      print versioNow
      if ( versAvail > versioNow ):     
        self.packageManager.table.setRowBackgroundColor( index, QColor(255, 255, 0, 100) )   
        self.packageManager.table.setRow( index, ( 'Upgradable', ) + self.packageManager.table.row( index )[ 1: ] )     
      else:
        self.packageManager.table.setRowBackgroundColor( index, QColor(0, 0, 255, 100) )   
        self.packageManager.table.setRow( index, ( 'Up to date', ) + self.packageManager.table.row( index )[ 1: ] )     
  


  def UnMarkOneForUpgrade( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      index = indexes[ 0 ].row()
      status = self.packageManager.table.row( index )[ 0 ]
      self.packageManager.table.setRowBackgroundColor( index, QColor(255, 255, 0, 100) )   
      self.packageManager.table.setRow( index, ( 'Upgradable', ) + self.packageManager.table.row( index )[ 1: ] )     


  def MarkUpgrade( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      index = indexes[ 0 ].row()
      NumberOfRow = self.packageManager.table.rowCount( self.packageManager.table ) 
      for n in range ( NumberOfRow ):
        status = self.packageManager.table.row( n )[ 0 ]
        if status == 'Upgradable':
          self.packageManager.table.setRowBackgroundColor( n, QColor(0, 255, 0, 100) )   
          self.packageManager.table.setRow( n, ( 'Mark for Upgrade', ) + self.packageManager.table.row( n )[ 1: ] )     
        	      

  def showProperties( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      #print 'Selection:', indexes[ 0 ].row()
      packageSelected = self.packageManager.table.row( indexes[ 0 ].row() )[1]
      #print packageSelected 
      
      dialog = QDialog( self.mainWindow )
      loadUi( os.path.join( os.path.dirname( __file__ ), 'dialog_properties.ui' ), dialog )

      dependencies = self.packageManager.dependsOf( packageSelected ).get( packageSelected, () )
      text = '<html><body>' + '<b>Dependencies of Package</b> ' + '<br><br>\n'
      for type, package in dependencies:
        text += '<b>' + type + ':</b> ' + htmlEscape( package ) + '<br>\n'
      text += '</body></html>'
      dialog.txtDependencies.setText( text )

      dialog.exec_()


  def showRequiredDependencies( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      #print 'Selection:', indexes[ 0 ].row()
      packageSelected = self.packageManager.table.row( indexes[ 0 ].row() )[1]
      #print packageSelected 
      
      dialog = QDialog( self.mainWindow )
      loadUi( os.path.join( os.path.dirname( __file__ ), 'dialog_markforinstall.ui' ), dialog )

      dependencies = self.packageManager.dependsOf( packageSelected ).get( packageSelected, () )
      text = '<html><body>' + '<b>Mark additional required Packages</b> ' + '<br><br>\n'
      for type, package in dependencies:
        text += '<b>' + type + ':</b> ' + htmlEscape( package ) + '<br>\n'
      text += '</body></html>'
      dialog.txtDependencies.setText( text )
      if dependencies == ():
        return dependencies
      else:
        ret = dialog.exec_()
        if ret == QDialog.Accepted:
          return dependencies
        else:
          dependencies = 'Cancel'
          return dependencies
         
  def unMarkAll( self ): 
    NumberOfRow = self.packageManager.table.rowCount( self.packageManager.table ) 
    for n in range ( NumberOfRow ):
      status = self.packageManager.table.row( n )[ 0 ]
      if status == 'Mark for Install':
        self.packageManager.table.setRowBackgroundColor( n, None )       
        self.packageManager.table.setRow( n, ( 'Not Installed', ) + self.packageManager.table.row( n )[ 1: ] )            

  def markAll( self ):  
    NumberOfRow = self.packageManager.table.rowCount( self.packageManager.table ) 
    for n in range ( NumberOfRow ):
      status = self.packageManager.table.row( n )[ 0 ]
      if status == 'Not Installed':
        self.packageManager.table.setRowBackgroundColor( n, QColor(0, 255, 0, 100) )   
        self.packageManager.table.setRow( n, ( 'Mark for Install', ) + self.packageManager.table.row( n )[ 1: ] )     

    
  def toto( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      index = indexes[ 0 ].row()
      status = self.packageManager.table.row( index )[ 0 ]
            
      packageSelected = self.packageManager.table.row( indexes[ 0 ].row() )[1]
      	          
      if status == 'Not Installed':
	      self.packageManager.table.setRowBackgroundColor( index, QColor(0, 0, 255, 100) )
	      
	      self.packageManager.table.setRow( index, ( 'Up to date', packageSelected, '3.2.0', ) + self.packageManager.table.row( index )[ 3: ]  )

      else:
	      self.packageManager.table.setRowBackgroundColor( index, QColor(255, 255, 0, 100) )
	      self.packageManager.table.setRow( index, ( 'Upgradable', packageSelected, '3.0.0', ) + self.packageManager.table.row( index )[ 3: ]  )
        

  def showReverseDependencies( self ):
    indexes = self.mainWindow.TableView.selectedIndexes()
    if indexes:
      #print 'Selection:', indexes[ 0 ].row()
      packageSelected = self.packageManager.table.row( indexes[ 0 ].row() )[1]   
      dialog = QDialog( self.mainWindow )
      loadUi( os.path.join( os.path.dirname( __file__ ), 'dialog_markforemove.ui' ), dialog )
      dependencies = self.packageManager.isDependentOf( packageSelected ).get( packageSelected, () )
      text = '<html><body>' + '<b>Mark UnInstall Reverse Dependencies</b> ' + '<br><br>\n'
      for type, package in dependencies:
        text += '<b>' + type + ':</b> ' + htmlEscape( package ) + '<br>\n'
      text += '</body></html>'
      dialog.txtReverseDependencies.setText( text )
      if dependencies == ():
        return dependencies
      else:
        ret = dialog.exec_()
        if ret == QDialog.Accepted:
          return dependencies
        else:
          dependencies = 'Cancel'
          return dependencies


  def showPackageWillBeInstalled( self, *PackageForInstall ):

      dialog = QDialog( self.mainWindow )
      loadUi( os.path.join( os.path.dirname( __file__ ), 'dialog_properties.ui' ), dialog )
      packages = self.packageManager.PackageWillBeInstalled( *PackageForInstall )
      print packages
      text = '<html><body>' + '<b>The following NEW packages will be installed</b> ' + '<br><br>\n'
      for package in packages:
        text += htmlEscape( package ) + '<br>\n'
      text += '</body></html>'
      dialog.txtDependencies.setText( text )
      ret = dialog.exec_()
      if ret == QDialog.Accepted:
          return 'Accepted'
      else:
          return 'Cancel'

  def showPackageWillBeUnInstalled( self, *PackageForUnInstall ):
      dialog = QDialog( self.mainWindow )
      loadUi( os.path.join( os.path.dirname( __file__ ), 'dialog_properties.ui' ), dialog )
      packages = self.packageManager.PackageWillBeUnInstalled( *PackageForUnInstall )
      text = '<html><body>' + '<b>The following NEW packages will be REMOVED</b> ' + '<br><br>\n'
      for package in packages:
        text += htmlEscape( package ) + '<br>\n'
      text += '</body></html>'
      dialog.txtDependencies.setText( text )

      ret = dialog.exec_()
      if ret == QDialog.Accepted:
          return 'Accepted'
      else:
          return 'Cancel'
  
          
  def apply( self ):  
    NumberOfRow = self.packageManager.table.rowCount( self.packageManager.table ) 
    listOfPackageForInstall = []
    listOfPackageForUnInstall = []
    listOfPackageForUpgrade = []    
    for n in range ( NumberOfRow ):
      status = self.packageManager.table.row( n )[ 0 ]
      namePackage = self.packageManager.table.row( n )[ 1 ]
      if status == 'Mark for Install':
        listOfPackageForInstall.append(namePackage)
      elif status == 'Mark for UnInstall':
        listOfPackageForUnInstall.append(namePackage)
      elif status == 'Mark for Upgrade':
        listOfPackageForUpgrade.append(namePackage)

    if ( listOfPackageForInstall != [] ):  
      if ( self.showPackageWillBeInstalled( *listOfPackageForInstall ) ==  'Accepted' ):
        self.packageManager.install( *listOfPackageForInstall )
        self.update()

    if ( listOfPackageForUnInstall != [] ):  
      if ( self.showPackageWillBeUnInstalled( *listOfPackageForUnInstall ) ==  'Accepted' ):
        self.packageManager.uninstall( *listOfPackageForUnInstall )
        self.update()

    if ( listOfPackageForUpgrade != [] ):     
      self.packageManager.upgrade( *listOfPackageForUnInstall ) 
      self.update()
      
      

      
