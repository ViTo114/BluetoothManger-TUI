import asyncio
from textual.app import App
from textual.await_complete import AwaitComplete
from textual.widgets import ListItem, ListView, Label, Static, ProgressBar
import subprocess
import os



def controllaStato() -> bool:
    stato = False

    comandoShow = "bluetoothctl show"

    outputShow = subprocess.run(comandoShow, text=True, capture_output=True, shell=True )


    if "PowerState: on" in outputShow.stdout:
        stato = True

    return stato

def statoBluetooth(app) -> None:
    app.statoCorrente = Static()

    comandoInfo = "bluetoothctl info"

    outputInfo = subprocess.run(comandoInfo, text=True, capture_output=True, shell=True)


    stato = "Bluetooth is "

    if controllaStato() and "Missing" in outputInfo.stdout:
        stato = stato + "enable"

    elif controllaStato() and "Missing" not in outputInfo.stdout:
        righe = outputInfo.stdout.split("\n")

        for riga in righe:
            if "Name" in riga:
                elementi = riga.split(":")
                stato = "Connected to\n" + elementi[1].strip()
            break

    else:
        stato = stato + "disable"

    app.statoCorrente.update(stato)
    app.statoCorrente.styles.border = ("heavy", "white")
    app.statoCorrente.border_title = "Bluetooth Status"
    app.statoCorrente.styles.width = 30

    if "Connected" in stato:
        app.statoCorrente.styles.height = 6
    else:
        app.statoCorrente.styles.height = 5

    app.statoCorrente.styles.padding = 1
    app.statoCorrente.styles.margin = 3

    app.mount(app.statoCorrente)

def menuPrincipale(app) -> None:
    app.menuCorrente =1

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

    app.menuPrincipale.focus()

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

def scannigLoadingScreen(app) -> None:
    app.scannigLoadingScreen = ProgressBar()
    app.scannigLoadingScreen.styles.border = ("heavy", "white")
    app.scannigLoadingScreen.border_title = "Scanning for devices..."

    app.scannigLoadingScreen.styles.width = 30
    app.scannigLoadingScreen.styles.height = 5
    app.scannigLoadingScreen.styles.padding = 1
    app.scannigLoadingScreen.styles.margin = 3

    app.mount(app.scannigLoadingScreen)

def connectonLoadingScreen(app) -> None:
    app.connectionLoadingScreen = ProgressBar()
    app.connectionLoadingScreen.styles.border = ("heavy", "white")
    app.connectionLoadingScreen.border_title = "Connecting..."

    app.connectionLoadingScreen.styles.width = 30
    app.connectionLoadingScreen.styles.height = 5
    app.connectionLoadingScreen.styles.padding = 1
    app.connectionLoadingScreen.styles.margin = 3

    app.mount(app.scannigLoadingScreen)

def scanDispositiviBluetooth() -> list:
    comando = "bluetoothctl --timeout 10 scan on"

    output = subprocess.run(comando, text=True, shell=True, capture_output=True)

    deviceList = output.stdout.split("\n")

    return deviceList

def cleanDevicesList(devicesList, app) -> list:
    listDevices = []

    for element in devicesList.copy():
        if "NEW" not in element:
            devicesList.remove(element)

    for element in devicesList:
        component = element.split(" ")

        nome = ""

        for i in range(len(component)):

            if i >= 3:
                nome = nome + " " + component[i]

        listDevices.append(nome)
        app.listDevicesAddress.append(component[2])

    return listDevices

async def menuListaDevice(app) -> None:
    app.menuCorrente = 3

    devices = await asyncio.to_thread(scanDispositiviBluetooth)

    itemList = []

    for device in cleanDevicesList(devices, app):
        itemList.append(ListItem(Label(device)))

    app.listaDevice = ListView(*itemList)

    app.listaDevice.styles.border = ("heavy", "white")
    app.listaDevice.border_title = "Select the device to connect to"
    app.listaDevice.styles.width = 50
    app.listaDevice.styles.height = 20
    app.listaDevice.styles.padding = 1
    app.listaDevice.styles.margin = 3

    app.scannigLoadingScreen.remove()
    await app.mount(app.listaDevice)
    await menuInfoScan(app)


