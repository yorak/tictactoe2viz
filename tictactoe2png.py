from collections import defaultdict
from PIL import Image, ImageDraw
from functools import reduce
import math

from tictactoegen import generate_all_states_and_transitions


def factors(n):
        step = 2 if n%2 else 1
        return sorted(list(set(reduce(list.__add__,
                    ([i, n//i] for i in range(1, int(math.sqrt(n))+1, step) if n % i == 0)))))

# Assuming all_states is a dictionary where the key is the state key and the value is a tuple (depth, state)
#def organize_by_depth(all_states, max_cnt_inner, max_cnt_outer):
def organize_by_depth(all_states):
    depth_dict = defaultdict(list)
    for state_key, (depth, state, winner) in all_states.items():
        depth_dict[depth].append({'key': state_key, 'state_info': (depth, state, winner)})
        
    #subdivided_depth_dict = defaultdict(defaultdict(list))
    #for 
    
    return depth_dict

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
    max_depth = max(list(organized_states.keys()))
    img_size = (0,0)
    circle_sep = 0
    for depth, states in sorted(organized_states.items()):
        if depth==0: continue
        if depth==2: break
        circle_state_cnt = len(states)
        circle_d = int((cell_size+cell_pad)*circle_state_cnt/(math.pi*(depth/max_depth)))
        circle_img_size = (circle_d*2+cell_size+cell_pad, circle_d*2+cell_size+cell_pad)
        if circle_img_size > img_size:
            img_size = circle_img_size
            print(img_size)
            circle_sep = circle_d/max_depth
        center_x = center_y = img_size[0]/2.0

    img = Image.new('RGB', img_size, color='white')
    draw = ImageDraw.Draw(img)

    for depth, states in organized_states.items():
        num_states = len(states)
        
        for si, state_info in enumerate(states):
            depth, state, winner = state_info['state_info']
            x = center_x + math.sin(2*math.pi*(si/num_states))*depth*circle_sep
            y = center_y + math.cos(2*math.pi*(si/num_states))*depth*circle_sep
            draw_tictactoe_state(draw, (x-cell_size, y-cell_size), cell_size, state)
            
    img.save(f"output/tictactoe.png")

if __name__=="__main__":
    all_states, state_transitions = generate_all_states_and_transitions()
    print("states =",len(all_states), "links =",len(state_transitions))

    
    organized_states = organize_by_depth(all_states)
    
    #per_ring = [None,None,63,63,105,95,95,195,None]
    
    print( [(d, len(s)) for d, s in organized_states.items() ] )
    
    draw(organized_states, 20, 20)