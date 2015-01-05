import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

from django.conf import settings
from django.db import transaction
from defender.data import store_login_attempt

@transaction.atomic
def main(use_celery):
    """ Create a record for the login attempt If using celery call celery
    task, if not, call the method normally """
    user_agent = '<unknown>'
    ip_address = '127.0.0.1'
    username = 'marcus@example.com'
    http_accept = '<unknown>'
    path_info = '<unknown>'
    login_valid = False

    if use_celery:
        from celery import shared_task
        from defender.tasks import add_login_attempt_task
        add_login_attempt_task.delay(user_agent, ip_address, username,
                                     http_accept, path_info, login_valid)
    else:
        store_login_attempt(user_agent, ip_address, username,
                            http_accept, path_info, login_valid)


if __name__ == "__main__":
    import timeit
    import time
    number = 1000

    print("without celery")
    print(timeit.timeit("main(False)", setup="from __main__ import main", number=number))

    time.sleep(5)

    print("use celery")
    print(timeit.timeit("main(True)", setup="from __main__ import main", number=number))
