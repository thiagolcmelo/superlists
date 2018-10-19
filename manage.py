#!/usr/bin/env python
import os
import sys
import argparse

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'superlists.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    argv = sys.argv
    if '-s' in argv or '--server' in argv:
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-s', '--server', default='')
        args, argv = parser.parse_known_args(argv)
        # We can save the argument as an environmental variable, in
        # which case it's to retrieve from within `project.settings`,
        os.environ['STAGING_SERVER'] = args.server
        #skey = '-s' if '-s' in argv else '--server'
        #argv = sys.argv[:sys.argv.index(skey)]
    execute_from_command_line(argv)
