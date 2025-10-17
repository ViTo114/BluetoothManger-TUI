from textual import events
from textual.app import App
from textual.widgets import ListItem, ListView, Label, Static
from textual import events

import subprocess


def mostraMenuPrincipale(menu):
    menu.styles.border = ("heavy", "white")
    menu.border_title = "Bluetooth Manger"
    menu.styles.width = 30
    menu.styles.height = 7
    menu.styles.margin = 3


def controllaStato() -> bool:
    stato = False

    output = subprocess.run("bluetoothctl show", text=True, capture_output=True, shell=True )

    if "PowerState: on" in output.stdout:
        stato = True

    return stato


def mostraStatoCorrente(menu):
    stato = "Bluetooth is "

    if controllaStato():
        stato = stato + "enable"

    else:
        stato = stato + "disable"

    menu.update(stato)
    menu.styles.border = ("heavy", "white")
    menu.border_title = "Bluetooth Status"
    menu.styles.width = 30
    menu.styles.height = 5
    menu.styles.padding = 1
    menu.styles.margin = 3






# Creiamo la sotto classe di App
class MyApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self):
        self.menuPrincipale = ListView(
            ListItem(Label("Stato")),
            ListItem(Label("Connessione"))
        )
        yield self.menuPrincipale

        self.statoCorrente = Static()
        yield  self.statoCorrente



    def on_mount(self):
        mostraMenuPrincipale(self.menuPrincipale)
        mostraStatoCorrente(self.statoCorrente)

    def _on_key(self, event):
        if event.key == "escape":
            self.exit()
    

    




if __name__ == "__main__":
    app = MyApp()
    app.run()