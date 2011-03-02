import os
from copy import copy
from subprocess import Popen, PIPE, STDOUT
from soma.qt4gui.simple_table import SimpleTable

class AptGet( object ):
  def __init__( self, installDirectory ):
    self.installDirectory = os.path.normpath( os.path.abspath( installDirectory ) )

  def _system( self, *args ):
    env = copy( os.environ )
    env[ 'LANG' ] = 'C'
    pipe = Popen( args, stdout=PIPE, stderr=PIPE, env=env )
    pipe.wait()
#    print pipe.returncode
#    print pipe.stderr
    for line in pipe.stdout:
      yield line

  def createNewConfiguration( self, repository=None ):
    for d in ( ( 'apt_admin', ),
               ( 'apt_admin','updates' ),
               ( 'apt_admin','lib' ),
               ( 'apt_admin','lib', 'dpkg' ),
               ( 'apt_admin','lib', 'apt' ),
               ( 'apt_admin','lib', 'dpkg', 'updates' ),
               ( 'apt_admin','lib', 'dpkg', 'triggers' ),
               ( 'apt_admin','lib', 'dpkg', 'info' ),
               ( 'apt_admin','cache' ),
               ( 'apt_admin','cache', 'apt' ),
               ( 'apt_admin','log' ),
               ( 'apt_admin','log', 'apt' ),
               ( 'apt_admin','archives', ),
               ( 'apt_admin','archives', 'partial' ),
               ( 'apt_admin','lists', ),
               ( 'apt_admin','lists', 'partial' ),           
                ) :
      os.mkdir( os.path.join( self.installDirectory, *d ) )
    
    for f in ( 'apt_admin/status',
               'apt_admin/available',
               'apt_admin/lib/dpkg/lock',
               'apt_admin/lib/dpkg/status',
               'apt_admin/lib/dpkg/available',
               'apt_admin/preferences',
               'apt_admin/lists/lock', ):                         
      b = open( os.path.join( self.installDirectory, *f.split( '/' ) ), 'w' )
      b.close()
    
    f = open( os.path.join( self.installDirectory, 'apt_admin', 'sources.list' ), 'w' )
    if repository:
      print >> f, 'deb file://' + repository + ' brainvisa main contrib non-free multiverse'
    f.close()
    
    f = open( os.path.join( os.path.dirname( __file__ ), 'apt.conf.in' ) )
    content = f.read()
    f = open(  os.path.join( self.installDirectory, 'apt.conf' ), 'w' )
    f.write( content.replace( 'MAIN_DIR', self.installDirectory ) )
    f.close()


    os.system( 'apt-get -c ' +  os.path.join( self.installDirectory, 'apt.conf' ) +  ' update' )
#   self._system( 'apt-get', '-c', os.path.join( self.installDirectory, 'apt.conf' ), 'update' )

    
  def getAllPackages( self ):
    for line in self._system( 'apt-cache', '-c', os.path.join( self.installDirectory, 'apt.conf' ), 'search', '.*' ):
      line = line.strip()
#      print '!!', repr( line )
      packageName, onSEnFout, packageShortDescription = line.split( None, 2 )
