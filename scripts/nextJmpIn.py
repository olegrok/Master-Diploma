#!/usr/bin/python3.7

from math import inf

dims = 2
steps = 3
maximal_bp = dims * steps
# From low to high
lower_bound = '001011'[::-1]
upper_bound = '110010'[::-1]


def bit_position(dim, step):
    return dims * (steps - step - 1) + (dims - 1 - dim)


def get_dimension(bit_pos):
    return dims - 1 - bit_pos % dims


def get_step(bit_pos):
    return steps - 1 - (bit_pos // dims)


def next_jmp_in(z_value):

    flag = [0, 0]
    out_step = [inf, inf]
    save_min = [-1, -1]
    save_max = [-1, -1]

    bp = maximal_bp
    while bp > 0:
        bp -= 1
        dim = get_dimension(bp)
        step = get_step(bp)
        if z_value[bp] > lower_bound[bp]:
            if save_min[dim] == -1:
                save_min[dim] = step

        elif z_value[bp] < lower_bound[bp]:
            if flag[dim] == 0 and save_min[dim] == -1:
                out_step[dim] = step
                flag[dim] = -1

        if z_value[bp] < upper_bound[bp]:
            if save_max[dim] == -1:
                save_max[dim] = step
        elif z_value[bp] > upper_bound[bp]:
            if flag[dim] == 0 and save_max[dim] == -1:
                out_step[dim] = step
                flag[dim] = 1

    in_qb = True
    for i in flag:
        if i != 0:
            in_qb = False
            break

    if in_qb:
        return z_value

    min_out_step = 99999
    min_dim = 9999

    for i in range(dims):
        if out_step[i] < min_out_step:
            min_out_step = out_step[i]
            min_dim = i

    max_bp = bit_position(min_dim, min_out_step)
    if flag[min_dim] == 1:
        for new_bp in range(max_bp, maximal_bp):
            if get_step(new_bp) <= save_max[get_dimension(new_bp)] and z_value[new_bp] == '0':
                max_bp = new_bp
                break
        save_min[get_dimension(max_bp)] = get_step(max_bp)
        flag[get_dimension(max_bp)] = 0

    for d in range(dims):
        if flag[d] >= 0:
            if max_bp <= bit_position(d, save_min[d]):
                for i in range(max_bp):
                    if get_dimension(i) == d:
                        l = list(z_value)
                        l[i] = '0'
                        z_value = ''.join(l)
            else:
                for i in range(max_bp):
                    if get_dimension(i) == d:
                        l = list(z_value)
                        l[i] = lower_bound[i]
                        z_value = ''.join(l)
        else:
            for i in range(max_bp):
                if get_dimension(i) == d:
                    l = list(z_value)
                    l[i] = lower_bound[i]
                    z_value = ''.join(l)

    l = list(z_value)
    l[max_bp] = '1'
    z_value = ''.join(l)
    return z_value


test = {
    '001011': '001011',  # 0.2.3
    '001100': '001110',  # 0.3.0
    '001101': '001110',  # 0.3.1
    '001110': '001110',  # 0.3.2
    '001111': '001111',  # 0.3.3
    '010000': '011010',  # 1.0.0 -> 1.2.2
    '010001': '011010',  # 1.0.1 -> 1.2.2
    '010010': '011010',  # 1.0.2 -> 1.2.2
    '010011': '011010',  # 1.0.3 -> 1.2.2
    '011000': '011010',  # 1.2.0 -> 1.2.2
    '011001': '011010',  # 1.2.1 -> 1.2.2
    '011011': '100001',  # 1.2.3 -> 2.0.1
    '011111': '100001',  # 1.3.3 -> 2.0.1
    '101000': '110000',  # 2.2.0 -> 3.0.0
    '101111': '110000',  # 2.3.3 -> 3.0.0
    '110001': '110010',  # 3.0.1 -> 3.0.2
}

for k, v in test.items():
    nji = next_jmp_in(k[::-1])
    if nji == v[::-1]:
        print('OK: {} -> {}'.format(k, nji[::-1]))
    else:
        print('FAIL: {} -> {}. Got: {}'.format(k, v, nji[::-1]))

