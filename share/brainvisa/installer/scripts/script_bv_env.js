function Component()
{
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (installer.value("os") === "win") {
		component.addOperation(	"CreateShortcut", 
								"http://www.brainvisa.info", 
								"@StartMenuDir@/BrainVISA Website.lnk",
								"workingDirectory=@TargetDir@", 
								"iconPath=%SystemRoot%/system32/SHELL32.dll",
								"iconId=91");
    }
}