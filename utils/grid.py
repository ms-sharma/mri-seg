import torch
from torch.nn import ConstantPad2d

def forward_diff(grid):
    nd = len(grid.shape)
    slice1 = [slice(None)]*nd
    slice2 = [slice(None)]*nd

    # Forward difference along x direction
    axis = 3
    slice1[axis] = slice(1, None)
    slice2[axis] = slice(None, -1)
    slice1 = tuple(slice1)
    slice2 = tuple(slice2)

    gridx = torch.nn.ConstantPad2d((0,1,0,0),0)(grid).clone()
    diffx = gridx[slice1] - gridx[slice2]

    # Forward difference along y direction
    axis = 2
    slice1 = [slice(None)]*nd
    slice2 = [slice(None)]*nd
    slice1[axis] = slice(1, None)
    slice2[axis] = slice(None, -1)
    slice1 = tuple(slice1)
    slice2 = tuple(slice2)

    gridy = torch.nn.ConstantPad2d((0,0,0,1),0)(grid).clone()
    diffy = gridy[slice1] - gridy[slice2]

    return torch.cat((diffx,diffy),1)
