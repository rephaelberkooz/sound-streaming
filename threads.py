import threading
import time

# Function for the first thread
def first_thread_func():
    print("First thread is starting a second thread.")
    second_thread = threading.Thread(target=second_thread_func)
    second_thread.start()
    print("First thread is not blocking on the second thread.")

# Function for the second thread
def second_thread_func():
    print("Second thread is running.")
    time.sleep(2)
    print("Second thread is done.")

# Create and start the first thread
first_thread = threading.Thread(target=first_thread_func)
first_thread.start()
first_thread.join()
print("Main thread is done.")
