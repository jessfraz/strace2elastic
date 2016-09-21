FROM python:2-alpine

RUN pip install elasticsearch

COPY strace.py /usr/src/
COPY strace_utils.py /usr/src/
COPY strace2elastic.py /usr/src/
WORKDIR /usr/src

ENTRYPOINT [ "python", "strace2elastic.py" ]
