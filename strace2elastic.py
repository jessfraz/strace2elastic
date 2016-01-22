#!/usr/bin/python

import getopt
import os.path
import sys
from datetime import datetime

from elasticsearch import Elasticsearch

from strace import *
from strace_utils import *

#
# Add to elastic search
#
def sys2elastic(input_file, container, elastic_host):

    # Open the files
    if input_file is not None:
        f_in = open(input_file, "r")
    else:
        f_in = sys.stdin

    # Connect to elastic search
    es = Elasticsearch([elastic_host])

    print "Shoving syscalls into elastic search, this may take awhile..."

    # Process the file
    strace_stream = StraceInputStream(f_in)
    for entry in strace_stream:
        i_was_unfinished = 0
        if entry.was_unfinished:
            i_was_unfinished = 1

        pid = 0
        if strace_stream.have_pids:
            pid = entry.pid

        syscall = {
                'container': container,
                'timestamp': entry.timestamp,
                'syscall': entry.syscall_name,
                'category': entry.category,
                'split': i_was_unfinished,
                'argc': len(entry.syscall_arguments),
                'arg1': array_safe_get(entry.syscall_arguments, 0),
                'arg2': array_safe_get(entry.syscall_arguments, 1),
                'arg3': array_safe_get(entry.syscall_arguments, 2),
                'arg4': array_safe_get(entry.syscall_arguments, 3),
                'arg5': array_safe_get(entry.syscall_arguments, 4),
                'arg6': array_safe_get(entry.syscall_arguments, 5),
                'result': str(entry.return_value),
                'elapsed': entry.elapsed_time,
                'pid': str(pid),
                }
        res = es.index(index="callmemaybe", doc_type='syscall', body=syscall)
        if res['created'] is not True:
            print res


#
# Print the usage information
#
def usage():
    sys.stderr.write('Usage: %s [OPTIONS] [FILE]\n\n'
            % os.path.basename(sys.argv[0]))
    sys.stderr.write('Options:\n')
    sys.stderr.write('  -h, --help                        Print this help message and exit\n')
    sys.stderr.write('  -e, --elastichost HOST:PORT       Elastic search instance\n')
    sys.stderr.write('  -c, --container   CONTAINER_NAME  Container name\n')

#
# The main function
#
# Arguments:
#   argv - the list of command-line arguments, excluding the executable name
#
def main(argv):
    input_file = None
    elastic_host = None
    container = None

    # Parse the command-line options
    try:
        options, remainder = getopt.gnu_getopt(argv, 'hec:',
                ['help', 'elastichost=', 'container='])

        for opt, arg in options:
            if opt in ('-h', '--help'):
                usage()
                return
            elif opt in ('-e', '--elastichost'):
                elastic_host = arg
            elif opt in ('-c', '--container'):
                container = arg

        if len(remainder) > 1:
            print remainder
            raise Exception("Too many options")
        elif len(remainder) == 1:
            input_file = remainder[0]
    except Exception as e:
        sys.stderr.write("%s: %s\n" % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

    if container is None or container == "":
        sys.stderr.write("container name cannot be empty\n")
        sys.exit(1)

    # Parse strace output and add to elastic search
    try:
        sys2elastic(input_file, container, elastic_host)
    except IOError as e:
        sys.stderr.write("%s: %s\n" % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

#
# Entry point to the application
#
if __name__ == "__main__":
    main(sys.argv[1:])
