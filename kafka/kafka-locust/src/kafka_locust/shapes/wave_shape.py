from locust import LoadTestShape
import math


class WaveShape(LoadTestShape):
    """
    A load shape to simulate a wave pattern of user activity.
    """

    time_limit = 3600  # Total duration of the test in seconds
    wave_duration = 60  # Duration of each wave in seconds
    min_users = 0  # Minimum number of users
    max_users = 100  # Maximum number of users
    min_spawn_rate = 0.0001  # Minimum spawn rate to avoid ZeroDivisionError

    def tick(self):
        """
        Returns a tuple of (user_count, spawn_rate) based on a sine wave pattern.
        """
        run_time = self.get_run_time()

        # Check if the test is over
        if run_time > self.time_limit:
            return None

        # Calculate the current phase of the wave
        wave_phase = (run_time % self.wave_duration) / self.wave_duration
        # Use a sine wave function to calculate the user count
        user_count = int(
            (self.max_users - self.min_users)
            / 2
            * (1 + math.sin(2 * math.pi * wave_phase))
            + self.min_users
        )

        # Calculate spawn rate to smoothly adjust the user count
        spawn_rate = max(
            abs(user_count - self.runner.user_count) / 10, self.min_spawn_rate
        )

        return (user_count, spawn_rate)
