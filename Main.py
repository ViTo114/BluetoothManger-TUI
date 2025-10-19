from textual.app import App
from textual.widgets import ListItem, ListView, Label, Static
import subprocess
import os



def controllaStato() -> bool:
    stato = False

    output = subprocess.run("bluetoothctl show", text=True, capture_output=True, shell=True )

    if "PowerState: on" in output.stdout:
        stato = True

    return stato

def mostraStato(app) -> None:
    stato = "Bluetooth is "

    if controllaStato():
        stato = stato + "enable"

    else:
        stato = stato + "disable"

    app.statoCorrente.update(stato)
    app.statoCorrente.styles.border = ("heavy", "white")
    app.statoCorrente.border_title = "Bluetooth Status"
    app.statoCorrente.styles.width = 30
    app.statoCorrente.styles.height = 5
    app.statoCorrente.styles.padding = 1
    app.statoCorrente.styles.margin = 3

def menuPrincipale(app) -> None:
    app.menuPrincipale.styles.border = ("heavy", "white")
    app.menuPrincipale.border_title = "Bluetooth Manger"
    app.menuPrincipale.styles.width = 30
    app.menuPrincipale.styles.height = 7
    app.menuPrincipale.styles.margin = 3

def mostraMenuStato(app) -> None:
    app.menuCorrente = 2

    app.menuPrincipale.display = False
    app.statoCorrente.display = False

    app.menuStato = (ListView(
        ListItem(Label("ON")),
        ListItem(Label("OFF"))))

    app.menuStato.styles.border = ("heavy", "white")
    app.menuStato.border_title = "Change Bluetooth Status"
    app.menuStato.styles.width = 30
    app.menuStato.styles.height = 7
    app.menuStato.styles.margin = 3

    app.mount(app.menuStato)

    app.menuStato.focus()





# Creiamo la sotto classe di App
class MyApp(App):

    def __init__(self):
        super().__init__()
        self.menuCorrente = 1

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
        menuPrincipale(self)
        mostraStato(self)


    def on_key(self, event):
        if event.key == "enter" and self.menuPrincipale.index == 0 and self.menuCorrente == 1:
            mostraMenuStato(self)

        elif event.key == "enter" and self.menuCorrente == 2 and self.menuStato.index == 0:
            os.system("bluetoothctl power on >/dev/null 2>&1")

            self.menuStato.remove()
            self.menuPrincipale.display = True
            mostraStato(self)
            self.statoCorrente.display = True

            self.menuPrincipale.focus()

            self.menuCorrente = 1

        elif event.key == "enter" and self.menuCorrente == 2 and self.menuStato.index == 1:
            os.system("bluetoothctl power off >/dev/null 2>&1")

            self.menuStato.remove()
            self.menuPrincipale.display = True
            mostraStato(self)
            self.statoCorrente.display = True

            self.menuPrincipale.focus()

            self.menuCorrente = 1



if __name__ == "__main__":
    app = MyApp()
    app.run()