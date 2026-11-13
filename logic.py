from config import N

def turn(matrix):
    """ Поворот матрицы по часовой стрелке """
    return [list(r) for r in zip(*matrix[::-1])]

def slide(row):
    """ Сдвиг и слияние одной строки """
    r = [v for v in row if v]
    gain = 0
    i = 0
    while i < len(r) - 1:
        if r[i] == r[i + 1]:
            r[i] *= 2
            gain += r[i]
            r.pop(i + 1)
        i += 1
    return r + [0] * (N - len(r)), gain

def move_logic(matrix, k):
    """ Просчет математического сдвига для направления k """
    b = [row[:] for row in matrix]
    gain = 0
    for _ in range(k):
        b = turn(b)
    out = []
    for r in b:
        r, g = slide(r)
        out.append(r)
        gain += g
    for _ in range(4 - k):
        out = turn(out)
    return out, gain