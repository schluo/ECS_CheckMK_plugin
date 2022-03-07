# ECS_CheckMK_plugin

Plugin to integrate Dell EMC ECS Systems into Check_MK

Although the plugin is designed to be used in Check_MK it is implemented as a NAGIOS plugin with Check_MK specific extentions. Thereofore it should be also possible to used it in NAGIOS.

#Installation Copy the plugin to /opt/omd/sites/{SITE NAME}/local/lib/nagios/plugins

usage: ecs.py [-h] -H HOSTNAME -u USERNAME -p PASSWORD [-d USE_DUMMY] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        hostname or IP address with Port
  -u USERNAME, --username USERNAME
                        username
  -p PASSWORD, --password PASSWORD
                        user password
  -c, --config          build new metric config file

Example:
ecs.py -H 10.10.10.10:4443 -u root -p ChangeMe -c

The plugin can be used to get capacity values for all bucktes within all namespaces . 

Define a check within Check_MK under "Classical active and passive Monitoring checks".

To initially create the metric config file use the -c option (directly from the CLI not from Check_MK/nagios) The plugin will auto-create a metric config file in /opt/omd/sites//local/share/check_mk/web/plugins/metrics which allows to beautify the diagrams in Check_MK

---
  
Copyright (c) 2022 Dell Technologies

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE
