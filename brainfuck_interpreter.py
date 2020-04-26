import re

class Brainfuck:
    def __init__(self, instructions, memory = [0]):
        self.instructions = re.sub('[^\+\-<>.,\[\]]', '', instructions)

        self.memory = memory
        self.memory_pointer = 0
        self.instruction_pointer = 0

        self.bracket_pairs = self.find_bracket_pairs()
        self.inverse_bracket_pairs = {a: b for b,a in self.bracket_pairs.items()}
        self.MAPPINGS = {
            "+": "add",
            "-": "subtract",
            "<": "decrement_pointer",
            ">": "increment_pointer",
            ".": "output",
            ",": "input",
            "[": "opening_bracket",
            "]": "closing_bracket"
        }

    def find_bracket_pairs(self):
        pairs = {}
        stack = []

        for i, c in enumerate(self.instructions):
            if c == '[':
                stack.append(i)
            elif c == ']':
                if len(stack) == 0:
                    raise IndexError(f"No matching closing bracket for {i}")
                pairs[stack.pop()] = i

        if len(stack) > 0:
            raise IndexError(f"No matching opening bracket for {i}")

        return pairs


    def run_code(self):
        while self.instruction_pointer < len(self.instructions):
            func = getattr(self, self.MAPPINGS.get(self.instructions[self.instruction_pointer]))

            if func:
                func()

            self.instruction_pointer += 1

    def run_code_steps(self):
        print("To go to the next step, press ENTER")
        while self.instruction_pointer < len(self.instructions):
            ok = input("")
            func = getattr(self, self.MAPPINGS.get(self.instructions[self.instruction_pointer]))

            if func:
                func()

            self.instruction_pointer += 1
            print(self.memory)

    def add(self):
        self.memory[self.memory_pointer] += 1

    def subtract(self):
        self.memory[self.memory_pointer] -= 1

    def decrement_pointer(self):
        if self.memory_pointer > 0:
            self.memory_pointer -= 1

    def increment_pointer(self):
        if self.memory_pointer == len(self.memory) - 1:
            self.memory.append(0)

        self.memory_pointer += 1

    def output(self):
        print(chr(self.memory[self.memory_pointer]), end="")

    def input(self):
        while True:
            input_data = int(input("> "))
            if 0 <= input_data <= 127:
                break
            print("Input must be an integer between 0 and 127 ")

        self.memory[self.memory_pointer] = input_data

    def opening_bracket(self):
        if self.memory[self.memory_pointer] == 0:
            self.instruction_pointer = self.bracket_pairs[self.instruction_pointer]

    def closing_bracket(self):
        if self.memory[self.memory_pointer] != 0:
            self.instruction_pointer = self.inverse_bracket_pairs[self.instruction_pointer]

    def __len__(self):
        return len(self.memory)

    def __str__(self):
        return str(self.memory)

    def __repr__(self):
        return self.memory

    def __getitem__(self, memory_pos):
        return self.memory[memory_pos]

ok = Brainfuck("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.")
ok.run_code()