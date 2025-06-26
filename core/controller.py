import os
import importlib

MODULES_DIR = "modules"

class OmegaShell:
    def __init__(self):
        self.modules = self.load_modules()
        self.active_module = None

    def load_modules(self):
        modules = {}
        for file in os.listdir(MODULES_DIR):
            if file.endswith(".py") and not file.startswith("__"):
                name = file[:-3]
                mod = importlib.import_module(f"{MODULES_DIR}.{name}")
                modules[name] = mod.Module()
        return modules

    def start(self):
        print("OmegaS C2 Framework [empty scaffold]")
        while True:
            cmd = input("OmegaS > ").strip()
            if not cmd: continue

            if cmd == "exit":
                break
            elif cmd == "show modules":
                for name in self.modules:
                    print(f"- {name}")
            elif cmd.startswith("use "):
                name = cmd[4:]
                if name in self.modules:
                    self.active_module = self.modules[name]
                    print(f"Loaded module: {name}")
                else:
                    print("Module not found.")
            elif cmd == "run" and self.active_module:
                self.active_module.run()
            else:
                print("Unknown command.")

if __name__ == "__main__":
    shell = OmegaShell()
    shell.start()
