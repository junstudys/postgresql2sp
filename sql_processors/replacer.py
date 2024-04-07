import re

def replace_content(content: list, regex_params: list) -> list:
    for i, line in enumerate(content):
        for j in range(1, len(regex_params)):
            if '偏移' in line:
                line = re.sub(r"%s" % regex_params[j][1], regex_params[j][3], line, 0, re.I)
            else:
                line = re.sub(r"%s" % regex_params[j][1], regex_params[j][2], line, 0, re.I)
        content[i] = line

    return content
