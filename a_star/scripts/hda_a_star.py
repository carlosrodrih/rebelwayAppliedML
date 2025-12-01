import hou
import math
import sys
import json

sys.path.append(r"D:\development\rebelwayAppliedML\a_star\scripts")

from a_star import AStarPathFinding

def get_maze_from_grid():
    grid = hou.pwd().parm('grid_path').eval()
    geo = hou.node(grid).geometry()
    
    prims = geo.prims()
    num_rows = num_colums = int(math.sqrt(len(prims)))
    
    grid_matrix = []
    for row in range(num_rows):
        new_row = []
        for col in range(num_colums):
            prim_index = row * num_colums + col
            prim = geo.prim(prim_index)
            color = prim.attribValue("Cd")
            new_row.append(1 if color == (1,1,1) else 0)
        grid_matrix.append(new_row)
        
    return grid_matrix

def get_position_from_object(obj_path,cell_size=1):
    obj = hou.node(obj_path)
    tx, ty, tz = obj.parmTuple("t").eval()
    
    col = int(round(tx / cell_size))
    row = int(round(tz / cell_size))
    
    pos = (row,col)
    return pos

def position_object(obj_path,row,col,cell_size=1):
    main_char = hou.node(obj_path)    
    world_x = col * cell_size
    world_z = row * cell_size
    
    center = main_char.parmTuple("t").eval()
    main_char.parmTuple("t").set((world_x,0,world_z))
    pos = (row,col)
    return pos
    
def get_all_npc_positions():
    count = hou.pwd().parm('npcs').eval()
    npcs = {}
    
    for i in range(1, count + 1):
        parm = f"npc_{i}"
        npc_path = hou.pwd().parm(parm).eval()
        npcs[parm] = get_position_from_object(npc_path)
    
    return npcs
    
def solve_maze():
    main_char_path = hou.pwd().parm("main_char").eval()
    main_pos = get_position_from_object(main_char_path)
    npcs = get_all_npc_positions()
    maze = get_maze_from_grid()
    solutions = {}
    
    for npc_name, npc_pos in npcs.items():
        print("")
        print(f"Solving path for {npc_name}...")
        pathfinder = AStarPathFinding(maze,npc_pos,main_pos)
        path = pathfinder.find_path()
        if path:
            print(f"{npc_name} path found: {path}")
            solutions[npc_name] = path
        else:
            print(f"{npc_name} no path found.")
            solutions[npc_name] = []
            
    json_str = json.dumps(solutions)
    hou.pwd().parm("solutions").set(json_str)

def update_step():
    node = hou.pwd()
    solutions = json.loads(node.parm("solutions").eval())
    for npc_name, npc_path in solutions.items():
        npc_path = solutions[npc_name]
        step = node.parm("step").eval()
        max_step = len(npc_path) - 1
        step = max(0, min(step, max_step))
        row,col = npc_path[step]
        position_object(node.parm(npc_name).eval(), row, col)
    
    

           