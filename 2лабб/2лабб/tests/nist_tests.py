import math
from scipy.special import gammaincc
from typing import Dict, Union, Optional

def frequency_test(sequence: str) -> Dict[str, Union[str, float, bool]]:
    """
    Частотный побитовый тест (Frequency (Monobit) Test)
    Проверяет, является ли количество единиц и нулей в последовательности примерно одинаковым.
    Args:sequence: Строка из битов ('0' и '1') для тестирования 
    Returns:
        Словарь с результатами теста:
        - name: Название теста
        - p_value: Рассчитанное p-value
        - passed: Результат теста (True если p-value ≥ 0.01)
    """
    n = len(sequence)
    s = sum([1 if bit == '1' else -1 for bit in sequence])
    s_obs = abs(s) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return {"name": "Частотный побитовый тест", "p_value": round(p_value, 4), "passed": p_value >= 0.01}

def runs_test(sequence: str) -> Optional[float]:
    """
    Тест на чередование битов (Runs Test)
    Вычисляет p-value для теста на случайность чередований битов.
    Args: sequence: Строка из битов ('0' и '1') для тестирования 
    Returns:float: p-value или None если последовательность невалидна
    """
    try:
        n = len(sequence)
        if n < 100:
            return None
        
        bits = [int(bit) for bit in sequence]
        for bit in bits:
            if bit not in (0, 1):
                return None
        
        sum_bits = sum(bits)
        pi = sum_bits / n
        
        threshold = 2 / math.sqrt(n)
        if abs(pi - 0.5) >= threshold:
            return 0.0
        
        runs = 0
        for i in range(1, n):
            if bits[i] != bits[i-1]:
                runs += 1
        
        numerator = abs(runs - 2 * n * pi * (1 - pi))
        denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
        return math.erfc(numerator / denominator)
    
    except Exception:
        return None

def interpret_runs_test(sequence: str) -> Dict[str, Union[str, float, bool, None]]:
    """
    Интерпретация результатов теста на чередование битов (Runs Test)
    Полная версия теста с интерпретацией результатов.
    Args:sequence: Строка из битов ('0' и '1') для тестирования  
    Returns:
        Словарь с детальными результатами теста:
        - название: Название теста
        - p_value: Рассчитанное p-value или None при ошибке
        - пройден: Результат теста (False при ошибке)
        - дополнительные поля с детализацией
    """
    p_value = runs_test(sequence)
    
    if p_value is None:
        n = len(sequence) if hasattr(sequence, '__len__') else 0
        if n < 100:
            return {
                "название": "Тест на чередование битов", 
                "p_value": None, 
                "пройден": False, 
                "ошибка": "Слишком короткая последовательность (минимум 100 бит)"
            }
        
        try:
            bits = [int(bit) for bit in sequence]
            for bit in bits:
                if bit not in (0, 1):
                    raise ValueError()
        except:
            return {
                "название": "Тест на чередование битов", 
                "p_value": None, 
                "пройден": False, 
                "ошибка": "Последовательность должна содержать только биты (0 или 1)"
            }
        
        return {
            "название": "Тест на чередование битов", 
            "p_value": None, 
            "пройден": False, 
            "ошибка": "Неизвестная ошибка при вычислении p-value"
        }
    
    n = len(sequence)
    sum_bits = sum(int(bit) for bit in sequence)
    pi = sum_bits / n
    threshold = 2 / math.sqrt(n)
    runs = sum(1 for i in range(1, n) if sequence[i] != sequence[i-1])
    
    if p_value == 0.0:
        return {
            "название": "Тест на чередование битов",
            "p_value": 0.0,
            "пройден": False,
            "причина": f"Не выполнено условие: |{pi:.4f} - 0.5| ≥ {threshold:.4f}",
            "рекомендация": "Доля единиц слишком далека от 50%"
        }
    
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

def longest_run_ones_test(sequence: str, block_size: int = 8) -> Dict[str, Union[str, float, bool, None]]:
    """
    Тест на максимальную последовательность единиц (Longest Run of Ones Test)
    Проверяет, соответствует ли длина самой длинной последовательности единиц 
    в блоках ожидаемому распределению для случайной последовательности.
    Args:sequence: Строка из битов ('0' и '1') для тестирования
        block_size: Размер блока (поддерживаются 8 или 128)  
    Returns:
        Словарь с детальными результатами теста:
        - название: Название теста
        - p_value: Рассчитанное p-value или None при ошибке
        - пройден: Результат теста (False при ошибке)
        - дополнительные поля с детализацией
    """
    try:
        n = len(sequence)
        if n < 128:
            raise ValueError("Слишком короткая последовательность (минимум 128 бит)")
        
        if not isinstance(sequence, str):
            raise TypeError("Последовательность должна быть строкой")
        
        if n % block_size != 0:
            sequence = sequence[:n - (n % block_size)]
            n = len(sequence)
        
        num_blocks = n // block_size
        
        match block_size:
            case 8:
                K = 3
                probabilities = [0.2148, 0.3672, 0.2305, 0.1875]
                categories = ["<=1", "=2", "=3", ">=4"]
            case 128:
                K = 5
                probabilities = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
                categories = ["<=4", "=5", "=6", "=7", "=8", ">=9"]
            case _:
                raise ValueError(f"Неподдерживаемый размер блока: {block_size}")
        
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
            
            match block_size:
                case 8:
                    match max_run:
                        case x if x <= 1:
                            counts[0] += 1
                        case 2:
                            counts[1] += 1
                        case 3:
                            counts[2] += 1
                        case _:
                            counts[3] += 1
                case 128:
                    match max_run:
                        case x if x <= 4:
                            counts[0] += 1
                        case 5:
                            counts[1] += 1
                        case 6:
                            counts[2] += 1
                        case 7:
                            counts[3] += 1
                        case 8:
                            counts[4] += 1
                        case _:
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
            "пройден": "True" if passed else "False",
            "интерпретация": "Последовательность случайна" if passed else "Последовательность неслучайна"
        }
    
    except ValueError as e:
        return {
            "название": "Тест на максимальную последовательность единиц", 
            "p_value": None, 
            "пройден": "False",
            "ошибка": str(e)
        }
    except TypeError as e:
        return {
            "название": "Тест на максимальную последовательность единиц", 
            "p_value": None, 
            "пройден": "False",
            "ошибка": str(e)
        }
    except Exception as e:
        return {
            "название": "Тест на максимальную последовательность единиц", 
            "p_value": None, 
            "пройден": "False",
            "ошибка": f"Неожиданная ошибка: {str(e)}"
        }