import time



class TaskTimer():
    def __init__(self):
        self.reset()


    def show(self):
        result = []
        if self.start_time is not None:
            total_time = time.time() - self.start_time
            for task in self.tasks:
                line = '{}: {} ({}%)'.format(task, self.tasks[task], (self.tasks[task] / total_time) * 100)
                result.append(line)
                print(line)
        else:
            print('nothing')
        return result


    def reset(self):
        self.start_time = None
        self.prev_time = None
        self.prev_name = None
        self.tasks = {}


    def log(self, name):
        #print(name)
        #print(self.tasks)
        if self.prev_time is not None:
            time_delta = time.time() - self.prev_time
            if self.prev_name in self.tasks:
                self.tasks[self.prev_name] += time_delta
            else:
                self.tasks[self.prev_name] = time_delta
        else:
            self.start_time = self.prev_time = time.time()
        self.prev_time = time.time()
        self.prev_name = name

if __name__ == '__main__':
    tt = TaskTimer()

    for i in range(10):
        tt.log('a')
        time.sleep(0.01)
        tt.log('b')
        time.sleep(0.02)
    tt.log('b')

    tt.show()
