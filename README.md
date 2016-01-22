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

Just add [strace-process.sh](strace-process.sh) as a `PostStart` hook in your
`runc` runtime config. See
[jfrazelle/containers/notify-osd/runtime.json](https://github.com/jfrazelle/containers/blob/master/notify-osd/runtime.json#L87)
as an example.

Huge thanks to [dirtyharrycallahan/pystrace](https://github.com/dirtyharrycallahan/pystrace)
