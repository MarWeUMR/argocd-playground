from locust import LoadTestShape


class SingleBurstShape(LoadTestShape):
    time_limit = 30  # Duration of each burst in seconds
    users = 60
    spawn_rate = 600  # Spawn all users almost instantly

    def tick(self):
        run_time = self.get_run_time()

        # Calculate the current cycle (each cycle is time_limit seconds long)
        cycle = int(run_time / self.time_limit)

        # Alternate between running 60 users and stopping all users each cycle
        if cycle % 2 == 0:
            return (self.users, self.spawn_rate)
        else:
            return (0, self.spawn_rate)
