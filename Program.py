
class Program:

    def __init__(self, **kwargs):

        self.user32 = kwargs.get("user32")

        self.name = kwargs.get("name")
        self.identifier = kwargs.get("identifier")
        self.handle = self.user32.FindWindowW(None, self.identifier)

        self.is_visible = True

    def minimize(self):
        self.user32.ShowWindow(self.handle, 6)
        self.is_visible = False

    def maximize(self):
        self.user32.ShowWindow(self.handle, 9)
        self.is_visible = True

    def toggle_visibility(self):
        if self.is_visible:
            self.minimize()
            self.is_visible = False
        else:
            self.maximize()
            self.is_visible = True

        # self.is_visible = not self.is_visible

    def move(self, x, y, height, width):
        self.user32.MoveWindow(self.handle, x, y, height, width, True)
