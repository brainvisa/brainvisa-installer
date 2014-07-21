var nVer = navigator.appVersion;
var nAgt = navigator.userAgent;
var browserName  = navigator.appName;
var fullVersion  = ''+parseFloat(navigator.appVersion);
var majorVersion = parseInt(navigator.appVersion,10);
var nameOffset,verOffset,ix;
var repversion;
var urlbase;

// In Opera, the true version is after "Opera" or after "Version"
if ((verOffset=nAgt.indexOf("Opera"))!=-1) {
 browserName = "Opera";
 fullVersion = nAgt.substring(verOffset+6);
 if ((verOffset=nAgt.indexOf("Version"))!=-1)
   fullVersion = nAgt.substring(verOffset+8);
}
// In MSIE, the true version is after "MSIE" in userAgent
else if ((verOffset=nAgt.indexOf("MSIE"))!=-1) {
 browserName = "Microsoft Internet Explorer";
 fullVersion = nAgt.substring(verOffset+5);
}
// In Chrome, the true version is after "Chrome"
else if ((verOffset=nAgt.indexOf("Chrome"))!=-1) {
 browserName = "Chrome";
 fullVersion = nAgt.substring(verOffset+7);
}
// In Safari, the true version is after "Safari" or after "Version"
else if ((verOffset=nAgt.indexOf("Safari"))!=-1) {
 browserName = "Safari";
 fullVersion = nAgt.substring(verOffset+7);
 if ((verOffset=nAgt.indexOf("Version"))!=-1)
   fullVersion = nAgt.substring(verOffset+8);
}
// In Firefox, the true version is after "Firefox"
else if ((verOffset=nAgt.indexOf("Firefox"))!=-1) {
 browserName = "Firefox";
 fullVersion = nAgt.substring(verOffset+8);
}
// In most other browsers, "name/version" is at the end of userAgent
else if ( (nameOffset=nAgt.lastIndexOf(' ')+1) <
          (verOffset=nAgt.lastIndexOf('/')) )
{
 browserName = nAgt.substring(nameOffset,verOffset);
 fullVersion = nAgt.substring(verOffset+1);
 if (browserName.toLowerCase()==browserName.toUpperCase()) {
  browserName = navigator.appName;
 }
}
// trim the fullVersion string at semicolon/space if present
if ((ix=fullVersion.indexOf(";"))!=-1)
   fullVersion=fullVersion.substring(0,ix);
if ((ix=fullVersion.indexOf(" "))!=-1)
   fullVersion=fullVersion.substring(0,ix);

majorVersion = parseInt(''+fullVersion,10);
if (isNaN(majorVersion)) {
 fullVersion  = ''+parseFloat(navigator.appVersion);
 majorVersion = parseInt(navigator.appVersion,10);
}


var links = {
    win32 : [
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_win32_online.exe',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_win32_online.exe.md5',
        'Windows (32 bits)',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_win32_offline.exe',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_win32_offline.exe.md5'
    ],
    osx :  [
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_osx_online.dmg',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_osx_online.dmg.md5',
        'Mac OS X',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_osx_offline',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_osx_offline.md5',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_osx_online.app.zip',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_osx_online.app.zip.md5',
    ],
    linux32 :  [
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_x86_32_online',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_x86_32_online.md5',
        'Linux (32 bits)',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_x86_32_offline',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_x86_32_offline.md5'
    ],
    linux64 :  [
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_x86_64_online',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_x86_64_online.md5',
        'Linux (64 bits)',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_x86_64_offline',
        urlbase + 'download/installer/' + repversion + '/brainvisa_installer_x86_64_offline.md5'
    ]
};


function resolveURL(url) {
    var div = document.createElement('div');
    div.innerHTML = "<a></a>";
    div.firstChild.href = url; // Ensures that the href is properly escaped
    div.innerHTML = div.innerHTML; // Run the current innerHTML back through the parser
    return div.firstChild.href;
}

var repos_links = {
    win32   : [
        urlbase + 'repositories/' + repversion + '/win32', 
        resolveURL(urlbase + 'repositories/' + repversion + '/win32')
    ],
    osx     : [
        urlbase + 'repositories/' + repversion + '/osx',
        resolveURL(urlbase + 'repositories/' + repversion + '/osx')
    ],
    linux32 : [
        urlbase + 'repositories/' + repversion + '/linux32',
        resolveURL(urlbase + 'repositories/' + repversion + '/linux32')
    ],
    linux64 : [
        urlbase + 'repositories/' + repversion + '/linux64',
        resolveURL(urlbase + 'repositories/' + repversion + '/linux64')
    ]
};

var myURL = 'Linux';
var myOS = '';
var myMD5 = '';

if (navigator.appVersion.indexOf("Win")!=-1)
{
    myURL = links.win32[0];
    myMD5 = links.win32[1];
    myOS  = links.win32[2];
}

if (navigator.appVersion.indexOf("Mac")!=-1)
{
    myURL = links.osx[0];
    myMD5 = links.osx[1];
    myOS  = links.osx[2];
}

if (navigator.appVersion.indexOf("X11")!=-1)
{
    if (navigator.userAgent.indexOf("x86_64")!=-1)
    {
        myURL = links.linux64[0];
        myMD5 = links.linux64[1];
        myOS  = links.linux64[2];
    }
    else
    {
        myURL = links.linux32[0];
        myMD5 = links.linux32[1];
        myOS  = links.linux32[2];
    }

}

/*
document.write(''
 +'Browser name  = '+browserName+'<br>'
 +'Full version  = '+fullVersion+'<br>'
 +'Major version = '+majorVersion+'<br>'
 +'navigator.appName = '+navigator.appName+'<br>'
 +'navigator.userAgent = '+navigator.userAgent+'<br>'
 +'navigator.appVersion = '+navigator.appVersion+'<br>'
)

// This script sets OSName variable as follows:
// "Windows"    for all versions of Windows
// "MacOS"      for all versions of Macintosh OS
// "Linux"      for all versions of Linux
// "UNIX"       for all other UNIX flavors
// "Unknown OS" indicates failure to detect the OS

var OSName="Unknown OS";
if (navigator.appVersion.indexOf("Win")!=-1) OSName="Windows";
if (navigator.appVersion.indexOf("Mac")!=-1) OSName="MacOS";
if (navigator.appVersion.indexOf("X11")!=-1) OSName="UNIX";
if (navigator.appVersion.indexOf("Linux")!=-1) OSName="Linux";

document.write('Your OS: '+OSName);*/
