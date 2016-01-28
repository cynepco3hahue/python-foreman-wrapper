# python-foreman-wrapper
Wrapper on Foreman API

## Intro
Help you to add, update and remove elements from foreman collections
```
from foreman_wrapper import ForemanHost

f_h = ForemanHost(
    host_ip="10.11.12.13",
    host_root_password="test",
    foreman_url=...,
    foreman_user=...,
    foreman_password=...
)
f_h.add(build_parameter)
f_h.build()
f_h.run_command(["reboot"])
```
