#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import docker
import requests

client = docker.from_env()

# Testing Opencart build

time.sleep(20)  # we expect all containers are up and running in 20 secs

for c in client.containers.list():
    print("{}: {}" .format(c.name, c.status))
    if 'running' not in c.status:
        print(c.logs())

# # NGINX
nginx = client.containers.get('opencart')
nginx_cfg = nginx.exec_run("/usr/sbin/nginx -T")
assert nginx.status == 'running'
print(nginx.logs())
print(nginx_cfg.output.decode())
# assert 'server_name _;' in nginx_cfg.output.decode()
# assert "error_log /proc/self/fd/2" in nginx_cfg.output.decode()
# assert "location = /.well-known/acme-challenge/" in nginx_cfg.output.decode()
# assert 'HTTP/1.1" 500' not in nginx.logs()


db = client.containers.get('db')
assert db.status == 'running'
cnf = db.exec_run("/usr/sbin/mysqld --verbose  --help")
print(cnf.output.decode())
# assert 'mysqld  Ver 5.7' in cnf.output.decode()
db_log = db.logs()
print(db.logs())
# assert "mysqld: ready for connections" in db_log.decode()

# check redirect to web installer
app = client.containers.get('opencart')
curl = app.exec_run("curl -i http://localhost")
print(curl.output.decode())
# assert 'Location: /setup/' in curl.output.decode()
