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
response = adapter.get('/agents')
if response.status_code == 200:
    agents = response.json()['agents']
    alive_agent_hostnames = [agent['host'] for agent in agents if
                             agent['alive']]
else:
    sys.stderr.write('Failed to retrieve Neutron agent list\n')
    sys.exit(1)

servers = cloud.list_servers()

try:
    my_server, = [server for server in servers if
                  server['name'] == server_name and
                  'metadata' in server and 'clusterid' in server.metadata]
except ValueError:
    sys.stderr.write('Failed to get unique server %s \n' % server_name)
    sys.exit(1)

neutron_agent_name = my_server['metadata'].get('neutron_agent_name')

if neutron_agent_name is None:
    name_to_find = server_name
else:
    name_to_find = neutron_agent_name

for agent_hostname in alive_agent_hostnames:
    if name_to_find in agent_hostname:
        sys.exit(0)
sys.stderr.write('Failed to find alive agent for host %s when searching for %s'
                 ' in alive agents %r\n' %
                 (server_name, name_to_find, alive_agent_hostnames))
sys.exit(1)

