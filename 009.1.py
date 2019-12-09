import sys
from enum import IntEnum
from typing import List, Union


class ProgramState(IntEnum):
    waiting = 0
    running = 1
    error = 2
    halt = 3


class ParamMode(IntEnum):
    value = 0
    reference = 1


class Param:
    def __init__(self, data, mode):
        self.data = data
        self.mode = mode


class IntCodeComputer:
    def __init__(self):
        self._core = []
        self.program_counter: int = 0
        self.relative_base: int = 0
        self.state = ProgramState.waiting
        self.input_buffer: List[int] = []
        self.output_buffer: List[int] = []

        self.opcodes = {
            1: self._add,
            2: self._mul,
            3: self._save_input,
            4: self._output,
            5: self._jump_if_true,
            6: self._jump_if_false,
            7: self._less_than,
            8: self._equals,
            9: self._adjust_relative_base,
            99: self._halt
        }

    def load_core(self, core):
        self._core = list(core)
        self._reset()

    def _reset(self):
        self.program_counter = 0
        self.relative_base = 0
        self.state = ProgramState.waiting
        self.input_buffer = []
        self.output_buffer = []

    def set_noun_verb(self, noun, verb):
        self.write_value(1, noun)
        self.write_value(2, verb)

    def set_input_buffer(self, input_buffer):
        self.input_buffer = input_buffer

    def run(self):
        self.state = ProgramState.running
        while self.state == ProgramState.running:
            self.step()

    def step(self):
        if self.program_counter >= len(self._core):
            self.state = ProgramState.error

        _raw_opcode = self.read_value(self.program_counter)
        _opcode = _raw_opcode % 100
        mode = _raw_opcode // 100

        opcode = self.opcodes.get(_opcode)
        if opcode is None:
            self.state = ProgramState.error
            return

        opcode(mode)

    def peek(self, i):
        return self.read_value(i)

    def __str__(self):
        return str(f"[pc={self.program_counter}, st={self.state}] {self._core}")

    def _extract_params(self, n, mode):
        idx = [self.read_value(i)
               for i in range(self.program_counter + 1, self.program_counter + n + 1)]
        params: List[Param] = [None] * n
        for i in range(n):
            if mode % 10 == 0:
                params[i] = Param(idx[i], mode=ParamMode.reference)
            elif mode % 10 == 1:
                params[i] = Param(idx[i], mode=ParamMode.value)
            elif mode % 10 == 2:
                params[i] = Param(self.relative_base + idx[i], mode=ParamMode.reference)
            mode //= 10
        return params

    def write_value(self, p: Union[int, Param], v):
        if isinstance(p, Param):
            if p.mode != ParamMode.reference:
                raise RuntimeError("Write attempted in immediate mode!")
            i = p.data
        else:
            i = p

        if i >= len(self._core):
            self._core.extend(0 for _ in range(i + 1 - len(self._core)))
        self._core[i] = v

    def read_value(self, p: Union[int, Param]):
        i = None
        if isinstance(p, Param):
            if p.mode == ParamMode.value:
                return p.data
            elif p.mode == ParamMode.reference:
                i = p.data
        else:
            i = p

        if i >= len(self._core):
            return 0
        return self._core[i]

    def _add(self, mode):
        i, j, k = self._extract_params(3, mode)
        a, b = self.read_value(i), self.read_value(j)
        self.write_value(k, a + b)
        self.program_counter += 4

    def _mul(self, mode):
        i, j, k = self._extract_params(3, mode)
        a, b = self.read_value(i), self.read_value(j)
        self.write_value(k, a * b)
        self.program_counter += 4

    def _save_input(self, mode):
        k, = self._extract_params(1, mode)
        self.write_value(k, self.input_buffer.pop())
        self.program_counter += 2

    def _output(self, mode):
        k, = self._extract_params(1, mode)
        self.output_buffer += [self.read_value(k)]
        self.program_counter += 2

    def _jump_if_true(self, mode):
        a, b = self._extract_params(2, mode)
        if self.read_value(a):
            self.program_counter = self.read_value(b)
        else:
            self.program_counter += 3

    def _jump_if_false(self, mode):
        a, b = self._extract_params(2, mode)
        if not self.read_value(a):
            self.program_counter = self.read_value(b)
        else:
            self.program_counter += 3

    def _less_than(self, mode):
        i, j, k = self._extract_params(3, mode)
        a, b = self.read_value(i), self.read_value(j)
        self.write_value(k, 1 if a < b else 0)
        self.program_counter += 4

    def _equals(self, mode):
        i, j, k = self._extract_params(3, mode)
        a, b = self.read_value(i), self.read_value(j)
        self.write_value(k, 1 if a == b else 0)
        self.program_counter += 4

    def _adjust_relative_base(self, mode):
        k, = self._extract_params(1, mode)
        self.relative_base += self.read_value(k)
        self.program_counter += 2

    def _halt(self, mode):
        self.state = ProgramState.halt


def main():
    with open(sys.argv[1], "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    computer = IntCodeComputer()
    computer.load_core(core)
    computer.set_input_buffer([1])
    computer.run()
    print(computer.output_buffer)


main()
