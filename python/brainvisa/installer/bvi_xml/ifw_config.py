#!/usr/bin/env python
# -*- coding: utf-8 -*-

from brainvisa.installer.bvi_utils.xml_file import XmlFile


class IFWConfig(XmlFile): #pylint: disable=R0902
	"""Model of XML IFW config file.

	Parameters
	----------
	Name 		: Name of the product being installed. This is mandatory.
	Version 	: Version number of the product being installed. This is mandatory.
	Title 		: Name of the installer as displayed on the title bar.
	Publisher 	: Publisher of the software (as shown in the Windows Control Panel).
	ProductUrl 	: URL to a page that contains product information on your web site.
	Icon 		: Filename for a custom installer icon. The actual file is looked up by attaching a '.icns' (Mac OS X), '.ico' (Windows) or '.png' (Unix) suffix. Deprecated, use InstallerApplicationIcon and / or InstallerWindowIcon instead.
	InstallerApplicationIcon : Filename for a custom installer icon. The actual file is looked up by attaching a '.icns' (Mac OS X), '.ico' (Windows). No functionality on Unix.
	InstallerWindowIcon : Filename for a custom window icon in PNG format for the Installer application.
	Logo 		: Filename for a logo used as QWizard::LogoPixmap.
	Watermark 	: Filename for a watermark used as QWizard::WatermarkPixmap.
	Banner 		: Filename for a banner used as QWizard::BannerPixmap (only used by ModernStyle).
	Background 	: Filename for an image used as QWizard::BackgroundPixmap (only used by MacStyle).
	RunProgram 	: Command executed after the installer is done if the user accepts the action.
	RunProgramArguments : Arguments passed to the program specified in RunProgram.
	RunProgramDescription : Text shown next to the check box for running the program after the installation. Defaults to Run <Name>.
	StartMenuDir : Name of the default program group for the product in the Windows Start menu.
	TargetDir 	 : Default target directory for installation.
	AdminTargetDir : Default target directory for installation with administrator rights.
	TagRepositories : List of remote repositories (i.e. TagRepository objects). You can add several Repository sections that each specify the Url to access the repository. For more information, see Configuring Repositories.
	UninstallerName : Filename of the generated uninstaller. Defaults to uninstall. The platform-specific executable file extension is appended.
	UninstallerIniFile : Filename for the configuration of the generated uninstaller. Defaults to UninstallerName.ini.
	RemoveTargetDir : Set to false if the target directory should not be deleted when uninstalling.
	AllowNonAsciiCharacters : Set to true if the installation path can contain non-ASCII characters.
	RepositorySettingsPageVisible : Set to false to hide the repository settings page inside the settings dialog.
	AllowSpaceInPath : Set to true if the installation path can contain space characters.
	DependsOnLocalInstallerBinary : Set to true if you want to prohibit installation from an external resource, such as a network drive. This might make sense for e.g. very big installers. The option is only used on Windows.
	TargetConfigurationFile : Filename for the configuration file on the target. Default is components.xml.
	Translations : List of language codes to be used for translating the user interface. To add several language variants, specify several Translation sections that each specify the name of a language variant. Optional. For more information, see Translating Pages.
	UrlQueryString : This string needs to be in the form "key=value" and will be appended to archive download requests. This can be used to transmit information to the webserver hosting the repository.
	"""

	def update(self, filename):
		self.init('Installer')
		# Root subelements
		self.set_root_subelement_text('Name', self.Name)
		self.set_root_subelement_text('Version', self.Version)
		self.set_root_subelement_text('Title', self.Title)
		self.set_root_subelement_text('Publisher', self.Publisher)
		self.set_root_subelement_text('ProductUrl', self.ProductUrl)
		self.set_root_subelement_text('Icon', self.Icon)
		# if platform.system() != 'Linux:'
		# 	self.set_root_subelement_text('InstallerApplicationIcon', self.InstallerApplicationIcon)
		# self.set_root_subelement_text('InstallerWindowIcon', self.InstallerWindowIcon)
		self.set_root_subelement_text('Logo', self.Logo)
		self.set_root_subelement_text('Watermark', self.Watermark)
		self.set_root_subelement_text('Banner', self.Banner)
		self.set_root_subelement_text('Background', self.Background)
		self.set_root_subelement_text('RunProgram', self.RunProgram)
		self.set_root_subelement_text('RunProgramArguments', self.RunProgramArguments)
		self.set_root_subelement_text('RunProgramDescription', 
			self.RunProgramDescription)
		self.set_root_subelement_text('StartMenuDir', self.StartMenuDir)
		self.set_root_subelement_text('TargetDir', self.TargetDir)
		self.set_root_subelement_text('AdminTargetDir', self.AdminTargetDir)		
		self.set_root_subelement_text('UninstallerName', self.UninstallerName)
		self.set_root_subelement_text('UninstallerIniFile', self.UninstallerIniFile)
		self.set_root_subelement_text('RemoveTargetDir', self.RemoveTargetDir)
		self.set_root_subelement_text('AllowNonAsciiCharacters', 
			self.AllowNonAsciiCharacters)
		self.set_root_subelement_text('RepositorySettingsPageVisible', 
			self.RepositorySettingsPageVisible)
		self.set_root_subelement_text('AllowSpaceInPath', self.AllowSpaceInPath)
		self.set_root_subelement_text('DependsOnLocalInstallerBinary', 
			self.DependsOnLocalInstallerBinary)
		self.set_root_subelement_text('TargetConfigurationFile', 
			self.TargetConfigurationFile)
		self.set_root_subelement_text('Translations', self.Translations)
		self.set_root_subelement_text('UrlQueryString', self.UrlQueryString)
		# List subelements
		if self.TagRepositories:
			e = self.add_element('RemoteRepositories')
			for tr in self.TagRepositories:
				e.append(tr.element)	

	def __init__(self,
		Name, 
		Version, 
		Title = None,
		Publisher = None, 
		ProductUrl = None, 
		Icon = None, 
		InstallerApplicationIcon = None, 
		InstallerWindowIcon = None, 
		Logo = None, 
		Watermark = None,
		Banner = None, 
		Background = None, 
		RunProgram = None, 
		RunProgramArguments = None, 
		RunProgramDescription = None, 
		StartMenuDir = None, 
		TargetDir = None, 
		AdminTargetDir = None, 
		TagRepositories = None, 
		UninstallerName = None, 
		UninstallerIniFile = None, 
		RemoveTargetDir = None, 
		AllowNonAsciiCharacters = None, 
		RepositorySettingsPageVisible = None, 
		AllowSpaceInPath = None, 
		DependsOnLocalInstallerBinary = None, 
		TargetConfigurationFile = None, 
		Translations = None,
		UrlQueryString = None):
		self.Name = Name
		self.Version = Version
		self.Title = Title
		self.Publisher = Publisher 
		self.ProductUrl = ProductUrl 
		self.Icon = Icon 
		self.InstallerApplicationIcon = InstallerApplicationIcon 
		self.InstallerWindowIcon = InstallerWindowIcon 
		self.Logo = Logo 
		self.Watermark = Watermark
		self.Banner = Banner 
		self.Background = Background 
		self.RunProgram = RunProgram 
		self.RunProgramArguments = RunProgramArguments 
		self.RunProgramDescription = RunProgramDescription 
		self.StartMenuDir = StartMenuDir 
		self.TargetDir = TargetDir 
		self.AdminTargetDir = AdminTargetDir 
		self.TagRepositories = TagRepositories 
		self.UninstallerName = UninstallerName 
		self.UninstallerIniFile = UninstallerIniFile 
		self.RemoveTargetDir = RemoveTargetDir 
		self.AllowNonAsciiCharacters = AllowNonAsciiCharacters 
		self.RepositorySettingsPageVisible = RepositorySettingsPageVisible 
		self.AllowSpaceInPath = AllowSpaceInPath 
		self.DependsOnLocalInstallerBinary = DependsOnLocalInstallerBinary 
		self.TargetConfigurationFile = TargetConfigurationFile 
		self.Translations = Translations
		self.UrlQueryString = UrlQueryString
