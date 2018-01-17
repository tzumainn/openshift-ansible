import json
import sys

import shade
import keystoneauth1


try:
    server_name = sys.argv[1]
except IndexError:
    sys.stderr.write('Hostname expected\n')
    sys.exit(1)

cloud = shade.openstack_cloud()
adapter = keystoneauth1.adapter.Adapter(
    session=cloud.keystone_session,
    service_type=cloud.cloud_config.get_service_type('network'),
    interface=cloud.cloud_config.get_interface('network'),
    endpoint_override=cloud.cloud_config.get_endpoint('network'),
    version=cloud.cloud_config.get_api_version('network'))

servers = cloud.list_servers()
ports = cloud.list_ports()

for port in ports:
    port_host = port['binding:host_id']
    if port_host == server_name:
        request = {'port':
                   {'binding:host_id': str(port['fixed_ips'][0]['ip_address'])}}
        response = adapter.put('/ports/%s' % port['id'], data=json.dumps(request))
        if response.status_code != 200:
            sys.stderr.write('Failed to update port %s binding host id to '
                             '%s' % (port['id'], new_attrs['binding:host_id']))
            sys.exit(1)
        sys.exit(0)
sys.stderr.write('Failed to find a kubelet port with hostname host_id to act '
                 'on\n')
sys.exit(1)

