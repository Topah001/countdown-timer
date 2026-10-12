import unittest

from main import countdown, format_duration, parse_duration


class CountdownTimerTests(unittest.TestCase):
    def test_duration_formats_parse(self):
        self.assertEqual(parse_duration("90"), 90)
        self.assertEqual(parse_duration("2:05"), 125)
        self.assertEqual(parse_duration("01:02:03"), 3723)

    def test_invalid_durations_are_rejected(self):
        for value in ("", "0", "-1", "1:60", "00:01:60", "abc", "100:00:00"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_duration(value)

    def test_format_duration(self):
        self.assertEqual(format_duration(0), "00:00:00")
        self.assertEqual(format_duration(3661), "01:01:01")
        with self.assertRaises(ValueError):
            format_duration(-1)

    def test_countdown_uses_sleep_and_notifies_expiry(self):
        now = [0.0]
        def fake_sleep(seconds):
            now[0] += seconds
        output = []
        countdown(3, sleep_fn=fake_sleep, clock_fn=lambda: now[0], output_fn=output.append)
        self.assertEqual(output, ["00:00:03", "00:00:02", "00:00:01", "Time is up!"])
        self.assertEqual(now[0], 3.0)

    def test_countdown_rejects_non_positive_duration(self):
        with self.assertRaises(ValueError):
            countdown(0, sleep_fn=lambda _: None, clock_fn=lambda: 0, output_fn=lambda _: None)


if __name__ == "__main__":
    unittest.main()