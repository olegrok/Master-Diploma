#!/usr/bin/python3.7

from math import inf

dims = 2
steps = 3
maximal_bp = dims * steps
# From low to high
lower_bound = '00001011'[::-1]
upper_bound = '00110010'[::-1]

def bit_position(dim, step):
    return dims * step + dim

def get_dimension(bit_pos):
    return bit_pos % dims


def get_step(bit_pos):
    return bit_pos // dims


def next_jmp_in(z_value):

    flag = [0, 0]
    out_step = [-inf, -inf]
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

    max_out_step = -1
    max_dim = -1

    for i in range(dims - 1, -1, -1):
        if out_step[i] > max_out_step:
            max_out_step = out_step[i]
            max_dim = i

    max_bp = bit_position(max_dim, max_out_step)

    if flag[max_dim] == 1:
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


test1 = {
    '00001011': '00001011',  # 0.2.3
    '00001100': '00001110',  # 0.3.0
    '00001101': '00001110',  # 0.3.1
    '00001110': '00001110',  # 0.3.2
    '00001111': '00001111',  # 0.3.3
    '00010000': '00011010',  # 1.0.0 -> 1.2.2
    '00010001': '00011010',  # 1.0.1 -> 1.2.2
    '00010010': '00011010',  # 1.0.2 -> 1.2.2
    '00010011': '00011010',  # 1.0.3 -> 1.2.2
    '00011000': '00011010',  # 1.2.0 -> 1.2.2
    '00011001': '00011010',  # 1.2.1 -> 1.2.2
    '00011011': '00100001',  # 1.2.3 -> 2.0.1
    '00011111': '00100001',  # 1.3.3 -> 2.0.1
    '00101000': '00110000',  # 2.2.0 -> 3.0.0
    '00101111': '00110000',  # 2.3.3 -> 3.0.0
    '00110001': '00110010',  # 3.0.1 -> 3.0.2
}

for k, v in test1.items():
    nji = next_jmp_in(k[::-1])
    if nji == v[::-1]:
        print('OK: {} -> {}'.format(k, nji[::-1]))
    else:
        print('FAIL: {} -> {}. Got: {}'.format(k, v, nji[::-1]))


lower_bound = '001011'[::-1]
upper_bound = '100101'[::-1]
test2 = {
    '001011': '001011',  # 0.2.3
    '010000': '100001',  # 1.0.0 -> 2.0.1
    '011111': '100001',  # 1.3.3 -> 2.0.1
    '100010': '100100',  # 2.0.2 -> 2.1.0
    '100011': '100100',  # 2.0.3 -> 2.1.0

}

for k, v in test2.items():
    nji = next_jmp_in(k[::-1])
    if nji == v[::-1]:
        print('OK: {} -> {}'.format(k, nji[::-1]))
    else:
        print('FAIL: {} -> {}. Got: {}'.format(k, v, nji[::-1]))


