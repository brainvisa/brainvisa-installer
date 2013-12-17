function Component()
{
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (installer.value("os") === "win") {
        component.addOperation(	"CreateShortcut", 
								"@TargetDir@/BrainVISA.bat", 
								"@StartMenuDir@/BrainVISA.lnk",
								"workingDirectory=@TargetDir@", 
								"iconPath=%SystemRoot%/system32/SHELL32.dll",
								"iconId=71");
    }
}