def warningMessage(app):
    app.menuCorrente = 4

    app.warning= Static("ATTENTION: you must enable Bluetooth to connect to a device. \n \n Press enter to go back")

    app.warning.styles.width = 30
    app.warning.styles.height = 10
    app.warning.styles.padding = 1
    app.warning.styles.margin = 3

    app.mount(app.warning)

def connectToADevice() -> bool:
    esito = False

    address = app.listDevicesAddress[app.listaDevice.index]

    pairComand = "bluetoothctl pair " + address
    connectionComand = "bluetoothctl connect " + address

    outputPair = subprocess.run(pairComand, text=True, capture_output=True, shell=True)
    outputConnection = subprocess.run(connectionComand, text=True, capture_output=True, shell=True)

    if "successful" in outputPair.stdout and "successful" in outputConnection.stdout :
        esito = True

    return esito

async def handlerConnection(app) -> None:
    app.menuCorrente = 5

    app.esitoConnessione = Static()

    esito  = await asyncio.to_thread(connectToADevice)

    if esito == True:
        stato = "Connection successful"

    else:
        stato = "Error during connection"

    app.connectionLoadingScreen.remove()

    app.esitoConnessione.update(stato)

    app.esitoConnessione.styles.width = 30
    app.esitoConnessione.styles.height = 5
    app.esitoConnessione.styles.padding = 1
    app.esitoConnessione.styles.margin = 3

    app.mount(app.esitoConnessione)

def menuInfoScan(app) -> None:
    app.shortcut = Static("Press 's' to restart the scan \nPress 'esc' to return to main menu")

    app.shortcut.styles.border = ("heavy", "white")
    app.shortcut.border_title = "Shortcut info"

    app.shortcut.styles.width = 40
    app.shortcut.styles.height = 6
    app.shortcut.styles.padding = 1
    app.shortcut.styles.margin = 3

    app.mount(app.shortcut)
    app.listaDevice.focus()


# Creiamo la sotto classe di App
class MyApp(App):

    def __init__(self):
        super().__init__()
        self.menuCorrente = 1
        self.listDevicesAddress = []

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

        elif event.key == "enter" and self.menuCorrente == 1 and self.menuPrincipale.index == 1 and controllaStato()==False:
            self.menuPrincipale.remove()
            self.statoCorrente.remove()

            warningMessage(self)


        elif event.key == "enter" and self.menuCorrente == 4:
            self.warning.remove()

            menuPrincipale(self)
            statoBluetooth(self)


        elif event.key == "enter" and self.menuCorrente == 1 and self.menuPrincipale.index == 1:
            self.menuPrincipale.remove()
            self.statoCorrente.remove()

            scannigLoadingScreen(self)

            asyncio.create_task(menuListaDevice(self))

        elif event.key == "escape" and self.menuCorrente == 3:
            self.listaDevice.remove()
            self.shortcut.remove()

            menuPrincipale(self)
            statoBluetooth(self)

        elif event.key=="s" and self.menuCorrente ==3:
            self.listaDevice.remove()
            self.shortcut.remove()

            scannigLoadingScreen(self)
            asyncio.create_task(menuListaDevice(self))


        elif event.key == "enter" and self.menuCorrente == 3:
            self.listaDevice.remove()
            self.shortcut.remove()

            connectonLoadingScreen(self)

            asyncio.create_task(handlerConnection(self))


        elif event.key == "enter" and self.menuCorrente == 5:
            connectonLoadingScreen(self)
            self.esitoConnessione.remove()

            menuPrincipale(self)
            statoBluetooth(self)



if __name__ == "__main__":
    app = MyApp()
    app.run()