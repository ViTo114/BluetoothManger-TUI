from textual.app import App
from textual.widgets import ListItem, ListView, Label, Static
import subprocess
import os



def controllaStato() -> bool:
    stato = False

    comando = "bluetoothctl show"

    output = subprocess.run(comando, text=True, capture_output=True, shell=True )

    if "PowerState: on" in output.stdout:
        stato = True

    return stato

def statoBluetooth(app) -> None:
    app.statoCorrente = Static()

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

    app.mount(app.statoCorrente)

def menuPrincipale(app) -> None:
    app.menuPrincipale = ListView(
        ListItem(Label("Stato")),
        ListItem(Label("Connessione"))
    )

    app.menuPrincipale.styles.border = ("heavy", "white")
    app.menuPrincipale.border_title = "Bluetooth Manger"
    app.menuPrincipale.styles.width = 30
    app.menuPrincipale.styles.height = 7
    app.menuPrincipale.styles.margin = 3

    app.mount(app.menuPrincipale)

def menuStato(app) -> None:
    app.menuCorrente = 2

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

def loadingScreen(app) -> None:
    app.loadingScreen = Static("Scannign for devices ...")
    app.loadingScreen.styles.border = ("heavy", "white")

    app.mount(app.loadingScreen)

def scanDispositiviBluetooth() -> list:
    comando = "bluetoothctl --timeout 20 scan on"

    output = subprocess.run(comando, text=True, shell=True, capture_output=True)

    deviceList = output.stdout.split("\n")

    return deviceList

def menuListaDevice(app) -> None:
    app.menuCorrente = 3

    devices = scanDispositiviBluetooth()

    app.listaDevice = ListView()

    for index in devices:
        app.listaDevice.append(ListItem(Label(devices[index])))

    app.loadingScreen.remove()
    app.mount(app.listaDevice)

    app.listaDevice.focus()






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


    def on_mount(self):
        menuPrincipale(self)
        statoBluetooth(self)


    def on_key(self, event):
        if event.key == "enter" and self.menuPrincipale.index == 0 and self.menuCorrente == 1:
            self.menuPrincipale.remove()
            self.statoCorrente.remove()

            menuStato(self)

        elif event.key == "enter" and self.menuCorrente == 2 and self.menuStato.index == 0:
            os.system("bluetoothctl power on >/dev/null 2>&1")

            self.menuStato.remove()

            menuPrincipale(self)
            statoBluetooth(self)

            self.menuPrincipale.focus()

            self.menuCorrente = 1

        elif event.key == "enter" and self.menuCorrente == 2 and self.menuStato.index == 1:
            os.system("bluetoothctl power off >/dev/null 2>&1")

            self.menuStato.remove()

            menuPrincipale(self)
            statoBluetooth(self)

            self.menuPrincipale.focus()

            self.menuCorrente = 1

        elif event.key == "enter" and self.menuCorrente == 1 and self.menuPrincipale.index == 1:
            self.menuPrincipale.remove()
            self.statoCorrente.remove()

            loadingScreen(self)

            menuListaDevice(self)


if __name__ == "__main__":
    app = MyApp()
    app.run()