#      print '!!', repr( packageName )
      installedVersion, latestVersion = self.getVersions( packageName )
      yield ( packageName, installedVersion, latestVersion, packageShortDescription )
        
  def getVersions( self, packageName ):
      installedVersion = None
      for line in self._system( 'dpkg', 
        '--force-not-root', 
        '--force-bad-path', 
        '--root', self.installDirectory,
        '--admindir=' + os.path.join( self.installDirectory, 'apt_admin', 'lib', 'dpkg' ),
        '--log=' + os.path.join( self.installDirectory, 'apt_admin', 'lib', 'dpkg', 'dpkg.log' ),
        '-s', packageName ):
        line = line.strip()
        if line.startswith( 'Version:' ):
          installedVersion = line.split( None, 1 )[ 1 ]
          break
      latestVersion = None
      for line in self._system( 'apt-cache', '-c', os.path.join( self.installDirectory, 'apt.conf' ), 'show', packageName ):
        line = line.strip()
        if line.startswith( 'Version:' ):
          latestVersion = line.split( None, 1 )[ 1 ]
          break
      return ( installedVersion, latestVersion )      
      
  def dependsOf( self, *packageNames ):
    result = {}
    currentDependencies = set()
    for line in self._system( 'apt-cache', '-c', os.path.join( self.installDirectory, 'apt.conf' ), 'depends', *packageNames ):
      if line and line[ 0 ].isspace():
        # Line is indented
        dependencyType, package = line.strip().split( None, 1 )
        dependencyType = dependencyType[ :-1 ]
        currentDependencies.add( ( dependencyType, package ) )
      else:
        if currentDependencies:
          result[ currentPackage ] = currentDependencies
        # Line is not indented
        currentPackage = line.strip()
        currentDependencies = set()
    if currentDependencies:
      result[ currentPackage ] = currentDependencies
    return result

  def isDependentOf( self, *packageNames ):
    result = {}
    currentReverseDependencies = set()
    currentPackage = 'init'
    for line in self._system( 'apt-cache', '-c', os.path.join( self.installDirectory, 'apt.conf' ), 'rdepends', *packageNames ):
      if line and line[ 0 ].isspace():
        # Line is indented
        package = line.strip()
        currentReverseDependencies.add( ( dependencyType, package ) )
      else:
        # Line is not indented
        if (currentPackage == 'init'):
          currentPackage = line.strip()
        else:  
          dependencyType = line.strip()
          dependencyType = dependencyType[ :-1 ]
    if currentReverseDependencies:
      result[ currentPackage ] = currentReverseDependencies
    return result


  def PackageWillBeUnInstalled( self, *packageNames ):
    result = []
    for line in self._system( 'apt-get', '-c', os.path.join( self.installDirectory, 'apt.conf' ), '-s', 'remove', *packageNames ):
      if line and line[ 0 ].isspace():
        # Line is indented
        packages = line.strip()
        result = packages.split()
    return result 


  def PackageWillBeInstalled( self, *packageNames ):
    result = []
    for line in self._system( 'apt-get', '-c', os.path.join( self.installDirectory, 'apt.conf' ), '-s', 'install', *packageNames ):
      if line and line[ 0 ].isspace():
        # Line is indented
        packages = line.strip()
        result = packages.split()
      else:
        # Line is not indented
        onveraplustard = line
    return result 


  def install( self, *packageNames ):
    result = {}   
    for line in self._system( 'apt-get', '-c', os.path.join( self.installDirectory, 'apt.conf' ), '-y', 'install', *packageNames ):
      print line    
    
  def uninstall( self, *packageNames ):
    result = {}
    for line in self._system( 'apt-get', '-c', os.path.join( self.installDirectory, 'apt.conf' ), '-y', 'remove', *packageNames ):
      print line
    
  def upgrade( self, *packageNames ):
    result = {}    
    for line in self._system( 'apt-get', '-c', os.path.join( self.installDirectory, 'apt.conf' ), '-y', 'upgrade', *packageNames ):
      print line
   
     
class PackageManager( object ):
  def __init__( self, aptget ):
  
    self.table = SimpleTable( ('status', 'Toolbox', 'Ver. Installed', 'Ver. Available', 'Description' ) )
    self.aptget = aptget
    self.update()

  def update( self ):
    self.table.clear()
    for packageName, installedVersion, latestVersion, packageShortDescription in self.aptget.getAllPackages():
      if not installedVersion:
        status = 'Not Installed'    
      elif installedVersion == latestVersion:
        status = 'Up to date'
      elif installedVersion < latestVersion:
        status = 'Upgradable'
      else:
        status = '???'
      self.table.addRow( ( status, packageName, installedVersion, latestVersion, packageShortDescription) )
 
  
  def dependsOf( self, *packageNames ):
    '''Return the dependencies of a list of packages
    '''
    return self.aptget.dependsOf( *packageNames )
    
  def isDependentOf( self, *packageNames ):
    return self.aptget.isDependentOf( *packageNames )
        
  def PackageWillBeInstalled( self, *packageNames ):
    return self.aptget.PackageWillBeInstalled( *packageNames )

  def PackageWillBeUnInstalled( self, *packageNames ):
    return self.aptget.PackageWillBeUnInstalled( *packageNames )   
  
  def install( self, *packageNames ):
    ''' install a list of packages
    '''
    self.aptget.install( *packageNames )
        
  def uninstall( self, *packageNames ):
    self.aptget.uninstall( *packageNames )
    
  def upgrade( self, *packageNames ):
    self.aptget.upgrade( *packageNames )  
    
    
  
    
    
   
    

