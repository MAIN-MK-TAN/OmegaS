# OmegaS C2 Skeleton

This is a modular shell-like interface intended to be extended.

## Structure

- `core/controller.py`: main shell logic
- `modules/`: drop-in Python modules
    - Each must define a `Module` class with a `run()` method

## Usage

- `show modules`: list modules
- `use <name>`: select a module
- `run`: execute the selected module
- `exit`: quit

## Adding a Module

1. Create a module, e.g. `modules/my_module.py`
2. Define a class `Module` with `run(self)` and `__init__(self)` methods
3. Define `self.name` and `self.help` as children of `__init__(self)`
4. Put your logic/code in `run(self)`

Example:
```python
class Module:                                                                            # Create the Module class
    def __init__(self):
        self.name = "example_module"                                                     # Name of the module
        self.help = "This is a example module. To use it, execute 'run example_module'." # Description of the module

    def run(self):
        print("[*] Running example module... (nothing happens)")                         # The modules code
```