import random
import unittest

from meerk40t.core.units import Length, ViewPort, UNITS_PER_MIL


class TestViewport(unittest.TestCase):
    def test_viewport_arbitrary(self):
        """
        Test arbitrary viewport.

        :return:
        """
        bed_width = Length(amount=random.randint(0, 65535 * 1000)).length_mm
        bed_height = Length(amount=random.randint(0, 65535 * 1000)).length_mm
        for i in range(100):
            view = ViewPort(
                bed_width,
                bed_height,
                user_scale_x=1.0,
                user_scale_y=1.0,
                native_scale_x=UNITS_PER_MIL,
                native_scale_y=UNITS_PER_MIL,
                origin_x=random.random(),
                origin_y=random.random(),
                flip_x=bool(random.randint(0, 1)),
                flip_y=bool(random.randint(0, 1)),
                swap_xy=bool(random.randint(0, 1)),
            )

            x, y = view.scene_to_device_position(0, 0)
            x, y = view.device_to_scene_position(x, y)
            self.assertGreaterEqual(x, -10)
            self.assertGreaterEqual(10, x)
            self.assertGreaterEqual(y, -10)
            self.assertGreaterEqual(10, y)

    def test_viewport_lihuiyu_user_scale(self):
        """
        Test Lihuiyu-esque viewport. User-scaled to mm

        :return:
        """
        bed_width = "330mm"
        bed_height = "225mm"

        view = ViewPort(
            bed_width,
            bed_height,
            user_scale_x=1.2,
            user_scale_y=1.0,
            native_scale_x=UNITS_PER_MIL,
            native_scale_y=UNITS_PER_MIL,
            origin_x=0,
            origin_y=0,
        )
        x, y = view.scene_to_device_position(0, 0)
        self.assertGreaterEqual(x, -1)
        self.assertGreaterEqual(1, x)
        self.assertGreaterEqual(y, -1)
        self.assertGreaterEqual(1, y)

        x, y = view.scene_to_device_position(0, 0)
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, -10)
        self.assertGreaterEqual(10, y)

        x, y = view.device_to_scene_position(0, Length(bed_height).mil)
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, float(Length(bed_height)) - 10)
        self.assertGreaterEqual(float(Length(bed_height)) + 10, y)

        x, y = view.device_to_scene_position(
            Length(bed_width).mil, Length(bed_height).mil
        )
        self.assertGreaterEqual(x, float(Length(bed_width)) * 1.2 - 10)
        self.assertGreaterEqual(float(Length(bed_width)) * 1.2 + 10, x)
        self.assertGreaterEqual(y, float(Length(bed_height)) - 10)
        self.assertGreaterEqual(float(Length(bed_height)) + 10, y)

    def test_viewport_lihuiyu_swap_xy(self):
        """
        Test Lihuiyu-esque viewport. User-scaled to mm

        :return:
        """
        bed_width = "330mm"
        bed_height = "225mm"

        view = ViewPort(
            bed_width,
            bed_height,
            user_scale_x=1.2,
            user_scale_y=1.0,
            native_scale_x=UNITS_PER_MIL,
            native_scale_y=UNITS_PER_MIL,
            origin_x=0,
            origin_y=0,
            swap_xy=True,
        )
        x, y = view.scene_to_device_position(0, 0)
        self.assertGreaterEqual(x, -1)
        self.assertGreaterEqual(1, x)
        self.assertGreaterEqual(y, -1)
        self.assertGreaterEqual(1, y)

        x, y = view.scene_to_device_position(0, 0)
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, -10)
        self.assertGreaterEqual(10, y)

        x, y = view.device_to_scene_position(0, Length(bed_height).mil)
        self.assertGreaterEqual(x, float(Length(bed_height)) - 10)
        self.assertGreaterEqual(float(Length(bed_height)) + 10, x)
        self.assertGreaterEqual(y, -10)
        self.assertGreaterEqual(10, y)

        x, y = view.device_to_scene_position(
            Length(bed_width).mil, Length(bed_height).mil
        )
        self.assertGreaterEqual(x, float(Length(bed_height)) - 10)
        self.assertGreaterEqual(float(Length(bed_height)) + 10, x)
        self.assertGreaterEqual(y, float(Length(bed_width)) * 1.2 - 10)
        self.assertGreaterEqual(float(Length(bed_width)) * 1.2 + 10, y)

    def test_viewport_grbl(self):
        """
        Test GRBL-esque viewport.

        :return:
        """
        bed_size = "225mm"

        view = ViewPort(
            bed_size,
            bed_size,
            native_scale_x=UNITS_PER_MIL,
            native_scale_y=UNITS_PER_MIL,
            origin_x=0,
            origin_y=1,
            flip_y=True,
        )
        x, y = view.scene_to_device_position(0, 0)
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, Length(bed_size).mil - 10)
        self.assertGreaterEqual(Length(bed_size).mil + 10, y)

        x, y = view.scene_to_device_position(0, float(Length(bed_size)))
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, -10)
        self.assertGreaterEqual(10, y)

        x, y = view.device_to_scene_position(0, Length(bed_size).mil)
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, -10)
        self.assertGreaterEqual(10, y)

    def test_viewport_grbl_user_scale(self):
        """
        Test GRBL-esque viewport. User-scaled to mm

        :return:
        """
        bed_size = "225mm"

        view = ViewPort(
            bed_size,
            bed_size,
            user_scale_x=1.0 / Length("1mil").mm,
            user_scale_y=1.0 / Length("1mil").mm,
            native_scale_x=UNITS_PER_MIL,
            native_scale_y=UNITS_PER_MIL,
            origin_x=0,
            origin_y=1,
            flip_y=True,
        )
        x, y = view.scene_to_device_position(0, 0)
        self.assertGreaterEqual(x, -1)
        self.assertGreaterEqual(1, x)
        self.assertGreaterEqual(y, Length(bed_size).mm - 1)
        self.assertGreaterEqual(Length(bed_size).mm + 1, y)

        x, y = view.scene_to_device_position(0, float(Length(bed_size)))
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, -10)
        self.assertGreaterEqual(10, y)

        x, y = view.device_to_scene_position(0, Length(bed_size).mm)
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, -10)
        self.assertGreaterEqual(10, y)

    def test_viewport_balor(self):
        """
        Test Balor-esque viewport.
        Center x, y.

        :return:
        """
        lens_size = "110mm"
        unit_size = float(Length(lens_size))
        galvo_range = 0xFFFF
        units_per_galvo = unit_size / galvo_range

        view = ViewPort(
            lens_size,
            lens_size,
            native_scale_x=units_per_galvo,
            native_scale_y=units_per_galvo,
            origin_x=0.5,
            origin_y=0.5,
        )

        x, y = view.device_to_scene_position(0x8000, 0x8000)
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, -10)
        self.assertGreaterEqual(10, y)

    def test_viewport_balor_flip_y(self):
        """
        Test Balor-esque viewport.
        Center x, y. flip_y

        :return:
        """
        lens_size = "110mm"
        unit_size = float(Length(lens_size))
        galvo_range = 0xFFFF
        units_per_galvo = unit_size / galvo_range

        view = ViewPort(
            lens_size,
            lens_size,
            native_scale_x=units_per_galvo,
            native_scale_y=units_per_galvo,
            origin_x=0.5,
            origin_y=0.5,
            flip_y=True,
        )

        x, y = view.device_to_scene_position(0x8000, 0x8000)
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, -10)
        self.assertGreaterEqual(10, y)

    def test_viewport_balor_flip_x(self):
        """
        Test Balor-esque viewport.
        Center x, y. flip_x

        :return:
        """
        lens_size = "110mm"
        unit_size = float(Length(lens_size))
        galvo_range = 0xFFFF
        units_per_galvo = unit_size / galvo_range

        view = ViewPort(
            lens_size,
            lens_size,
            native_scale_x=units_per_galvo,
            native_scale_y=units_per_galvo,
            origin_x=0.5,
            origin_y=0.5,
            flip_x=True,
        )

        x, y = view.device_to_scene_position(0x8000, 0x8000)
        self.assertGreaterEqual(x, -10)
        self.assertGreaterEqual(10, x)
        self.assertGreaterEqual(y, -10)
        self.assertGreaterEqual(10, y)
