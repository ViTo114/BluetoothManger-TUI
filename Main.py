from textual.app import App
from textual.widgets import ListItem, ListView, Label, Static
import subprocess




def controllaStato() -> bool:
    stato = False

    output = subprocess.run("bluetoothctl show", text=True, capture_output=True, shell=True )

    if "PowerState: on" in output.stdout:
        stato = True

    return stato










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
        self.menuPrincipale.styles.border = ("heavy", "white")
        self.menuPrincipale.border_title = "Bluetooth Manger"
        self.menuPrincipale.styles.width = 30
        self.menuPrincipale.styles.height = 7
        self.menuPrincipale.styles.margin = 3

        stato = "Bluetooth is "

        if controllaStato():
            stato = stato + "enable"

        else:
            stato = stato + "disable"

        self.statoCorrente.update(stato)
        self.statoCorrente.styles.border = ("heavy", "white")
        self.statoCorrente.border_title = "Bluetooth Status"
        self.statoCorrente.styles.width = 30
        self.statoCorrente.styles.height = 5
        self.statoCorrente.styles.padding = 1
        self.statoCorrente.styles.margin = 3


    async def on_key(self, event):
        if event.key == "enter" and self.menuPrincipale.index == 0:
            self.menuCorrente = 2

            self.menuPrincipale.remove()
            self.statoCorrente.remove()

            self.menuStato = (ListView(
            ListItem(Label("ON")),
            ListItem(Label("OFF"))))

            self.menuStato.styles.border = ("heavy", "white")
            self.menuStato.border_title = "Change Bluetooth Status"
            self.menuStato.styles.width = 30
            self.menuStato.styles.height = 7
            self.menuStato.styles.margin = 3


            stato = "Bluetooth is "

            if controllaStato():
                stato = stato + "enable"

            else:
                stato = stato + "disable"

            self.statoCorrente.update(stato)
            self.statoCorrente.styles.border = ("heavy", "white")
            self.statoCorrente.border_title = "Bluetooth Status"
            self.statoCorrente.styles.width = 30
            self.statoCorrente.styles.height = 5
            self.statoCorrente.styles.padding = 1
            self.statoCorrente.styles.margin = 3

            await self.mount(self.menuStato)
            await self.mount(self.statoCorrente)

            self.menuStato.focus()







if __name__ == "__main__":
    app = MyApp()
    app.run()