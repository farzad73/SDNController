from ipaddress import ip_network, ip_address


class SimpleRouter(object):

    def __init__(self):
        self.portsCounter = 0
        self.ports = {}
        self.table_dict = {}
        self.input_flows = []

    def load_table_file(self, table_file):
        with open(table_file) as table_file_handle:
            for line in table_file_handle.readlines():
                rule_id, subnet, priority, out_port = line.strip().split()
                if not rule_id in self.table_dict:
                    self.table_dict[rule_id] = {'subnet': ip_network(subnet, False),
                                                'priority': priority,
                                                'out_port': out_port}
                else:
                    raise KeyError('Rule with the id {id} already exist.'.format(id=rule_id))

    def load_input_flows(self, input_flow_file):
        with open(input_flow_file) as input_file_handle:
            self.input_flows = [ip_address(line.strip()) for line in input_file_handle.readlines()]

    @staticmethod
    def route_address(table, address):
        route = {}
        for rule_id, subnets_dict in table.items():
            subnet = subnets_dict['subnet']
            priority = subnets_dict['priority']
            out_port = subnets_dict['out_port']

            if address in subnet:
                if priority > route.get('priority', ''):
                    route['address'] = address
                    route['out_port'] = out_port
                    route['match_id'] = rule_id
                    route['priority'] = priority
        return route

    def route(self):
        for address in self.input_flows:
            route_dict = SimpleRouter.route_address(self.table_dict, address)
            if not route_dict:
                print(address, 'X')
            else:
                print(address, route_dict.get('out_port'))


if __name__ == '__main__':
    s1 = SimpleRouter()
    s1.load_table_file("")