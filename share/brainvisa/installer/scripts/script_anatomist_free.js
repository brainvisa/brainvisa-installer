function Component()
{
    // constructor
}

Component.prototype.createOperations = function()
{
	try {
		// call the base create operations function
		component.createOperations();
	} catch (e) {
		print(e);
	}
}
