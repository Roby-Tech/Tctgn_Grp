def create_label (x,y,z):

    # direzione destra/sinistra
    threshold_direction = 0.6
    if y > threshold_direction:
        dir_y = 1 # destra
    elif y < -(threshold_direction):
        dir_y = 2 # sinistra
    else:
        dir_y = 0 # fermo

    # direzione avanti/dietro
    threshold_direction = 0.6
    if x > threshold_direction:
        dir_x = 1 # sopra
    elif x < -(threshold_direction):
        dir_x = 2 # sotto
    else:
        dir_x = 0 # fermo

    # direzione sopra/sotto
    threshold_direction = 0.6
    if z > threshold_direction:
        dir_z = 1 # avanti
    elif z < -(threshold_direction):
        dir_z = 2 # indietro
    else:
        dir_z = 0 # fermo

    return [dir_x, dir_y, dir_z]

print(create_label(-7,14,0))