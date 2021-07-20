# Scheduler
A scheduler for running tasks is provided by the [Django Background Tasks](https://django-background-tasks.readthedocs.io/) library.

Currently, only some tasks from the scraper module can be scheduled. More details on [scraper docs](SCRAPER.md).

## How to use
Read library documentation for learning on how to allow an specific task/function to be scheduled.

For scheduled tasks to excecute, you need to run this management command:
```
python manage.py process_tasks
```

It is recomended to daemonize or supervise this process on production enviroments.
