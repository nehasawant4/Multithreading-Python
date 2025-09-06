import threading
import time
import random

class StarvationFreeBathroom:
    def __init__(self):
        self.mutex = threading.Lock()

        self.male_sem = threading.Semaphore(0)
        self.female_sem = threading.Semaphore(0)

        self.current_gender = None
        self.inside_count = 0

        self.waiting_male = 0
        self.waiting_female = 0

    def try_enter(self, gender):
        with self.mutex:
            if self.current_gender is None:
                self.current_gender = gender

            if self.current_gender == gender and self.inside_count < 3:
                self.inside_count += 1
                return True  # Can enter
            else:
                if gender == 'male':
                    self.waiting_male += 1
                else:
                    self.waiting_female += 1
                return False  # Must wait

    def exit_bathroom(self, gender):
        with self.mutex:
            self.inside_count -= 1

            if self.inside_count == 0:
                # Switch turn only if other gender is waiting
                if gender == 'male' and self.waiting_female > 0:
                    self.current_gender = 'female'
                    for _ in range(min(3, self.waiting_female)):
                        self.female_sem.release()
                        self.waiting_female -= 1
                elif gender == 'female' and self.waiting_male > 0:
                    self.current_gender = 'male'
                    for _ in range(min(3, self.waiting_male)):
                        self.male_sem.release()
                        self.waiting_male -= 1
                else:
                    self.current_gender = None

    def enter_male(self, name):
        while not self.try_enter('male'):
            self.male_sem.acquire()

        print(f"{name} entered.")
        time.sleep(random.uniform(0.1, 0.4))
        print(f"{name} used bathroom.")

        self.exit_bathroom('male')

    def enter_female(self, name):
        while not self.try_enter('female'):
            self.female_sem.acquire()

        print(f"{name} entered.")
        time.sleep(random.uniform(0.1, 0.4))
        print(f"{name} used bathroom.")

        self.exit_bathroom('female')

def simulate_male(bathroom, name):
    bathroom.enter_male(name)

def simulate_female(bathroom, name):
    bathroom.enter_female(name)

def main():
    bathroom = StarvationFreeBathroom()
    threads = []

    for i in range(20):
        threads.append(threading.Thread(target=simulate_male, args=(bathroom, f"Male-{i+1}")))
        threads.append(threading.Thread(target=simulate_female, args=(bathroom, f"Female-{i+1}")))

    random.shuffle(threads)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("All done.")

if __name__ == "__main__":
    main()
