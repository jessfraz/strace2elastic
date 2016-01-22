# strace2elastic

Strace container output to a file, then shove the syscalls into elastic search. 

```console
$ strace2elastic.py
Usage: strace2elastic.py [OPTIONS] [FILE]

Options:
  -h, --help                        Print this help message and exit
  -e, --elastichost HOST:PORT       Elastic search instance
  -c, --container   CONTAINER_NAME  Container name
```
