from pathlib import Path
import pytest
import subprocess
import re

TEST_CASES = [
    "../class4/exercises/ex7_show_int_status.py",
    #    COLLATERAL
]

TEST_CASES_TEXTFSM = [
    (
        "../class4/exercises/ex1_show_int_status.tpl",
        "../class4/exercises/ex1_show_int_status.txt",
        5,
    ),
    (
        "../class4/exercises/ex2_show_int_status.tpl",
        "../class4/exercises/ex2_show_int_status.txt",
        5,
    ),
    (
        "../class4/exercises/ex3_nxos_show_interface.tpl",
        "../class4/exercises/ex3_nxos_show_interface_ethernet_2_1.txt",
        2,
    ),
    (
        "../class4/exercises/ex4_junos_show_arp.tpl",
        "../class4/exercises/ex4_junos_show_arp.txt",
        7,
    ),
    (
        "../class4/exercises/ex5_show_lldp_neighbors.tpl",
        "../class4/exercises/ex5_nxos_show_lldp_neighbors.txt",
        5,
    ),
    (
        "../class4/exercises/ex6_show_ip_bgp_summary.tpl",
        "../class4/exercises/ex6_show_ip_bgp_summary.txt",
        14,
    ),
]


def subprocess_runner(cmd_list, exercise_dir):
    with subprocess.Popen(
        cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=exercise_dir
    ) as proc:
        std_out, std_err = proc.communicate()
    return (std_out.decode(), std_err.decode(), proc.returncode)


def subprocess_runner_stdin(cmd_list, stdin_response, exercise_dir):
    with subprocess.Popen(
        cmd_list,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        # Use line-buffering (send line when a newline is encountered)
        bufsize=1,
        # Input/output gets converted to/from text
        universal_newlines=True,
        cwd=exercise_dir,
    ) as proc:
        std_out, std_err = proc.communicate(input=stdin_response)
    return (std_out, std_err, proc.returncode)


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_runner(test_case):
    path_obj = Path(test_case)
    python_script = path_obj.name
    script_dir = path_obj.parents[0]
    cmd_list = ["python", python_script]
    std_out, std_err, return_code = subprocess_runner(cmd_list, script_dir)
    assert return_code == 0
    assert std_err == ""


@pytest.mark.parametrize("template, test_input, row_count", TEST_CASES_TEXTFSM)
def test_runner_textfsm(template, test_input, row_count):
    path_obj = Path(template)
    template_file = path_obj.name
    script_dir = path_obj.parents[0]
    path_obj = Path(test_input)
    input_file = path_obj.name
    cmd_list = ["textfsm.py", template_file, input_file]
    std_out, std_err, return_code = subprocess_runner(cmd_list, script_dir)
    # print(std_out)
    assert return_code == 0
    assert std_err == ""
    # Count rows in the FSM output table
    textfsm_rows = re.findall(r"^\[.*\]$", std_out, flags=re.M)
    assert row_count == len(textfsm_rows)
