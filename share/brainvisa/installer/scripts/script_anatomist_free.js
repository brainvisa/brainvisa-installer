function Component()
{
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (installer.value("os") === "win") {
        component.addOperation(	"CreateShortcut", 
								"@TargetDir@/anatomist.bat", 
								"@StartMenuDir@/Anatomist.lnk",
								"workingDirectory=@TargetDir@", 
								"iconPath=%SystemRoot%/system32/SHELL32.dll",
								"iconId=71");
    }
}