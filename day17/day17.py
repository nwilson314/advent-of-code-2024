from collections import deque
from enum import Enum
from multiprocessing import Pool, cpu_count
import time

def parse_input(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        return lines

def search_range(program, start, end, pid, max_found):
    computer = ThreeBitComputer(start, 0, 0)
    return computer.run_correction(program, start, end, pid, max_found)

class ThreeBitComputer:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.inst_p = 0
        self.output = []

    def run(self, program):
        while self.inst_p < len(program):
            opcode = program[self.inst_p]
            operand = program[self.inst_p + 1]
            val = self.execute_opcode(opcode, operand)
            if val is not True:
                self.inst_p += 2
        return ",".join([str(x) for x in self.output]), self.output

    def run_correction(self, program, start, end, pid, max_found):
        initial_a = start
        while initial_a < end:
            self.a = initial_a
            self.output = []
            self.b = 0
            self.c = 0
            self.inst_p = 0

            while self.inst_p < len(program):
                opcode = program[self.inst_p]
                operand = program[self.inst_p + 1]
                val = self.execute_opcode(opcode, operand)
                if self.output and self.output[-1] != program[len(self.output) -1]:
                    break
                if val is not True:
                    self.inst_p += 2

                if len(self.output) >= max_found and len(self.output) != 0:
                    max_found = len(self.output)
                    print(f"Process {pid} ({start}-{end}): trying {initial_a} (oct: {oct(initial_a)}) with {self.output}")

            if self.output == program:
                print(f"Found solution: {initial_a} (oct: {oct(initial_a)})")
                return initial_a, max_found
                
            initial_a += 1
        return None, max_found

    def reset(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.inst_p = 0
        self.output = []

    def find_matches_at_level(self, program, level, base_numbers, prev_best_suffixes=None):
        matches = []
        suffix_patterns = {}
        suffix_length = max(1, level - 1)  
        max_output_length = min(level + 3, len(program))
        
        if prev_best_suffixes and level > 3:
            print(f"\nUsing previous best suffixes: {prev_best_suffixes}")
            new_base_numbers = [
                base for base in base_numbers 
                if any(oct(base)[2:].endswith(suffix) for suffix in prev_best_suffixes)
            ]
            base_numbers = new_base_numbers
            print(f"Filtered to {len(base_numbers)} numbers ending with best suffixes")
        
        for base in base_numbers:
            base_oct = oct(base)[2:]
            for prefix in range(64):
                prefix_oct = oct(prefix)[2:]
                try:
                    test_val = int(f"0o{prefix_oct}{base_oct}", 8)
                    self.reset()
                    self.a = test_val
                    output = self.run(program)[1]
                    
                    if (output[:level] == program[:level] and 
                        len(output) <= max_output_length):
                        matches.append(test_val)
                        oct_str = oct(test_val)[2:]
                        suffix = oct_str[-suffix_length:] if len(oct_str) >= suffix_length else oct_str
                        suffix_patterns[suffix] = suffix_patterns.get(suffix, 0) + 1
                except ValueError:
                    continue
        
        best_suffixes = [s for s, _ in sorted(suffix_patterns.items(), 
                                            key=lambda x: x[1], 
                                            reverse=True)[:4]]
        print(f"\nMost common {suffix_length}-digit suffixes at level {level}:")
        for suffix in best_suffixes:
            print(f"  Suffix '{suffix}' appeared {suffix_patterns[suffix]} times")
            
        return matches, best_suffixes

    def run_correction_corrected(self, program):
        first_matches = []
        for i in range(500):
            self.reset()
            self.a = i
            output = self.run(program)[1]
            if output[:1] == program[:1]:
                first_matches.append(i)
        
        print(f"Level 1: Found {len(first_matches)} matches")
        
        current_matches = first_matches
        best_suffixes = None
        for level in range(2, len(program) + 1):
            current_matches, best_suffixes = self.find_matches_at_level(
                program, level, current_matches, best_suffixes)
            
            if not current_matches:
                break
            
            self.reset()
            self.a = current_matches[-1]
            best_output = self.run(program)[1]
            print(f"Level {level}: Found {len(current_matches)} matches. "
                  f"Best: {current_matches[-1]} (oct: {oct(current_matches[-1])}) "
                  f"-> {best_output}")
        
        return current_matches[0] if current_matches else None

    def adv(self, operand: int):
        op = self.get_combo_operand(operand)
        self.a = self.a // (2 ** op)
        return self.a

    def bxl(self, operand: int):
        self.b = self.b ^ operand
        return self.b

    def bst(self, operand: int):
        op = self.get_combo_operand(operand)
        self.b = op % 8
        return self.b

    def jnz(self, operand: int):
        if self.a == 0:
            return False
        self.inst_p = operand
        return True

    def bxc(self, _operand: int):
        self.b = self.b ^ self.c
        return self.b
    
    def out(self, operand: int):
        op = self.get_combo_operand(operand)
        return op % 8

    def bdv(self, operand: int):
        op = self.get_combo_operand(operand)
        self.b = self.a // (2 ** op)
        return self.b

    def cdv(self, operand: int):
        op = self.get_combo_operand(operand)
        self.c = self.a // (2 ** op)
        return self.c

    def execute_opcode(self, code: int, operand: int):
        match code:
            case 0:
                return self.adv(operand)
            case 1:
                return self.bxl(operand)
            case 2:
                return self.bst(operand)
            case 3:
                return self.jnz(operand)
            case 4:
                return self.bxc(operand)
            case 5:
                self.output.append(self.out(operand))
                return self.out(operand)
            case 6:
                return self.bdv(operand)
            case 7:
                return self.cdv(operand)
            case _:
                raise ValueError
    
    def get_combo_operand(self, operand: int):
        match operand:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return 2
            case 3:
                return 3
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise ValueError


def part2_multi_process_brute(program):
    num_processes = 1 #* cpu_count()
    chunk_size = 10000  
    start_point = 1  
    max_found = 0
    ranges = [(start_point + i * chunk_size, start_point + (i + 1) * chunk_size) for i in range(num_processes)]
    
    start_time = time.time()
    
    with Pool(num_processes) as pool:
        results = []
        for i, (start, end) in enumerate(ranges):
            results.append(pool.apply_async(search_range, (program, start, end, i, max_found)))
        
        while True:
            all_done = True
            for r in results:
                if r.ready():
                    result = r.get()
                    if result[0] is not None:
                        elapsed = time.time() - start_time
                        print(f"Found solution: {result} in {elapsed:.2f} seconds")
                        pool.terminate()
                        exit(0)
                    else:
                        if result[1] > max_found:
                            max_found = result[1]
                else:
                    all_done = False
            if all_done:
                last_end = max(end for _, end in ranges)
                ranges = [(last_end + i * chunk_size, last_end + (i + 1) * chunk_size) for i in range(num_processes)]
                results = []
                for i, (start, end) in enumerate(ranges):
                    results.append(pool.apply_async(search_range, (program, start, end, i, max_found)))


if __name__ == "__main__":
    lines = parse_input("input.txt")

    for line in lines:
        if line.startswith("Register A:"):
            a = int(line.split(" ")[2])
        elif line.startswith("Register B:"):
            b = int(line.split(" ")[2])
        elif line.startswith("Register C:"):
            c = int(line.split(" ")[2])
        elif line.startswith("Program:"):
            meh = line.split(" ")
            program = [int(x) for x in meh[1].split(",")]
            break

    computer = ThreeBitComputer(a, b, c)
    print(f"Part 1: {computer.run(program)[0]}")

    answer = computer.run_correction_corrected(program)
    print(f"Part 2: {answer}")
