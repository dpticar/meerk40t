import wx
from wx import aui

from meerk40t.core.element_types import elem_nodes
from meerk40t.core.units import Length, ViewPort
from meerk40t.gui.icons import icons8_lock_50, icons8_padlock_50

_ = wx.GetTranslation


def register_panel_position(window, context):
    pane = (
        aui.AuiPaneInfo()
        .Left()
        .MinSize(225, 110)
        .FloatingSize(225, 110)
        .Caption(_("Position"))
        .CaptionVisible(not context.pane_lock)
        .Name("position")
        .Hide()
    )
    pane.dock_proportion = 225
    pane.control = PositionPanel(window, wx.ID_ANY, context=context)
    pane.submenu = _("Editing")
    window.on_pane_add(pane)
    context.register("pane/position", pane)


class PositionPanel(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: PositionPanel.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        self.text_x = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.text_y = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.text_w = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.text_h = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.text_x.SetMinSize((70, 23))
        self.text_y.SetMinSize((70, 23))
        self.text_w.SetMinSize((70, 23))
        self.text_h.SetMinSize((70, 23))
        self.chk_indivdually = wx.CheckBox(self, wx.ID_ANY, _("Apply individually"))
        self.button_aspect_ratio = wx.BitmapButton(self, wx.ID_ANY, icons8_lock_50.GetBitmap(resize=25))
        self.choices = [_("mm"), _("cm"), _("inch"), _("mil"), "%"]
        self.combo_box_units = wx.ComboBox(
            self,
            wx.ID_ANY,
            choices=self.choices,
            style=wx.CB_DROPDOWN | wx.CB_READONLY,
        )
        self.combo_box_units.SetSelection(0)

        self.__set_properties()
        self.__do_layout()

        self.text_x.Bind(wx.EVT_TEXT_ENTER, self.on_text_x_enter)
        self.text_x.Bind(wx.EVT_KILL_FOCUS, self.on_text_x_focus)
        self.text_y.Bind(wx.EVT_TEXT_ENTER, self.on_text_y_enter)
        self.text_y.Bind(wx.EVT_KILL_FOCUS, self.on_text_y_focus)
        self.text_w.Bind(wx.EVT_TEXT_ENTER, self.on_text_w_enter)
        self.text_w.Bind(wx.EVT_KILL_FOCUS, self.on_text_w_focus)
        self.text_h.Bind(wx.EVT_TEXT_ENTER, self.on_text_h_enter)
        self.text_h.Bind(wx.EVT_KILL_FOCUS, self.on_text_h_focus)
        self.Bind(wx.EVT_COMBOBOX, self.on_combo_box_units, self.combo_box_units)
        self.Bind(wx.EVT_BUTTON, self.on_button_aspect_ratio, self.button_aspect_ratio)
        # end wxGlade

        self.position_aspect_ratio = True
        self.position_x = 0.0
        self.position_y = 0.0
        self.position_h = 0.0
        self.position_w = 0.0
        self.context.setting(int, "units_name", "mm")
        self.position_units = self.context.units_name
        self._update_position()

    def pane_show(self, *args):
        self.context.listen("units", self.space_changed)
        self.context.listen("emphasized", self._update_position)
        self.context.listen("modified", self._update_position)
        self.context.listen("altered", self._update_position)

    def pane_hide(self, *args):
        self.context.unlisten("units", self.space_changed)
        self.context.unlisten("emphasized", self._update_position)
        self.context.unlisten("modified", self._update_position)
        self.context.unlisten("altered", self._update_position)

    def __set_properties(self):
        # begin wxGlade: PositionPanel.__set_properties
        self.text_h.SetToolTip(_("New height (enter to apply)"))
        self.text_w.SetToolTip(_("New width (enter to apply)"))
        self.text_x.SetToolTip(_("New X-coordinate of left top corner (enter to apply)"))
        self.text_y.SetToolTip(_("New Y-coordinate of left top corner (enter to apply)"))
        self.button_aspect_ratio.SetToolTip(_("Maintain orginal aspect ratio of complete selection"))
        self.chk_indivdually.SetToolTip(_("If checked then each element will get the new value of the current field, if unchecked then the new values apply to the selection-dimensions"))
        self.button_aspect_ratio.SetSize(self.button_aspect_ratio.GetBestSize())
        self.combo_box_units.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: PositionPanel.__do_layout
        sizer_main = wx.BoxSizer(wx.VERTICAL)
        sizer_units = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Units")), wx.HORIZONTAL
        )
        sizer_h_wh = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Height:")), wx.HORIZONTAL
        )
        sizer_w = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Width:")), wx.HORIZONTAL
        )
        sizer_y = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Y:"), wx.HORIZONTAL)
        sizer_x = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "X:"), wx.HORIZONTAL)
        sizer_x.Add(self.text_x, 1, 0, 0)
        sizer_y.Add(self.text_y, 1, 0, 0)

        sizer_units.Add(self.combo_box_units, 0, 0, 0)

        sizer_h_xyu = wx.BoxSizer(wx.HORIZONTAL)
        sizer_h_xyu.Add(sizer_x, 0, 0, 0)
        sizer_h_xyu.Add(sizer_y, 0, 0, 0)
        sizer_h_xyu.Add(sizer_units, 0, 0, 0)
        sizer_main.Add(sizer_h_xyu, 0, wx.EXPAND, 0)

        sizer_w.Add(self.text_w, 1, 0, 0)
        sizer_h.Add(self.text_h, 1, wx.ALL, 0)

        sizer_h_wh.Add(sizer_w, 0, 0, 0)
        sizer_h_wh.Add(sizer_h, 0, 0, 0)
        sizer_h_wh.Add(self.button_aspect_ratio, 0, 0, 0)
        sizer_main.Add(sizer_h_wh, 0, wx.EXPAND, 0)
        sizer_main.Add(self.chk_indivdually, 0, 0, 0)

        self.SetSizer(sizer_main)
        sizer_main.Fit(self)
        self.Layout()
        # end wxGlade

    def _update_position(self, *args):
        self.update_position(True)

    def update_position(self, reset):
        more_than_one = False
        ct = 0
        for e in self.context.elements.flat(types=elem_nodes, emphasized=True):
            ct += 1
            if (ct>1):
                more_than_one = True
                break

        bounds = self.context.elements.selected_area()
        if bounds is None:
            if self.text_x.IsEnabled():
                self.text_w.Enable(False)
                self.text_h.Enable(False)
                self.text_x.Enable(False)
                self.text_y.Enable(False)
                self.button_aspect_ratio.Enable(False)
                self.chk_indivdually.SetValue(False)
                self.chk_indivdually.Enable(False)
                self.combo_box_units.Enable(False)
            if self.position_units in self.choices:
                self.combo_box_units.SetSelection(
                    self.choices.index(self.position_units)
                )
            return
        if not self.text_x.IsEnabled():
            self.text_w.Enable(True)
            self.text_h.Enable(True)
            self.text_x.Enable(True)
            self.text_y.Enable(True)
            self.combo_box_units.Enable(True)
            self.button_aspect_ratio.Enable(True)
            self.chk_indivdually.SetValue(False)
        self.chk_indivdually.Enable(more_than_one)

        if reset:
            x0, y0, x1, y1 = bounds
            # conversion = ViewPort.conversion(self.position_units)
            conversion = float(
                Length("{amount}{units}".format(units=self.position_units, amount=1))
            )
            # print ("Size: x0 = %.2f, conversion=%.5f, new=%.2f (units %s)" % (x0, conversion, x0/conversion, self.position_units))
            self.position_x = x0 / conversion
            self.position_y = y0 / conversion
            self.position_w = (x1 - x0) / conversion
            self.position_h = (y1 - y0) / conversion

        if self.position_units == "%":
            self.text_x.SetValue("%.2f" % 100)
            self.text_y.SetValue("%.2f" % 100)
            self.text_w.SetValue("%.2f" % 100)
            self.text_h.SetValue("%.2f" % 100)
        else:
            self.text_x.SetValue("%.2f" % self.position_x)
            self.text_y.SetValue("%.2f" % self.position_y)
            self.text_w.SetValue("%.2f" % self.position_w)
            self.text_h.SetValue("%.2f" % self.position_h)
        self.combo_box_units.SetSelection(self.choices.index(self.position_units))

    def space_changed(self, origin, *args):
        self.position_units = self.context.units_name
        self.update_position(True)

    def on_button_aspect_ratio(self, event):  # wxGlade: MyFrame.<event_handler>
        if self.position_aspect_ratio:
            self.button_aspect_ratio.SetBitmap(icons8_padlock_50.GetBitmap(resize=25))
        else:
            self.button_aspect_ratio.SetBitmap(icons8_lock_50.GetBitmap(resize=25))
        self.position_aspect_ratio = not self.position_aspect_ratio

    def on_text_w_enter(self, event):
        event.Skip()
        self.on_text_w_action(True)

    def on_text_w_focus(self, event):
        event.Skip()
        self.on_text_w_action(False)

    def on_text_h_enter(self, event):
        event.Skip()
        self.on_text_h_action(True)

    def on_text_h_focus(self, event):
        event.Skip()
        self.on_text_h_action(False)

    def on_text_x_enter(self, event):
        event.Skip()
        self.on_text_x_action(True)

    def on_text_x_focus(self, event):
        event.Skip()
        self.on_text_x_action(False)

    def on_text_y_enter(self, event):
        event.Skip()
        self.on_text_y_action(True)

    def on_text_y_focus(self, event):
        event.Skip()
        self.on_text_y_action(False)

    def on_text_w_action(self, force):
        original = self.position_w

        if self.position_units == "%":
            ratio_w = float(self.text_w.GetValue()) / 100.0
            w = self.position_w * ratio_w
        else:
            try:
                w = float(self.text_w.GetValue())
            except ValueError:
                try:
                    w = self.context.device.length(
                        self.text_w.GetValue(), 0, new_unit=self.position_units
                    )
                except ValueError:
                    return
        if abs(w) < 1e-8:
            self.text_w.SetValue(str(self.position_w))
            return
        self.position_w = w

        if self.position_aspect_ratio:
            if abs(original) < 1e-8:
                self.update_position(True)
                return
            self.position_h *= self.position_w / original
            self.update_position(False)

        if not force:
            return

        if self.chk_indivdually.GetValue():
            for elem in self.context.elements.flat(types=elem_nodes, emphasized=True):
                _bb = elem.bounds
                bb = [_bb[0], _bb[1], _bb[2], _bb[3]]
                new_w = float(Length("{value}{unit}".format(value=self.position_w, unit=self.position_units)))

                try:
                    scalex = new_w / (bb[2]-bb[0])
                    scaley = 1.0
                except ZeroDivisionError:
                    continue
                # print("Old=%.1f, new=%.1f, sx=%.1f" % ((bb[2]-bb[0]), new_w, scalex))

                bb[2] = bb[0] + (bb[2]-bb[0]) * scalex

                elem.matrix.post_scale(scalex, scaley, bb[0], bb[1])
                elem._bounds = bb
                elem.modified()
        else:
            cmd = "resize %f%s %f%s %f%s %f%s\n" % (
                    self.position_x,
                    self.position_units,
                    self.position_y,
                    self.position_units,
                    self.position_w,
                    self.position_units,
                    self.position_h,
                    self.position_units,
                )
            self.context(cmd)
        self.update_position(True)

    def on_text_h_action(self, force):
        original = self.position_h
        if self.position_units == "%":
            ratio_w = float(self.text_h.GetValue()) / 100.0
            h = self.position_h * ratio_w
        else:
            try:
                h = float(self.text_h.GetValue())
            except ValueError:
                try:
                    h = self.context.device.length(
                        self.text_h.GetValue(), 1, new_units=self.position_units
                    )
                except ValueError:
                    return
        if abs(h) < 1e-8:
            self.text_h.SetValue(str(self.position_h))
            return

        self.position_h = h
        if self.position_aspect_ratio:
            if abs(original) < 1e-8:
                self.update_position(True)
                return
            self.position_w *= self.position_h / original
            self.update_position(False)

        if not force:
            return

        if self.chk_indivdually.GetValue():
            for elem in self.context.elements.flat(types=elem_nodes, emphasized=True):
                _bb = elem.bounds
                bb = [_bb[0], _bb[1], _bb[2], _bb[3]]
                new_h = float(Length("{value}{unit}".format(value=self.position_h, unit=self.position_units)))

                try:
                    scalex = 1.0
                    scaley = new_h / (bb[3] - bb[1])
                except ZeroDivisionError:
                    continue

                # print("Old=%.1f, new=%.1f, sy=%.1f" % ((bb[3]-bb[1]), new_h, scaley))

                bb[3] = bb[1] + (bb[3]-bb[1]) * scaley

                elem.matrix.post_scale(scalex, scaley, bb[0], bb[1])
                elem._bounds = bb
                elem.modified()
        else:
            cmd = "resize %f%s %f%s %f%s %f%s\n" % (
                    self.position_x,
                    self.position_units,
                    self.position_y,
                    self.position_units,
                    self.position_w,
                    self.position_units,
                    self.position_h,
                    self.position_units,
                )
            self.context(cmd)
        self.update_position(True)

    def on_text_x_action(self, force):
        try:
            self.position_x = float(self.text_x.GetValue())
        except ValueError:
            try:
                self.position_x = self.context.device.length(
                    self.text_h.GetValue(), 1, new_units=self.position_units
                )
            except ValueError:
                return

        if not force:
            return

        if self.chk_indivdually.GetValue():
            for elem in self.context.elements.flat(types=elem_nodes, emphasized=True):
                _bb = elem.bounds
                bb = [_bb[0], _bb[1], _bb[2], _bb[3]]
                newx = float(Length("{value}{unit}".format(value=self.position_x, unit=self.position_units)))
                dx = newx - bb[0]
                dy = 0
                # print("Old=%.1f, new=%.1f, dx=%.1f" % (bb[0], newx, dx))

                oldw = bb[2]-bb[0]
                bb[0] = newx
                bb[2] = newx + oldw
                elem.matrix.post_translate(dx, dy)
                elem._bounds = bb
                elem.modified()
        else:
            self.context(
                "resize %f%s %f%s %f%s %f%s\n"
                % (
                    self.position_x,
                    self.position_units,
                    self.position_y,
                    self.position_units,
                    self.position_w,
                    self.position_units,
                    self.position_h,
                    self.position_units,
                )
            )
        self.update_position(True)

    def on_text_y_action(self, force):
        try:
            self.position_y = float(self.text_y.GetValue())
        except ValueError:
            try:
                self.position_y = self.context.device.length(
                    self.text_h.GetValue(), 1, new_units=self.position_units
                )
            except ValueError:
                return

        if not force:
            return

        if self.chk_indivdually.GetValue():
            for elem in self.context.elements.flat(types=elem_nodes, emphasized=True):
                _bb = elem.bounds
                bb = [_bb[0], _bb[1], _bb[2], _bb[3]]
                newy = float(Length("{value}{unit}".format(value=self.position_y, unit=self.position_units)))
                dy = newy - bb[1]
                dx = 0
                # print("Old=%.1f, new=%.1f, dy=%.1f" % (bb[1], newy, dy))

                oldh = bb[3]-bb[1]
                bb[1] = newy
                bb[3] = newy + oldh

                elem.matrix.post_translate(dx, dy)
                elem._bounds = bb
                elem.modified()
        else:
            self.context(
                "resize %f%s %f%s %f%s %f%s\n"
                % (
                    self.position_x,
                    self.position_units,
                    self.position_y,
                    self.position_units,
                    self.position_w,
                    self.position_units,
                    self.position_h,
                    self.position_units,
                )
            )
        self.update_position(True)

    def on_combo_box_units(self, event):
        self.position_units = self.choices[self.combo_box_units.GetSelection()]
        self.update_position(True)
