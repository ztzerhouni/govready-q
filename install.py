#!/usr/bin/env python3

################################################################
#
# install.py - Quickly set up a new GovReady-Q instance
#   from a freshly-cloned repository.
#
# Usage: install.py [--help] [--non-interactive] [--verbose]
#
# Optional arguments:
#   -h, --help             show this help message and exit
#   -n, --non-interactive  run without terminal interaction
#   -u, --user             do pip install with --user flag
#   -v, --verbose          output more information
#
################################################################

# parse command-line arguments
import argparse

# system stuff
import os
import platform
import re
import signal
import subprocess
import sys
import time

# JSON handling
import json

# Default constants
GOVREADYURL = "http://localhost:8000"
SPACER = "\n====\n"

# Gracefully exit on control-C
signal.signal(signal.SIGINT, lambda signal_number, current_stack_frame: sys.exit(0))

# Define a fatal error handler
class FatalError(Exception):
    pass

# Define a halted error handler
class HaltedError(Exception):
    pass

# Set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Quickly set up a new GovReady-Q instance from a freshly-cloned repository.')
    parser.add_argument('--non-interactive', '-n', action='store_true', help='run without terminal interaction')
    parser.add_argument('--user', '-u', action='store_true', help='do pip install with --user flag')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='output more information')
    return parser

################################################################
#
# helpers
#
################################################################

def run_optionally_verbose(args, verbose_flag):
    if verbose_flag:
        p = subprocess.run(args, capture_output=False)
    else:
        p = subprocess.run(args, capture_output=True)
    return p

def check_has_command(command_array):
    try:
        p = subprocess.run(command_array, capture_output=True)
        return True
    except FileNotFoundError as err:
        return False

def create_environment_json(path):
    import secrets
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = ''.join(secrets.choice(alphabet) for i in range(50))
    # NOTE: `environment` here refers to locally-created environment data object and not OS-level environment variables
    environment = {
    "govready-url": GOVREADYURL,
    "static": "static_root",
    "secret-key": secret_key,
    "test_visible": False,
    "debug": True
    }
    # Create local directory
    if not os.path.exists('local'):
        os.makedirs('local')
    # Create local/envionment.json file
    with open(path, 'w') as f:
        f.write(json.dumps(environment, sort_keys=True, indent=2))

