import time

class Interval:
    def __init__(self) -> None:
        self.can_run = False

    def run_interval(self, func, my_time: int):
        print('Args: ', type(func), type(my_time))
        self.can_run = True
        def func_wrapper():
            if self.can_run:
                func()
                time.sleep(my_time)
                func_wrapper()
        func_wrapper()
        print('Stop interval')
    
    def stop_interval(self):
        self.can_run = False
