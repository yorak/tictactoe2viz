from copy import deepcopy
from tictactoegen import generate_all_states_and_transitions

def generate_graphviz_dot(all_states, state_transitions, filename="output/tictactoe_graph.dot"):
    def state_to_table(state_str, winner):
        """Converts a flattened state string to an HTML-like table for GraphViz."""
        html_state_str = state_str

        table_rows = ""
        for i in range(9):
            if i % 3 == 0:
                table_rows += "<tr>"
            char = state_str[i] if state_str[i]!=" " else "&emsp;"
            if winner==char:
                table_rows += f"<td><b>{char}</b></td>"
            else:
                table_rows += f"<td>{char}</td>"
            if i % 3 == 2:
                table_rows += "</tr>"
        return f"<<table border=\"0\" cellborder=\"1\" cellspacing=\"0\">{table_rows}</table>>"

    with open(filename, 'w') as file:
        file.write("digraph G {\n")
        file.write("    node [shape=plain];\n")
        file.write("    overlap=scalexy;\n")
        file.write('    sep="+1";\n')

        # Create nodes for each state
        for state_str, state in all_states.items():
            winner = state[2]
            table = state_to_table(state_str, winner)
            file.write(f'    "{state_str}" [label={table}];\n')

        # Create edges for state transitions
        for src, dst in state_transitions:
            file.write(f'    "{src}" -> "{dst}";\n')

        file.write("}\n")


if __name__=="__main__":
    all_states, state_transitions = generate_all_states_and_transitions()
    print(len(all_states))
    print(len(state_transitions))

    generate_graphviz_dot(all_states, state_transitions)