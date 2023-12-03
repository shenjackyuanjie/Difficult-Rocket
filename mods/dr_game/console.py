from . import DR_mod_runtime
from Difficult_Rocket.main import Console

if DR_mod_runtime.use_DR_rust:
    from .Difficult_Rocket_rs import Console_rs


class RustConsole(Console):
    name = "Rust stdin Console"

    running: bool = False
    console: Console_rs

    def start(self):
        self.console.start()

    def stop(self):
        return self.console.stop()

    def init(self, **kwargs) -> None:
        self.console = Console_rs()

    def get_command(self) -> str:
        return self.console.get_command()

    def new_command(self) -> None:
        self.console.new_command()
