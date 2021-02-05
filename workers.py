from time import sleep
from random import randint

# Redis functions
def dummy_sleeping(msg):
    to_sleep = randint(2, 6)
    print(f"We are going to sleep for {to_sleep} seconds")
    print("Zzzzz...")

    sleep(to_sleep)
    print(f"Wakey wakey! - Job finished. Msg: ({msg})")