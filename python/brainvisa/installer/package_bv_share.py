
import os
import sys
import shutil
import glob
from package import Package
from component import Component

class PackageBVShare(Package):
    '''Specialize create() for brainvisa-share on Windows
    since the normal procedure results in too long filenames.
    Here we install in a "short" directory, then compress, and put the
    compressed archives at the package location.
    '''
    def create(self, folder):
        path = "%s/%s" % (folder, self.ifwname)
        if path in Component.done_created_components \
                or (configuration.skip_existing and os.path.exists(path)):
            return
        temp_folder = self.configuration.exception_info_by_name(
            self.name, 'PACKAGING_DIR')
        if temp_folder is None:
            if sys.platform.startswith('win'):
                temp_folder = "C:\\x"
            else:
                # used only for testing since non-wondows OS don't have the
                # problem
                temp_folder = '/tmp/x'
        if not os.path.exists(temp_folder):
            os.mkdir(temp_folder)
        if not self.write_it:
            logging.getLogger().info(
                "[ BVI ] PACKAGE: %s => skipping writing" % self.name)
            return

        # remove previous compressed packages to avoid messing archivegen
        for f in glob.glob(os.path.join(temp_folder, 'data', '*.7z')):
            os.unlink(f)

        self.compress = True # force compression
        ifwname = self.ifwname
        self._block_ifwname = True
        super(Package, self).create(temp_folder)

        self._block_ifwname = False
        self.copy_package(temp_folder, folder)

        if self.dependencies is None:
            return
        for dep_pack in self.dependencies:
            dep_pack.create(folder)

    @property
    def ifwname(self):
        if getattr(self, '_block_ifwname', False):
            return ''
        return super(PackageBVShare, self).ifwname

    def copy_package(self, temp_folder, folder):
        path = "%s/%s" % (folder, self.ifwname)
        temp_path = temp_folder
        if not os.path.isdir(path):
            os.makedirs(path)
        meta_path = os.path.join(path, 'meta')
        if os.path.exists(meta_path):
            shutil.rmtree(meta_path)
        shutil.copytree(os.path.join(temp_path, 'meta'), meta_path)
        data_path = os.path.join(path, 'data')
        temp_data_path = os.path.join(temp_path, 'data')
        if os.path.exists(data_path):
            shutil.rmtree(data_path)
        os.mkdir(data_path)
        infiles = glob.glob(os.path.join(temp_data_path, '*.7z'))
        for f in infiles:
            shutil.copy2(f, data_path)

