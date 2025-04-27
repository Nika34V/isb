import math
from scipy.special import gammaincc 

def frequency_test(sequence):
    n = len(sequence)
    s = sum([1 if bit == '1' else -1 for bit in sequence])
    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return {"name": "Частотный побитовый тест", "p_value": round(p_value, 4), "passed": p_value >= 0.01}


def runs_test(sequence):
    n = len(sequence)
    if n < 100:
        return {
            "название": "Тест на чередование битов", 
            "p_value": None, 
            "пройден": False, 
            "ошибка": "Слишком короткая последовательность (минимум 100 бит)"
        }
    
    bits = [int(bit) for bit in sequence]
    
    sum_bits = sum(bits)
    pi = sum_bits / n
    
    threshold = 2 / math.sqrt(n)
    if abs(pi - 0.5) >= threshold:
        return {
            "название": "Тест на чередование битов",
            "p_value": 0.0,
            "пройден": False,
            "причина": f"Не выполнено условие: |{pi:.4f} - 0.5| ≥ {threshold:.4f}",
            "рекомендация": "Доля единиц слишком далека от 50%"
        }
    
    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i-1]:
            runs += 1
    
    numerator = abs(runs - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    p_value = math.erfc(numerator / denominator)
    
    return {
        "название": "Тест на чередование битов",
        "доля_единиц": round(pi, 4),
        "количество_переходов": runs,
        "p_value": round(p_value, 4),
        "пройден": p_value >= 0.01,
        "пороговое_значение": round(threshold, 4),
        "интерпретация": "Последовательность считается случайной" if p_value >= 0.01 
                        else "Последовательность неслучайна"
    }


def longest_run_ones_test(sequence, block_size=8):
    n = len(sequence)
    if n < 128:
        return {
            "название": "Тест на максимальную последовательность единиц", 
            "p_value": None, 
            "пройден": "False",  # Строка вместо bool
            "ошибка": "Слишком короткая последовательность (минимум 128 бит)"
        }
    
    if n % block_size != 0:
        sequence = sequence[:n - (n % block_size)]
        n = len(sequence)
    
    num_blocks = n // block_size
    
    if block_size == 8:
        K = 3
        probabilities = [0.2148, 0.3672, 0.2305, 0.1875]
        categories = ["<=1", "=2", "=3", ">=4"]
    elif block_size == 128:
        K = 5
        probabilities = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
        categories = ["<=4", "=5", "=6", "=7", "=8", ">=9"]
    else:
        return {
            "название": "Тест на максимальную последовательность единиц",
            "p_value": None,
            "пройден": "False", 
            "ошибка": f"Неподдерживаемый размер блока: {block_size}"
        }
    
    counts = [0] * len(probabilities)
    
    for i in range(num_blocks):
        block = sequence[i*block_size : (i+1)*block_size]
        max_run = 0
        current_run = 0
        
        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0
        
        if block_size == 8:
            if max_run <= 1:
                counts[0] += 1
            elif max_run == 2:
                counts[1] += 1
            elif max_run == 3:
                counts[2] += 1
            else:
                counts[3] += 1
        else:
            if max_run <= 4:
                counts[0] += 1
            elif max_run == 5:
                counts[1] += 1
            elif max_run == 6:
                counts[2] += 1
            elif max_run == 7:
                counts[3] += 1
            elif max_run == 8:
                counts[4] += 1
            else:
                counts[5] += 1
    
    chi_squared = 0.0
    for i in range(len(probabilities)):
        expected = probabilities[i] * num_blocks
        chi_squared += (counts[i] - expected)**2 / expected
    
    p_value = gammaincc(K/2, chi_squared/2)
    passed = p_value >= 0.01
    
    return {
        "название": "Тест на максимальную последовательность единиц",
        "размер_блока": block_size,
        "количество_блоков": num_blocks,
        "распределение_категорий": dict(zip(categories, counts)),
        "ожидаемые_вероятности": dict(zip(categories, probabilities)),
        "хи_квадрат": round(chi_squared, 4),
        "p_value": round(p_value, 4),
        "пройден": "True" if passed else "False",  # Строка вместо bool
        "интерпретация": "Последовательность случайна" if passed else "Последовательность неслучайна"
    }