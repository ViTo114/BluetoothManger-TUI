from textual.app import App
from textual.widgets import ListItem, ListView, Label


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
            ListItem(Label("Connessione")),
        )
        yield self.menuPrincipale

    def on_mount(self):
        self.menuPrincipale.styles.border = ("heavy", "white")
        self.menuPrincipale.border_title = "Bluetooth Manger"
        self.menuPrincipale.styles.width = 30
        self.menuPrincipale.styles.height = 7
        self.menuPrincipale.styles.padding = 1

    




if __name__ == "__main__":
    app = MyApp()
    app.run()