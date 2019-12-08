import sys
from enum import IntEnum


class ProgramState(IntEnum):
    waiting = 0
    running = 1
    error = 2
    halt = 3


class IntCodeComputer:
    def __init__(self):
        self.core = []
        self.program_counter = 0
        self.state = ProgramState.waiting
        self.input_buffer = []
        self.output_buffer = []

        self.opcodes = {
            1: self._add,
            2: self._mul,
            3: self._save_input,
            4: self._output,
            5: self._jump_if_true,
            6: self._jump_if_false,
            7: self._less_than,
            8: self._equals,
            99: self._halt
        }

    def load_core(self, core):
        self.core = list(core)
        self.program_counter = 0
        self.state = ProgramState.waiting

    def set_noun_verb(self, noun, verb):
        self.core[1] = noun
        self.core[2] = verb

    def set_input_buffer(self, input_buffer):
        self.input_buffer = input_buffer

    def run(self):
        self.state = ProgramState.running
        while self.state == ProgramState.running:
            self.step()

    def step(self):
        if self.program_counter >= len(self.core):
            self.state = ProgramState.error

        _raw_opcode = self.core[self.program_counter]
        _opcode = _raw_opcode % 100
        mode = _raw_opcode // 100

        opcode = self.opcodes.get(_opcode)
        if opcode is None:
            self.state = ProgramState.error
            return

        opcode(mode)

    def peek(self, i):
        return self.core[i]

    def __str__(self):
        return str(f"[pc={self.program_counter}] {self.core}")

    def _extract_params(self, n, mode):
        idx = self.core[self.program_counter + 1:self.program_counter + n + 1]
        val = [None] * n
        for i in range(n):
            val[i] = self.core[idx[i]] if mode % 10 == 0 else idx[i]
            mode //= 10
        return val

    def _add(self, mode):
        a, b = self._extract_params(2, mode)
        k = self.core[self.program_counter + 3]
        self.core[k] = a + b
        self.program_counter += 4

    def _mul(self, mode):
        a, b = self._extract_params(2, mode)
        k = self.core[self.program_counter + 3]
        self.core[k] = a * b
        self.program_counter += 4

    def _save_input(self, mode):
        self.core[self.core[self.program_counter + 1]] = self.input_buffer.pop()
        self.program_counter += 2

    def _output(self, mode):
        k, = self._extract_params(1, mode)
        self.output_buffer += [k]
        self.program_counter += 2

    def _jump_if_true(self, mode):
        a, b = self._extract_params(2, mode)
        if a:
            self.program_counter = b
        else:
            self.program_counter += 3

    def _jump_if_false(self, mode):
        a, b = self._extract_params(2, mode)
        if not a:
            self.program_counter = b
        else:
            self.program_counter += 3

    def _less_than(self, mode):
        a, b = self._extract_params(2, mode)
        self.core[self.core[self.program_counter + 3]] = 1 if a < b else 0
        self.program_counter += 4

    def _equals(self, mode):
        a, b = self._extract_params(2, mode)
        self.core[self.core[self.program_counter + 3]] = 1 if a == b else 0
        self.program_counter += 4

    def _halt(self, mode):
        self.state = ProgramState.halt


def run_amplification_circuit(phase_vector, core):
    computers = []
    for phase in phase_vector:
        computer = IntCodeComputer()
        computer.load_core(core)
        computer.set_input_buffer([phase])
        computer.state = ProgramState.running
        computer.step()
        computers += [computer]

    signal = 0
    while 1:
        for i in range(len(phase_vector)):
            computers[i].set_input_buffer([signal])
            while len(computers[i].output_buffer) == 0:
                computers[i].step()
                if computers[i].state == ProgramState.halt:
                    return signal
            signal = computers[i].output_buffer.pop()


def permute(phases):
    if len(phases) == 1:
        return [phases]

    return [
        [phases[i]] + p_rest
        for i in range(len(phases))
        for p_rest in permute(phases[:i] + phases[i+1:])
    ]


def main():
    with open(sys.argv[1], "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    max_sig = None
    for phase_vector in permute([5, 6, 7, 8, 9]):
        sig = run_amplification_circuit(phase_vector, core)
        if max_sig is None:
            max_sig = sig
        else:
            max_sig = max(max_sig, sig)

    print(max_sig)


main()
