import shade
import keystoneauth1

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
    alive_agent_hosts = [agent['host'] for agent in agents if agent['alive']]
    print(alive_agent_hosts)
