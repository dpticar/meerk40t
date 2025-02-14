from meerk40t.gui.scene.sceneconst import (
    HITCHAIN_DELEGATE_AND_HIT,
    RESPONSE_CHAIN,
    RESPONSE_CONSUME,
)
from meerk40t.gui.scene.widget import Widget
from meerk40t.svgelements import Matrix, Viewbox


class SceneSpaceWidget(Widget):
    """
    SceneSpaceWidget contains two sections:
    Interface: Drawn on top, uses no matrix.
    Scene: Drawn at a particular scale relative to the zoom-pan scene.
    """

    def __init__(self, scene):
        Widget.__init__(self, scene, all=True)
        self._view = None
        self._frame = None
        self.aspect = False

        self.interface_widget = Widget(scene)
        self.scene_widget = Widget(scene)
        self.add_widget(-1, self.interface_widget)
        self.add_widget(-1, self.scene_widget)
        self.last_position = None
        self._previous_zoom = None
        self._placement_event = None
        self._placement_event_type = None

    def hit(self):
        """
        If any event captures the events they take priority. But, if nothing is hit, then the events
        should be dealt with here. These are mostly zoom and pan events.
        """
        return HITCHAIN_DELEGATE_AND_HIT

    @property
    def pan_factor(self):
        pf = self.scene.context.pan_factor
        if self.scene.context.mouse_pan_invert:
            pf = -pf
        return pf

    @property
    def zoom_factor(self):
        zf = self.scene.context.zoom_factor
        if self.scene.context.mouse_zoom_invert:
            zf = -zf
        zf += 1.0
        return zf

    @property
    def zoom_forward(self):
        return self.zoom_factor

    @property
    def zoom_backwards(self):
        zf = self.zoom_factor
        if zf == 0:
            return 1.0
        return 1.0 / zf

    def event(self, window_pos=None, space_pos=None, event_type=None):
        """
        Process the zooming and panning of otherwise unhit-widget events.

        If nothing was otherwise hit by the event, we process the scene manipulation events
        """

        if event_type == "hover":
            return RESPONSE_CHAIN
        if self.aspect:
            return RESPONSE_CONSUME

        if event_type == "wheelup" and self.scene.context.mouse_wheel_pan:
            self.scene_widget.matrix.post_translate(0, -self.pan_factor)
        elif event_type == "wheeldown" and self.scene.context.mouse_wheel_pan:
            self.scene_widget.matrix.post_translate(0, self.pan_factor)
        elif event_type == "wheelup" or event_type == "wheelup_ctrl":
            self.scene_widget.matrix.post_scale(
                self.zoom_forward, self.zoom_forward, space_pos[0], space_pos[1]
            )
            self.scene.request_refresh()
            return RESPONSE_CONSUME
        # elif event_type == "zoom-in":
        #     self.scene_widget.matrix.post_scale(self.zoom_forward, self.zoom_forward, space_pos[0], space_pos[1])
        #     self.scene.request_refresh()
        #     return RESPONSE_CONSUME
        elif event_type == "rightdown+alt":
            self._previous_zoom = 1.0
            self._placement_event = space_pos
            self._placement_event_type = "zoom"
            return RESPONSE_CONSUME
        elif event_type == "rightdown+control":
            self._previous_zoom = 1.0
            self._placement_event = space_pos
            self._placement_event_type = "pan"
            return RESPONSE_CONSUME
        elif event_type == "rightup":
            self._previous_zoom = None
            self._placement_event = None
            self._placement_event_type = None
        elif event_type == "wheeldown" or event_type == "wheeldown_ctrl":
            self.scene_widget.matrix.post_scale(
                self.zoom_backwards, self.zoom_backwards, space_pos[0], space_pos[1]
            )
            self.scene.request_refresh()
            return RESPONSE_CONSUME
        # elif event_type == "zoom-out":
        #     self.scene_widget.matrix.post_scale(
        #         self.zoom_backwards, self.zoom_backwards, space_pos[0], space_pos[1]
        #     )
        #     self.scene.request_refresh()
        #     return RESPONSE_CONSUME
        elif event_type == "wheelleft":
            self.scene_widget.matrix.post_translate(self.pan_factor, 0)
            self.scene.request_refresh()
            return RESPONSE_CONSUME
        elif event_type == "wheelright":
            self.scene_widget.matrix.post_translate(-self.pan_factor, 0)
            self.scene.request_refresh()
            return RESPONSE_CONSUME
        elif event_type == "middledown":
            return RESPONSE_CONSUME
        elif event_type == "middleup":
            return RESPONSE_CONSUME
        elif event_type == "gesture-start":
            self._previous_zoom = 1.0
            return RESPONSE_CONSUME
        elif event_type == "gesture-end":
            self._previous_zoom = None
            return RESPONSE_CONSUME
        elif event_type == "lost":
            return RESPONSE_CONSUME
        elif str(event_type).startswith("zoom "):
            if self._previous_zoom is None:
                return RESPONSE_CONSUME
            try:
                zoom = float(event_type.split(" ")[1])
            except Exception:
                return RESPONSE_CONSUME

            zoom_change = zoom / self._previous_zoom
            self.scene_widget.matrix.post_scale(
                zoom_change, zoom_change, space_pos[0], space_pos[1]
            )
            self.scene_widget.matrix.post_translate(space_pos[4], space_pos[5])
            self._previous_zoom = zoom
            self.scene.request_refresh()

            return RESPONSE_CONSUME
        elif str(event_type).startswith("magnify "):
            magnify = float(event_type.split(" ")[1])
            self.scene_widget.matrix.post_scale(
                magnify, magnify, space_pos[0], space_pos[1]
            )
            self.scene_widget.matrix.post_translate(space_pos[4], space_pos[5])
            self.scene.context.signal("refresh_scene", 0)

            return RESPONSE_CONSUME

        # Movement
        if self._placement_event_type is None:
            self.scene_widget.matrix.post_translate(space_pos[4], space_pos[5])
            self.scene.request_refresh()
        elif self._placement_event_type == "zoom":
            from math import e

            p = (
                space_pos[0]
                - self._placement_event[0]
                + space_pos[1]
                - self._placement_event[1]
            )
            p /= 250.0
            if self._previous_zoom is not None:
                zoom_factor = e**p
                zoom_change = zoom_factor / self._previous_zoom
                self._previous_zoom = zoom_factor
                self.scene_widget.matrix.post_scale(
                    zoom_change,
                    zoom_change,
                    self._placement_event[0],
                    self._placement_event[1],
                )
            self.scene.request_refresh()
        elif self._placement_event_type == "pan":
            pan_factor_x = -(space_pos[0] - self._placement_event[0]) / 10
            pan_factor_y = -(space_pos[1] - self._placement_event[1]) / 10
            self.scene_widget.matrix.post_translate(pan_factor_x, pan_factor_y)
            self.scene.request_refresh()
        return RESPONSE_CONSUME

    def set_view(self, x, y, w, h, preserve_aspect=None):
        self._view = Viewbox(
            "%d %d %d %d" % (x, y, w, h),
            preserve_aspect,
        )
        self.aspect_matrix()

    def set_frame(self, x, y, w, h):
        self._frame = Viewbox("%d %d %d %d" % (x, y, w, h))
        self.aspect_matrix()

    def set_aspect(self, aspect=True):
        self.aspect = aspect
        self.aspect_matrix()

    def aspect_matrix(self):
        """
        Specifically view the scene with the given Viewbox.
        """
        if self._frame and self._view and self.aspect:
            self.scene_widget.matrix = Matrix(self._view.transform(self._frame))

    def focus_position_scene(self, scene_point, scene_size):
        """
        Focus on the specific point within the scene.
        """
        window_width, window_height = self.scene.ClientSize
        scale_x = self.get_scale_x()
        scale_y = self.get_scale_y()
        self.scene_matrix_reset()
        self.scene_post_pan(-scene_point[0], -scene_point[1])
        self.scene_post_scale(scale_x, scale_y)
        self.scene_post_pan(window_width / 2.0, window_height / 2.0)

    def focus_viewport_scene(
        self, new_scene_viewport, scene_size, buffer=0.0, lock=True
    ):
        """
        Focus on the given viewport in the scene.

        @param new_scene_viewport: Viewport to have after this process within the scene.
        @param scene_size: Size of the scene in which this viewport is active.
        @param buffer: Amount of buffer around the edge of the new viewport.
        @param lock: lock the scalex, scaley.
        @return:
        """
        window_width, window_height = scene_size
        left = new_scene_viewport[0]
        top = new_scene_viewport[1]
        right = new_scene_viewport[2]
        bottom = new_scene_viewport[3]
        viewport_width = right - left
        viewport_height = bottom - top

        left -= viewport_width * buffer
        right += viewport_width * buffer
        top -= viewport_height * buffer
        bottom += viewport_height * buffer

        if right == left:
            scale_x = 100
        else:
            scale_x = window_width / float(right - left)
        if bottom == top:
            scale_y = 100
        else:
            scale_y = window_height / float(bottom - top)

        cx = (right + left) / 2
        cy = (top + bottom) / 2
        self.scene_widget.matrix.reset()
        self.scene_widget.matrix.post_translate(-cx, -cy)
        if lock:
            scale = min(scale_x, scale_y)
            if scale != 0:
                self.scene_widget.matrix.post_scale(scale)
        else:
            if scale_x != 0 and scale_y != 0:
                self.scene_widget.matrix.post_scale(scale_x, scale_y)
        self.scene_widget.matrix.post_translate(window_width / 2.0, window_height / 2.0)