def main():
    print(">>>>>>>>>> Welcome to the GovReady-Q Installer <<<<<<<<<\n")

    try:
        # Collect command line arguments, print help if necessary
        argparser = init_argparse();
        args = argparser.parse_args();

        print("Testing environment...\n")

        # Print machine information
        print("Platform is {} version {} running on {}.".format(platform.system(), platform.release(), platform.machine()))

        # Print spacer
        print(SPACER)

        # Test version of Python
        ver = sys.version_info
        print("Python version is {}.{}.{}.".format(ver[0],ver[1],ver[2]))

        if sys.version_info >= (3, 8):
            print("+ Python version is >= 3.8.")
        else:
            print("! Python version is < 3.8.")
            print("GovReady-Q is best run with Python 3.8 or higher.")
            print("It is STRONGLY encouraged to run GovReady-Q with Python 3.8 or higher.")
            if args.non_interactive:
                reply = ''
            else:
                reply = input("Continue install with Python {}.{}.{} (y/n)? ".format(ver[0],ver[1],ver[2]))
            if len(reply) == 0 or reply[0].lower() != "y":
                raise HaltedError("Python version is < 3.8")

        # Print spacer
        print(SPACER)

        # Check if inside a virtual environment
        print("Check for virtual Python environment.")
        if sys.prefix != sys.base_prefix:
            print("+ Installer is running inside a virtual Python environment.")
        else:
            print("! Installer is not running inside a virtual Python environment.")
            print("It is STRONGLY encouraged to run GovReady-Q inside a Python virtual environment.")
            if args.non_interactive:
                reply = ''
            else:
                reply = input("Continue install outside of virtual environment (y/n)? ")
            if len(reply) == 0 or reply[0].lower() != "y":
                raise HaltedError("Installer is not running inside a virtual Python environment")

        # Print spacer
        print(SPACER)

        # Check for python3 and pip3 (and not 2 or e.g. 'python3.8')
        print("Confirming python3 and pip3 commands are available...", flush=True)
        if not check_has_command(['python3', '--version']):
            raise FatalError("The 'python3' command is not available.")
        if not check_has_command(['pip3', '--version']):
            raise FatalError("The 'pip3' command is not available.")
        print("... done confirming python3 and pip3 commands are available.", flush=True)

        # Print spacer
        print(SPACER)

        # Print mode of interactivity
        if args.non_interactive:
            print("Installing/updating GovReady-Q in non-interactive mode.")
        else:
            print("Installing/updating GovReady-Q in interactive mode.")

        # Print spacer
        print(SPACER)

        # Briefly sleep in verbose mode so user can glance at output.
        time.sleep(3) if args.verbose else time.sleep(0)

        # pip install basic requirements
        print("Installing Python libraries via pip...", flush=True)
        if args.user:
            p = run_optionally_verbose(['pip3', 'install', '--user', '-r', 'requirements.txt'], args.verbose)
            if p.returncode != 0:
                raise FatalError("'pip3 install' returned error code {}".format(p.returncode))
        else:
            p = run_optionally_verbose(['pip3', 'install', '-r', 'requirements.txt'], args.verbose)
            if p.returncode != 0:
                raise FatalError("'pip3 install' returned error code {}".format(p.returncode))
        print("... done installing Python libraries via pip.", flush=True)

        # Print spacer
        print(SPACER)

        # Retrieve static assets
        print("Fetching static resource files from Internet...", flush=True)
        p = run_optionally_verbose(['./fetch-vendor-resources.sh'], args.verbose)
        if p.returncode != 0:
            raise FatalError("'./fetch-vendor-resources.sh' returned error code {}".format(p.returncode))
        print("... done fetching resource files from Internet.", flush=True)

        # Print spacer
        print(SPACER)

        # Collect files into static directory
        print("Collecting files into static directory...", flush=True)
        if args.non_interactive:
            p = run_optionally_verbose(['./manage.py', 'collectstatic', '--no-input'], args.verbose)
            if p.returncode != 0:
                raise FatalError("'./manage.py collectstatic --no-input' returned error code {}".format(p.returncode))
        else:
            p = run_optionally_verbose(['./manage.py', 'collectstatic', '--no-input'], args.verbose)
            if p.returncode != 0:
                raise FatalError("'./manage.py collectstatic' returned error code {}".format(p.returncode))
        print("... done collecting files into static directory.", flush=True)

        # Print spacer
        print(SPACER)

        # Create the local/environment.json file, if it is missing (it generally will be)
        # NOTE: `environment` here refers to locally-created environment data object and not OS-level environment variables
        print("Creating local/environment.json file...", flush=True)
        environment_path = 'local/environment.json'
        if os.path.exists(environment_path):
            # confirm that environment.json is JSON
            try:
                environment = json.load(open(environment_path))
                print("environment.json file already exists, proceeding")
            except json.decoder.JSONDecodeError as e:
                print("'{}' is not in JSON format:".format(environment_path))
                print(">>>>>>>>>>")
                print(open(environment_path).read())
                print("<<<<<<<<<<")
                raise FatalError("'{}' is not in JSON format.".format(environment_path))
        else:
            create_environment_json(environment_path)
        print("... done creating local/environment.json file.", flush=True)

        # Print spacer
        print(SPACER)

        # Configure database (migrate, load_modules)
        print("Initializing/migrating database...", flush=True)
        p = run_optionally_verbose(["./manage.py", "migrate"], args.verbose)
        if p.returncode != 0:
            raise FatalError("'./manage.py migrate' returned error code {}".format(p.returncode))
        p = run_optionally_verbose(["./manage.py", "load_modules"], args.verbose)
        if p.returncode != 0:
            raise FatalError("'./manage.py load_modules' returned error code {}".format(p.returncode))
        print("... done initializing/migrating database.", flush=True)

        # Print spacer
        print(SPACER)

        # Run first_run non-interactively
        print("Setting up system and creating Administrator user if none exists...", flush=True)
        p = subprocess.run(["./manage.py", "first_run", "--non-interactive"], capture_output=True)
        if p.returncode != 0:
            raise FatalError("'./manage.py first_run --non-interactive' returned error code {}".format(p.returncode))
        if args.verbose:
            print(p.stdout.decode('utf-8'))
            print(p.stdout.decode('utf-8'), p.stderr.decode('utf-8'))
        # save admin account details
        admin_details = ''
        if p.stdout:
            m1 = re.search('\n(Created administrator account.+)\n', p.stdout.decode('utf-8'))
            m2 = re.search('\n(Skipping create admin account.+)\n', p.stdout.decode('utf-8'))
            m3 = re.search('\n(\[INFO\] Superuser.+)\n', p.stdout.decode('utf-8'))
            if m1:
                admin_details = m1.group(1)
            elif m2:
                admin_details = "Administrator account(s) previously created."
            elif m3:
                admin_details = "Administrator account(s) previously created."
            else:
                admin_details = "Administrator account details not found."
        print("... done setting up system and creating Administrator user.", flush=True)

        # Print spacer
        print(SPACER)

        # Load GovReady sample SSP
        print("Setting up GovReady-Q sample project if none exists...", flush=True)
        p = run_optionally_verbose(["./manage.py", "load_govready_ssp"], args.verbose)
        if p.returncode != 0:
            raise FatalError("'./manage.py load_govready_ssp' returned error code {}".format(p.returncode))
        print("... done setting up GovReady-Q sample project.", flush=True)

        # Print spacer
        print(SPACER)

        print("""\

***********************************
* GovReady-Q Server configured... *
***********************************

To start GovReady-Q, run:
    ./manage.py runserver
""")

        if len(admin_details):
            if "Created administrator account" in admin_details:
                print("Log in with these administrator credentials.\n\nWRITE THIS DOWN:\n")
            print(admin_details, "\n")

        print("When GovReady-Q is running, visit http://localhost:8000/ with your web browser.\n")

    except HaltedError as err:
        print("\n\nInstall halted because: {}.\n".format(err));
        sys.exit(0)

    except FatalError as err:
        print("\n\nFatal error, exiting: {}.\n".format(err));
        sys.exit(1)

if __name__ == "__main__":
    exit(main())