from collections import defaultdict
from PIL import Image, ImageDraw
from functools import reduce
import math

from tictactoegen import generate_all_states_and_transitions


def factors(n):
        step = 2 if n%2 else 1
        return sorted(list(set(reduce(list.__add__,
                    ([i, n//i] for i in range(1, int(math.sqrt(n))+1, step) if n % i == 0)))))

""" Re-organize states by their depth 
Assuming all_states is a dictionary where the key is a state key and the
value is a tuple (depth, state, winner), create a dictionary of lists 
for the tuples where the key is the depth."""
def organize_by_depth(all_states):
    depth_dict = defaultdict(list)
    for state_key, (depth, state, winner) in all_states.items():
        depth_dict[depth].append({'key': state_key, 'state_info': (depth, state, winner)})
    return depth_dict

def subdivide_depths(depth_dict, inner_state_max, outer_state_max):
    subdivided_depth_dict = defaultdict(lambda: defaultdict(list))
    max_depth = max(depth_dict.keys())

    for depth, states in depth_dict.items():
        num_states = len(states)
        depth_ratio = depth / max_depth
        max_states_at_depth = int(inner_state_max + depth_ratio * (outer_state_max - inner_state_max))

        # Find optimal number of subdepths
        possible_factors = factors(num_states)
        num_subdepths = min(possible_factors, key=lambda x: abs(x - max_states_at_depth))
        print(num_subdepths)
        for i, state in enumerate(states):
            subdepth = i % num_subdepths
            subdivided_depth_dict[depth][subdepth].append(state)

    return subdivided_depth_dict

def draw_tictactoe_state(draw, top_left, cell_size, state, color='black'):
    x, y = top_left
    board_size = cell_size * 3

    for i in range(1, 3):
        draw.line([(x + i * cell_size, y), (x + i * cell_size, y + board_size)], fill=color)
        draw.line([(x, y + i * cell_size), (x + board_size, y + i * cell_size)], fill=color)

    for row in state:
        for cell in row:
            if cell != " ":
                draw.text((x + 10, y + 10), cell, fill=color)
            x += cell_size
        x = top_left[0]
        y += cell_size

def draw(organized_states, cell_size=50, cell_pad=20):
    max_depth = max(organized_states.keys())

    # 1. Determine image size
    img_size = (0,0)
    circle_sep = 0
    for depth, states_or_subgroups in sorted(organized_states.items()):
        if depth == 0: continue

        # All the subgroups should have the same number of states
        circle_state_cnt = len(states_or_subgroups)
        if type(states_or_subgroups) is not list:
            circle_state_cnt = len(states_or_subgroups[0])

        circle_C = (cell_size+cell_pad)*circle_state_cnt
        circle_d = int(circle_C/(math.pi*(depth/max_depth)))
        circle_img_size = (circle_d*2+cell_size+cell_pad, circle_d*2+cell_size+cell_pad)
        if circle_img_size > img_size:
            img_size = circle_img_size
            circle_sep = circle_d/max_depth
        center_x = center_y = img_size[0]/2.0

    # 2. Initialize image
    img = Image.new('RGB', img_size, color='white')
    draw = ImageDraw.Draw(img)

    # 3. Determine the placing of the states
    for depth, states_or_subgroups in organized_states.items():

        # Wrap plain states (no subgroups) into states with one subgroup
        state_groups = states_or_subgroups
        if type(states_or_subgroups) is list:
            state_groups = dict( 0, states_or_subgroups )

        num_subgroups = len(state_groups)
        middle = (num_subgroups - 1) / 2
        for sgi, states in state_groups:
            num_states = len(states)
            
            for sti, state_info in enumerate(states):
                depth, state, winner = state_info['state_info']
                
                subgroup_r = depth*circle_sep+(sgi-middle)*2*(cell_size+cell_pad)
                base_offset_x = math.sin(2*math.pi*(sti/num_states))*subgroup_r
                base_offset_y = math.cos(2*math.pi*(sti/num_states))*subgroup_r
                x = center_x + base_offset_x
                y = center_y + base_offset_y
                draw_tictactoe_state(draw, (x-cell_size, y-cell_size), cell_size, state)
                
    img.save(f"output/tictactoe.png")

if __name__=="__main__":

    all_states, state_transitions = generate_all_states_and_transitions(2)
    organized_states = organize_by_depth(all_states)
    sub_organized_states = subdivide_depths(organized_states, 60, 240)
    from pprint import pprint
    pprint(sub_organized_states)
    exit()

    all_states, state_transitions = generate_all_states_and_transitions()
    print("states =",len(all_states), "links =",len(state_transitions))

    
    organized_states = organize_by_depth(all_states)
    sub_organized_states = subdivide_depths(organized_states, 60, 240)
    
    #per_ring = [None,None,63,63,105,95,95,195,None]
    
    print( [(d, len(s)) for d, s in organized_states.items() ] )
    
    draw(sub_organized_states, 20, 20)