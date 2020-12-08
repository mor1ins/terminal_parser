import lark
import pprint

from lark import Transformer, Visitor, Tree, Token


class TreeToConfiguration(Visitor):
    state = {
        'user_name': None,
        'configuration_name': None,
        'commands': []
    }

    def user_name(self, tree: Tree) -> Tree:
        self.state['user_name'] = tree.children[0].value
        return tree

    def configuration_name(self, tree: Tree) -> Tree:
        self.state['configuration_name'] = tree.children[0].value
        return tree

    def interface_wireless_print_command(self, tree: Tree) -> Tree:
        self.state['commands'].append({'command': ' '.join(map(lambda t: t.value, tree.children))})
        return tree

    def wireless_interface(self, tree: Tree) -> Tree:
        if 'interfaces' not in self.state['commands'][-1].keys():
            self.state['commands'][-1]['interfaces'] = []

        interface = {
            'id': tree.children[0].children[0].value,
        }
        params = tree.children[1]
        while True:
            param_name = '-'.join(params.children[0].children)
            param_value = params.children[2]
            interface[param_name] = param_value

            if isinstance(params.children[3], Token):
                break

            params = params.children[3]


        self.state['commands'][-1]['interfaces'].append(interface)
        return tree


def parser_terminal(text):
    parser = lark.Lark.open('grammar.lark', rel_to=__file__)
    return parser.parse(text)


if __name__ == '__main__':
    tree = parser_terminal(''.join(open('output.txt', 'r').readlines()))
    mikrotik_state_keeper = TreeToConfiguration()
    mikrotik_state_keeper.visit_topdown(tree)
    pprint.pprint(mikrotik_state_keeper.state)
