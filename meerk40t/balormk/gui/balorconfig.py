import wx

from meerk40t.gui.choicepropertypanel import ChoicePropertyPanel
from meerk40t.gui.icons import icons8_administrative_tools_50
from meerk40t.gui.mwindow import MWindow

_ = wx.GetTranslation


class BalorConfiguration(MWindow):
    def __init__(self, *args, **kwds):
        super().__init__(374, 734, *args, **kwds)
        self.context = self.context.device
        _icon = wx.NullIcon
        _icon.CopyFromBitmap(icons8_administrative_tools_50.GetBitmap())
        self.SetIcon(_icon)
        self.SetTitle(_(_("Balor-Configuration")))

        self.notebook_main = wx.aui.AuiNotebook(
            self,
            -1,
            style=wx.aui.AUI_NB_TAB_EXTERNAL_MOVE
            | wx.aui.AUI_NB_SCROLL_BUTTONS
            | wx.aui.AUI_NB_TAB_SPLIT
            | wx.aui.AUI_NB_TAB_MOVE,
        )

        self.panel_main = ChoicePropertyPanel(
            self, wx.ID_ANY, context=self.context, choices="balor"
        )
        self.panel_red = ChoicePropertyPanel(
            self, wx.ID_ANY, context=self.context, choices="balor-redlight"
        )
        self.panel_global = ChoicePropertyPanel(
            self, wx.ID_ANY, context=self.context, choices="balor-global"
        )
        self.panel_timing = ChoicePropertyPanel(
            self, wx.ID_ANY, context=self.context, choices="balor-global-timing"
        )
        self.panel_extra = ChoicePropertyPanel(
            self, wx.ID_ANY, context=self.context, choices="balor-extra"
        )
        self.notebook_main.AddPage(self.panel_main, _("Balor"))
        self.notebook_main.AddPage(self.panel_red, _("Redlight"))
        self.notebook_main.AddPage(self.panel_global, _("Global"))
        self.notebook_main.AddPage(self.panel_timing, _("Timings"))
        self.notebook_main.AddPage(self.panel_extra, _("Extras"))
        self.Layout()

        self.add_module_delegate(self.panel_main)
        self.add_module_delegate(self.panel_red)
        self.add_module_delegate(self.panel_global)
        self.add_module_delegate(self.panel_timing)
        self.add_module_delegate(self.panel_extra)

    def window_close(self):
        self.context.unlisten("flip_x", self.on_viewport_update)
        self.context.unlisten("flip_y", self.on_viewport_update)

    def window_open(self):
        self.context.listen("flip_x", self.on_viewport_update)
        self.context.listen("flip_y", self.on_viewport_update)

    def on_viewport_update(self, origin, *args):
        self.context("viewport_update\n")

    def window_preserve(self):
        return False
