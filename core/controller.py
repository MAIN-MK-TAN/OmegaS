import os
import importlib.util
import json

MODULES_DIR = "../modules"
PAYLOADS_DIR = "../payloads"

class OmegaShell:
    def __init__(self):
        self.modules = self.load_modules()
        self.payloads = self.load_payloads()
        self.active_module = None
        self.active_payload = None

    def load_modules(self):
        modules = {}
        for file in os.listdir(MODULES_DIR):
            if file.endswith(".py") and not file.startswith("__"):
                name = file[:-3]
                path = os.path.join(MODULES_DIR, file)
                spec = importlib.util.spec_from_file_location(name, path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                modules[name] = mod.Module()
        return modules

    def load_payloads(self):
        payloads = {}
        for file in os.listdir(PAYLOADS_DIR):
            if file.endswith(".json"):
                name = file[:-5]
                path = os.path.join(PAYLOADS_DIR, file)
                with open(path, 'r') as f:
                    payload_data = json.load(f)
                    payloads[name] = payload_data
        return payloads

    def start(self):
        print("OmegaS C2 Framework")
        while True:
            cmd = input("OmegaS > ").strip()
            if not cmd:
                continue
            if cmd == "exit":
                break
            elif cmd == "help":
                print("Commands:\nshow\nuse\nrun\ntestpayload\nexit")
            elif cmd.startswith("help "):
                if cmd == "help show":
                    print("Syntax:\nshow {arg1}\n\nAvailable arguments: modules, payloads")
            elif cmd == "show":
                print("Please use 'help show' (or read the code) for intel on how to use 'show'.")
            elif cmd.startswith("show "):
                arg = cmd.split(" ", 1)[1]
                if arg == "modules":
                    for name in self.modules:
                        print(f"- {name}")
                elif arg == "payloads":
                    for name in self.payloads:
                        print(f"- {name}")
                else:
                    print("Invalid argument.")
            elif cmd.startswith("use "):
                parts = cmd.split(" ", 2)
                if len(parts) != 3:
                    print("Invalid use syntax. Use: use module <name> or use payload <name>")
                    continue
                _, typ, name = parts
                if typ == "module":
                    if name in self.modules:
                        self.active_module = self.modules[name]
                        print(f"Loaded module: {name}")
                    else:
                        print(f"Module {name} not found.")
                elif typ == "payload":
                    if name in self.payloads:
                        self.active_payload = self.payloads[name]
                        print(f"Loaded payload: {name}")
                    else:
                        print(f"Payload {name} not found.")
                else:
                    print("Invalid type. Run 'help use' for help.")
            elif cmd == "run":
                if self.active_module:
                    self.active_module.run()
                else:
                    print("No module loaded.")
            elif cmd == "testpayload":
                if self.active_payload:
                    print(json.dumps(self.active_payload, indent=2))
                else:
                    print("No payload loaded.")
            else:
                print("Unknown command.")

if __name__ == "__main__":
    shell = OmegaShell()
    shell.start()