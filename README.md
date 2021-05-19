# ECS_CheckMK_plugin

Plugin to integrate Dell EMC ECS Systems into Check_MK

Although the plugin is designed to be used in Check_MK it is implemented as a NAGIOS plugin with Check_MK specific extentions. Thereofore it should be also possible to used it in NAGIOS.

#Installation Copy the plugin to /opt/omd/sites/<SITE>/local/lib/nagios/plugins

uusage: ecs.py [-h] -H HOSTNAME -u USERNAME -p PASSWORD [-d USE_DUMMY] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        hostname or IP address
  -u USERNAME, --username USERNAME
                        username
  -p PASSWORD, --password PASSWORD
                        user password
  -c, --config          build new metric config file


The plugin can be used to get capacity values for all bucktes within all namespaces . 

Define a check within Check_MK under "Classical active and passive Monitoring checks".

To initially create the metric config file use the -c option (directly from the CLI not from Check_MK/nagios) The plugin will auto-create a metric config file in /opt/omd/sites//local/share/check_mk/web/plugins/metrics which allows to beautify the diagrams in Check_MK
