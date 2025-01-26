import re
import json
from functools import partial
from code_exec import load_data, get_data
import inspect

api = []
trace = []
tools = {}
new_tools = {}
pascal_case_names = []

def set_function_names(value):
    global pascal_case_names
    pascal_case_names = value

def set_tools(value):
    global tools
    tools = value

def format_output(raw):
    try:
        parsed = json.loads(raw)
        # print(json.dumps(parsed, indent=2))
        return parsed
    except:
        # print(raw)
        return raw

def adapt(pascal_case_name, snake_case_name):
    original_function = partial(getattr(tools, pascal_case_name).invoke, {})
    def new_function(**kwargs):
        trace.append({
            "name": snake_case_name,
            "arguments": kwargs
        })
        return format_output(getattr(tools, pascal_case_name).invoke(get_data(), **kwargs))
    new_function.__name__ = snake_case_name
    new_function.__signature__ = inspect.signature(original_function)
    return new_function

def replay(provided_trace=None):
    if provided_trace is None:
        provided_trace = trace
    reset()
    i = 1
    for call in provided_trace:
        print(f"============STEP {i}============")
        print("Call:")
        print(json.dumps(call, indent=2))
        print("Result:")
        print(json.dumps(new_tools[call["name"]](**call["arguments"]), indent=2))
        print()
        i += 1

def export():
    print(json.dumps(trace, indent=2))

def reset():
    global trace
    trace = []

    load_data()

    for pascal_case_name in pascal_case_names:
        snake_case_name = re.sub(r'(?<!^)(?=[A-Z])', '_', pascal_case_name).lower()
        new_tools[snake_case_name] = adapt(pascal_case_name, snake_case_name)
        api.append(getattr(tools, pascal_case_name).get_info())

def get_functions():
    return new_tools

def _export_api():
    print(json.dumps(api))