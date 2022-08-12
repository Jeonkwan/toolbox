import os
from os.path import isfile as is_file
from os.path import join as p_join
import filecmp
from difflib import Differ


script_dir = os.path.dirname(os.path.realpath(__file__))
print(f"Working Directory: {script_dir}")

left_dir = os.path.join(script_dir, 'left_files')
right_dir = os.path.join(script_dir, 'right_files')
print(f"Left side: {left_dir}")
print(f"Right side: {right_dir}")

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

left_files_only = get_files_only_list(left_dir)
right_files_only = get_files_only_list(right_dir)

print(left_files_only)
print(right_files_only)

dir_compare_result = filecmp.dircmp(left_dir, right_dir)
l_r_common_files = dir_compare_result.common_files
l_only_files = dir_compare_result.left_only
r_only_files = dir_compare_result.right_only

print(f"Left and Right Common Files(same name only):\n{l_r_common_files}")
print(f"Left Only Files:\n{l_only_files}")
print(f"Right Only Files:\n{r_only_files}")

if(len(l_only_files) != 0 or len(r_only_files) != 0): 
    print("Manualy check on left only OR right only files.")

# check whether common files are identical:
for common_file_name in l_r_common_files:
    left_file_path = p_join(left_dir, common_file_name)
    right_file_path = p_join(right_dir, common_file_name)
    with open(left_file_path) as file_L, open(right_file_path) as file_R:
        differ = Differ()
        print(f"Diff for Common File: {common_file_name}")
        diff_result = differ.compare(file_L.readlines(), file_R.readlines())
        print(str(diff_result))
        # todo: better at reporting error
        # https://docs.python.org/3/library/difflib.html