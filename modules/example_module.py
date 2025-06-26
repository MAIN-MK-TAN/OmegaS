class Module:                                                                            # Create the Module class
    def __init__(self):
        self.name = "example_module"                                                     # Name of the module
        self.help = "This is a example module. To use it, execute 'run example_module'." # Description of the module

    def run(self):
        print("[*] Running example module... (nothing happens)")                         # The modules code
