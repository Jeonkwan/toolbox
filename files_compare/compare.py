from email import parser
import os
from os.path import isfile as is_file
from os.path import join as p_join
import filecmp
from difflib import Differ
import re
from pprint import pprint
import argparse
from turtle import right

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description='left and right directory files compare'
        )
    parser.add_argument('-l', '--left-dir', required=True, dest='left_dir', help='Left side directory')
    parser.add_argument('-r', '--right-dir', required=True, dest='right_dir', help='Right side directory')
    return parser

def get_files_only_list(dir: str):
    if not os.path.isdir(dir): 
        print(f"EXIT. Given Directory does NOT exist. {dir}")
        exit(1)
    try:
        dir_list = os.listdir(dir)
    except FileNotFoundError:
        print(f"Given Directory is EMPTY. {dir}")
        dir_list = []
    return [p_join(dir, f) for f in dir_list if is_file(p_join(dir, f))] 

def prettyListStr(list: list):
    return '\n'.join(list)

def recursive_common_files_content_compare(dcmp: filecmp.dircmp, l_dir: str, r_dir: str):
    sub_dcmps = dcmp.subdirs.values()
    common_files_content_compare(dcmp, l_dir, r_dir)
    for index, s_dcmp in enumerate(sub_dcmps):
        sub_dir_name = dcmp.common_dirs[index]
        print(f"{indent_prefix}++++++ {index} - Directory: {sub_dir_name} ++++++")
        recursive_common_files_content_compare(s_dcmp, p_join(l_dir, sub_dir_name), p_join(r_dir, sub_dir_name))

def common_files_content_compare(dir_compare_result: filecmp.dircmp, l_dir: str, r_dir: str):
    print('\n+++++++++++++++++++++ content compare section start +++++++++++++++++++++')
    l_r_common_files = dir_compare_result.common_files
    l_r_common_dirs = dir_compare_result.common_dirs
    l_only_files = dir_compare_result.left_only
    r_only_files = dir_compare_result.right_only
    print(f"Left side: {l_dir}")
    print(f"Right side: {r_dir}")
    
    print(f"====== [{len(l_only_files)}] Left Only Files ======\n{prettyListStr(l_only_files)}\n")
    print(f"====== [{len(r_only_files)}] Right Only Files ======\n{prettyListStr(r_only_files)}\n")

    if(len(l_only_files) != 0 or len(r_only_files) != 0): 
        print("!!!Requires manualy checking on left only OR right only files.!!!")

    print(f"====== [{len(l_r_common_files)}] Left and Right Common Files(same name only) ======\n{prettyListStr(l_r_common_files)}\n")
    print(f"====== [{len(l_r_common_dirs)}] Left and Right Common Directories(same name only) ======\n{prettyListStr(l_r_common_dirs)}\n")
    
    diff_common_files_result = {}
    diff_common_files = []
    same_common_files = []

    # check whether common files are identical:
    for common_file_name in l_r_common_files:
        print(f"====== Checking Diff for Common File: {common_file_name} ======")
        all_diff_of_a_file = ''
        left_file_path = p_join(l_dir, common_file_name)
        right_file_path = p_join(r_dir, common_file_name)
        with open(left_file_path) as file_L, open(right_file_path) as file_R:
            differ = Differ()
            diff_result = differ.compare(file_L.readlines(), file_R.readlines())
            for line in diff_result:
                regex_finder = re.compile('^(\-)|(\+)|(\?) .*')
                regex_matcher = regex_finder.search(line)
                if not regex_matcher: continue
                all_diff_of_a_file += f"\t{line}"
        if all_diff_of_a_file:
            diff_common_files_result[common_file_name] = all_diff_of_a_file
            diff_common_files.append(common_file_name)
            print(f"Found diff:\n{all_diff_of_a_file}")
        else:
            same_common_files.append(common_file_name)
            print("No diff found.")
        print("------ Checing END ------\n")

    print(f"====== [{len(same_common_files)}] Same Common Files(Update NOT Required) ======\n{prettyListStr(same_common_files)}\n")
    print(f"====== [{len(diff_common_files)}] Different Common Files(Update Required) ======\n{prettyListStr(diff_common_files)}\n")
    print('+++++++++++++++++++++ content compare section end +++++++++++++++++++++\n')

parser = init_argparse()
args = parser.parse_args()
# safe check is needed
left_dir = args.left_dir
right_dir = args.right_dir

script_dir = os.path.dirname(os.path.realpath(__file__))
print(f"Working Directory: {script_dir}")

left_dir = p_join(script_dir, left_dir)
right_dir = p_join(script_dir, right_dir)

if not os.path.isdir(left_dir): 
    print(f"Directory does NOT exist: {left_dir}")
    exit(1)
if not os.path.isdir(right_dir): 
    print(f"Directory does NOT exist: {right_dir}")
    exit(1)

dir_compare_result = filecmp.dircmp(left_dir, right_dir)
recursive_common_files_content_compare(dir_compare_result, left_dir, right_dir)
