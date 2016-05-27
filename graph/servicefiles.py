import re
import os


class ServiceFile:

    name = ""
    description = ""
    requires = []
    wants = []

    def __init__(self, fp):
        self.name = os.path.splitext(os.path.basename(fp.name))[0].split('@')[0]
        lines = fp.readlines()
        self.description = _get_property(lines, "Description")
        self.requires = _get_property(lines, "Requires", list_separator=' ', debug=False)
        self.wants = _get_property(lines, "Wants", list_separator=' ')
        if len(self.wants) == 0:
            print "{} BOOO".format(self.name)

    def __str__(self):
        return "name=\"{}\" description=\"{}\" requires={} wants={}"\
            .format(self.name, self.description, self.requires, self.wants)


def _get_property(lines, property_name, list_separator=None, debug=False):
    pattern = re.compile("^{}=(.*)$".format(property_name))
    if property_name == "Wants":
        print pattern.pattern
    matches = []
    for i, line in enumerate(lines):
        for match in re.finditer(pattern, line):
            matches.append(match)
    if len(matches) > 1:
        raise Exception("{} matches found for property_name={}"
                        .format(len(matches), property_name))
    if len(matches) == 0:
        return []
    if list_separator is not None:
        if debug:
            print "list_separator='{}'".format(list_separator)
        return matches[0].group(1).split(list_separator)
    else:
        return matches[0].group(1)
