import math


def frequency_test(sequence):
    n = len(sequence)
    s = sum([1 if bit == '1' else -1 for bit in sequence])
    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return {"name": "Частотный побитовый тест", "p_value": round(p_value, 4), "passed": p_value >= 0.01}


def runs_test(sequence):
    n = len(sequence)
    pi = sequence.count('1') / n
    if abs(pi - 0.5) >= 0.05:
        return {"name": "Тест на одинаковые подряд идущие биты", "p_value": 0.0, "passed": False}
    v_obs = 1 + sum(sequence[i] != sequence[i + 1] for i in range(n - 1))
    p_value = math.erfc(abs(v_obs - 2 * n * pi * (1 - pi)) / (2 * math.sqrt(2 * n) * pi * (1 - pi)))
    return {"name": "Тест на одинаковые подряд идущие биты", "p_value": round(p_value, 4), "passed": p_value >= 0.01}


def longest_run_ones_test(sequence, block_size=8):
    if len(sequence) % block_size != 0:
        sequence = sequence[:len(sequence) - (len(sequence) % block_size)]

    blocks = [sequence[i:i + block_size] for i in range(0, len(sequence), block_size)]
    counts = [0] * 4  # <=1, ==2, ==3, >=4

    for block in blocks:
        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        match max_run:
            case run if run <= 1:
                counts[0] += 1
            case 2:
                counts[1] += 1
            case 3:
                counts[2] += 1
            case _:
                counts[3] += 1

    expected = [0.2148, 0.3672, 0.2305, 0.1875]
    total_blocks = len(blocks)
    chi_squared = sum([(counts[i] - expected[i] * total_blocks) ** 2 / (expected[i] * total_blocks) for i in range(4)])
    p_value = math.exp(-chi_squared / 2)
    return {"name": "Тест на самую длинную подпоследовательность", "p_value": round(p_value, 4), "passed": p_value >= 0.01}
