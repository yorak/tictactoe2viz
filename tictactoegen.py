from collections import namedtuple
from copy import deepcopy

StoredState = namedtuple('StoredState', ['depth', 'state', 'is_winning'])

def is_winning_state(state):
    n = len(state)

    # Check rows and columns
    for i in range(n):
        if state[i][0] != " " and all(state[i][j] == state[i][0] for j in range(n)):
            return True
        if state[0][i] != " " and all(state[j][i] == state[0][i] for j in range(n)):
            return True

    # Check diagonals
    if state[0][0] != " " and all(state[i][i] == state[0][0] for i in range(n)):
        return True
    if state[0][n-1] != " " and all(state[i][n-1-i] == state[0][n-1] for i in range(n)):
        return True

    return False

def flatten_state(state):
    return ''.join(''.join(row) for row in state)

def generate_states(state, player, all_states, state_transitions, depth,
                    depth_limit=None, prune_at_possible_winning_move=False):
    
    if depth_limit is not None and depth>=depth_limit:
        return

    # First collect the possible states
    possible_states = {}
    possible_transitons = []
    winning_states = []
    fromkey = flatten_state(state)
    for i in range(3):
        for j in range(3):
            if state[i][j] == " ":
                state[i][j] = player
                tokey = flatten_state(state)
                possible_transitons.append( (fromkey, tokey) )
                if tokey not in all_states:
                    is_winning = is_winning_state(state)
                    winning_label = player if is_winning else " " 
                    possible_states[tokey] =\
                        StoredState(depth, deepcopy(state), winning_label)
                    if is_winning:
                        winning_states.append( deepcopy(state) )
                state[i][j] = " "
    
    # Recurse as and if needed
    if prune_at_possible_winning_move and winning_states:
        for winning_state in winning_states:
            tokey = flatten_state(winning_state)
            all_states[tokey] = StoredState(depth, winning_state, player)
            state_transitions.append( (fromkey,tokey) )
    else:
        for tokey in possible_states:
            depth, state, winning = possible_states[tokey]
            all_states[tokey] = (depth, state, winning)
            # The game can be continued.
            if winning==" " and (depth_limit is None or depth<=depth_limit):
                editable_state = deepcopy(state)
                generate_states(editable_state, 'O' if player == 'X' else 'X',
                                all_states, state_transitions, depth+1, 
                                depth_limit, prune_at_possible_winning_move)
        state_transitions+=possible_transitons
            
def generate_all_states_and_transitions(depth_limit=None, prune_at_possible_winning_move=False):
    """
    Generates all possible states and transitions of a Tic-Tac-Toe game up to a certain depth.

    :param depth_limit: The maximum depth of states to generate. If None, generates all possible states.
    :return: A tuple containing two dictionaries, one with all states and another with state transitions.

    >>> states, transitions = generate_all_states_and_transitions(1)
    >>> len(states), len(transitions)
    (10, 9)
    >>> states, transitions = generate_all_states_and_transitions(0)
    >>> len(states), len(transitions)
    (1, 0)
    >>> states, transitions = generate_all_states_and_transitions()
    >>> len(states), len(transitions)
    (5478, 16167)
    >>> states, transitions = generate_all_states_and_transitions(None, True)
    >>> len(states), len(transitions)
    (5449, 14301)
    
    # The last one has not been checked
    """

    all_states = {}
    state = [[" "]*3 for _ in range(3)]
    all_states[flatten_state(state)] = StoredState(0, deepcopy(state), " ")
    state_transitions = []
    generate_states(state, 'X', all_states, state_transitions, 0,
                    depth_limit, prune_at_possible_winning_move)

    return all_states, state_transitions


# To run the tests
if __name__ == "__main__":
    #s,t = generate_all_states_and_transitions()
    #print(len(s), len(t))
    import doctest
    doctest.testmod()