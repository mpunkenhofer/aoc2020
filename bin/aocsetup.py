from datetime import datetime
import argparse
import logging
import json
import sys
import requests
import os


def load_config(config_file):
    config = {}

    try:
        with open(config_file, mode='r') as f:
            # logging.info('loading config: {}'.format(config_file))
            config = json.load(f)
            return config
    except FileNotFoundError:
        # logging.info('creating default config file...')

        default_config = {
            # AoC Session Cookie
            "session-cookie": "",
            # Leave empty if you are not using a src template
            "src-template": "src-template.py",
            "src-output": "src/year-{{year}}/day-{{day}}.py",
            # Leave empty if you are not using a test template
            "test-template": "test-template.py",
            "test-output": "tests/year-{{year}}/test_day{{day}}.py",
            # None or >= 2015 -- ignored if you are using wait
            "year": None,
            # None or 1 - 25 -- ignored if you are using wait
            "day": None,
            # Wait for next AoC release
            "wait": False,
            # Replace any existing files
            "force": False,
            # Detailed logging output
            "log": False
        }

        with open('aocsetup.conf', 'w') as f:
            json.dump(default_config, f, indent=4)

        return default_config


def load_input_file(year, day, session_id):
    uri = 'https://adventofcode.com/{}/day/{}/input'.format(year, day)
    aoc_cookie = {'session': session_id}

    r = requests.get(uri, cookies=aoc_cookie)

    if r.status_code == 200:
        logging.info('Got input from {}'.format(uri))
        return r.text
    else:
        logging.info('Invalid request return: {} for {}'.format(
            r.status_code, uri))
        return None


def write_file(filename, content, force=False):
    if not filename:
        logging.info('Missig filename: {}!'.format(filename))
        return

    if not content:
        logging.info('No content to write for file: {}!'.format(filename))

    dirs = os.path.dirname(filename)
    exists = os.path.isfile(filename)

    if dirs:
        logging.info('Creating directories: {} ...'.format(dirs))
        os.makedirs(dirs, exist_ok=True)

    if not exists or force:
        with open(filename, "w+") as f:
            logging.info('Writing file: {} ...'.format(filename))
            f.write(content)
    elif exists:
        print('File "{}" already exists. Skipped writing file.\nUse -f if you want to overwrite existing files.'.format(filename))

def replace_placeholder(content: str, year, day):
    content = content.replace('{{day}}', '{}'.format(day))
    content = content.replace('{{year}}', '{}'.format(year))
    return content


def write_template(template, output, year, day, force):
    if template and output:
        try:
            with open(template, 'r') as f:
                logging.info(
                    'Reading & processing template: {} ...'.format(template))
                tmp = f.read()
                tmp = replace_placeholder(tmp, year, day)
                write_file(replace_placeholder(output, year, day), tmp, force)
        except FileNotFoundError as e:
            print('{}'.format(str(e)))

def write_input(output, session_cookie, year, day, force):
    if output and session_cookie:
        input_file = load_input_file(year, day, session_cookie)
        write_file(replace_placeholder(output, year, day), input_file, force)


def wait():
    print('waiting...')


def main():
    today = datetime.today()

    parser = argparse.ArgumentParser(
        description='Advent of Code (AOC) utility to download problem input and setup python files for a given day.')
    parser.add_argument('-s', '--session-cookie', type=str, default=None,
                        help='Session cookie which is used to dowload problem input')
    parser.add_argument('-y', '--year', type=int, default=None,
                        help='Download the aoc input for a given year')
    parser.add_argument('-d', '--day', type=int, default=None,
                        help='Download the aoc input for a given day')
    parser.add_argument('-st', '--src-template', type=str,
                        default=None, help='Source template file')
    parser.add_argument('-so', '--src-output', type=str,
                        default=None, help='Source output file')
    parser.add_argument('-tt', '--test-template', type=str,
                        default=None, help='Test template file')
    parser.add_argument('-to', '--test-output', type=str,
                        default=None, help='Test output file')
    parser.add_argument('-io', '--input-output', type=str,
                        default=None, help='Input output file')
    parser.add_argument('-cf', '--config-file', type=str,
                        default='aocsetup.conf', help='Config file')
    parser.add_argument('-w', '--wait', action='store_true',
                        default=False, help='Wait for the next problem release')
    parser.add_argument('-l', '--log', action='store_true',
                        default=False, help='Enable logging')
    parser.add_argument('-f', '--force', action='store_true',
                        default=False, help='Overwrite existing files')

    args = parser.parse_args()

    if args.log:
        logging.basicConfig(level=logging.INFO)

    config = load_config(args.config_file)

    logging.info('arguments: {}'.format(args))

    session_cookie = args.session_cookie or config['session-cookie'] or None
    year = args.year or config['year'] or today.year
    day = args.day or config['day'] or today.day
    src_template = args.src_template
    src_output = args.src_output
    test_template = args.test_template
    test_output = args.test_output
    input_output = args.input_output
    force = args.force

    if 2015 < year > today.year:
        logging.info('year: {} out of acceptable range'.format(year))
        print('Invalid input: year has to be between 2015 and {}. (input was: {})'.format(
            today.year, year))
        sys.exit(0)

    if 1 < day > 25:
        logging.info('day: {} out of acceptable range'.format(year))
        print('Invalid input: there are 1-25 days in one AoC. (input was: {})'.format(day))

    write_input(input_output, session_cookie, year, day, force)
    write_template(src_template, src_output, year, day, force)
    write_template(test_template, test_output, year, day, force)

    logging.info('aocsetup done.')


if __name__ == "__main__":
    main()
