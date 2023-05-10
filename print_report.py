from termcolor import colored, cprint
from colorama import Fore, Back, Style
import yaml
import time


with open('settings.yml') as info:
    set_dict = yaml.safe_load(info)

task_width = set_dict['task_width']

move_cursor_up = '\033[1A'
set_cursor_column = f'\033[{task_width}C'
clear_result_field = '\x1b[0K'


def print_header(content):
    header_width = set_dict['task_width'] + set_dict['result_width']
    content = content+" "
    content = ('{:*<{x}}'.format(content,x=header_width))
    print ('{:*<{x}}'.format(content,x=header_width))


def print_action(content):
    content = "- "+content
    content = ('{:<{x}}'.format(content,x=set_dict['task_width']))
    print (content)
    print_status("Running")

def print_action_l2(content):
    content = "  "+content
    content = ('{:<{x}}'.format(content,x=set_dict['task_width']))
    print (content)
    print_status("Running")


def print_status(status):
    content = (Fore.WHITE + '{:>{x}}'.format(status,x=set_dict['result_width'])+ Fore.RESET)
    print (move_cursor_up, end=set_cursor_column)
    print (end=clear_result_field)
    print (colored(content, attrs=['blink']))
    time.sleep(1)


def print_skip():
    content = (Fore.YELLOW + '{:>{x}}'.format(set_dict['result_skip'],x=set_dict['result_width'])+ Fore.RESET)
    print (move_cursor_up, end=set_cursor_column)
    print (end=clear_result_field)
    print (content)
    time.sleep(1)

def print_skip_custom(result):
    content = (Fore.YELLOW + '{:>{x}}'.format(result,x=set_dict['result_width'])+ Fore.RESET)
    print (move_cursor_up, end=set_cursor_column)
    print (end=clear_result_field)
    print (content)
    time.sleep(1)


def print_pass():
    content = (Fore.GREEN + '{:>{x}}'.format(set_dict['result_pass'],x=set_dict['result_width'])+ Fore.RESET)
    print (move_cursor_up, end=set_cursor_column)
    print (end=clear_result_field)
    print (content)
    time.sleep(1)

def print_pass_custom(result):
    content = (Fore.GREEN + '{:>{x}}'.format(result,x=set_dict['result_width'])+ Fore.RESET)
    print (move_cursor_up, end=set_cursor_column)
    print (end=clear_result_field)
    print (content)
    time.sleep(1)


def print_fail():
    content = (Fore.RED + '{:>{x}}'.format(set_dict['result_fail'],x=set_dict['result_width'])+ Fore.RESET)
    print (move_cursor_up, end=set_cursor_column)
    print (end=clear_result_field)
    print (content)
    time.sleep(1)




