# This is the same int code computer as used in 009

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

    def print(self, val):
        if self.mode == ParamMode.reference:
            return f"([{self.data}] -> {val})"
        else:
            return f"{self.data}"


class IntCodeComputer:
    def __init__(self, debug=False):
        self._core = []
        self.program_counter: int = 0
        self.relative_base: int = 0
        self.state = ProgramState.waiting
        self.input_buffer: List[int] = []
        self.output_buffer: List[int] = []
        self._debug = debug
        self._log = []

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

    def get_log(self):
        return self._log

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
        if self._debug:
            self._log += [f"[{self.program_counter:#4}] ADD {i.print(a)}, {j.print(b)} = {a + b} => [{k.data}]"]
        self.program_counter += 4

    def _mul(self, mode):
        i, j, k = self._extract_params(3, mode)
        a, b = self.read_value(i), self.read_value(j)
        self.write_value(k, a * b)
        if self._debug:
            self._log += [f"[{self.program_counter:#4}] MUL {i.print(a)}, {j.print(b)} = {a * b} => [{k.data}]"]
        self.program_counter += 4

    def _save_input(self, mode):
        k, = self._extract_params(1, mode)
        val = self.input_buffer.pop()
        self.write_value(k, val)
        if self._debug:
            self._log += [f"[{self.program_counter:#4}] INP {val} -> [{k.data}]"]
        self.program_counter += 2

    def _output(self, mode):
        k, = self._extract_params(1, mode)
        val = self.read_value(k)
        self.output_buffer += [val]
        if self._debug:
            self._log += [f"[{self.program_counter:#4}] OUT {k.print(val)}"]
        self.program_counter += 2

    def _jump_if_true(self, mode):
        a, b = self._extract_params(2, mode)
        val_a = self.read_value(a)
        if self._debug:
            self._log += [f"[{self.program_counter:#4}] JMP TRUE {a.print(val_a)}"]

        if val_a:
            val_b = self.read_value(b)
            self.program_counter = val_b
            if self._debug:
                self._log[-1] += f" -> {b.print(val_b)}"
        else:
            self.program_counter += 3
            if self._debug:
                self._log[-1] += f" -> NOJMP"

    def _jump_if_false(self, mode):
        a, b = self._extract_params(2, mode)
        val_a = self.read_value(a)
        if self._debug:
            self._log += [f"[{self.program_counter:#4}] JMP FALSE {a.print(val_a)}"]

        if not val_a:
            val_b = self.read_value(b)
            self.program_counter = val_b
            if self._debug:
                self._log[-1] += f" -> {b.print(val_b)}"
        else:
            self.program_counter += 3
            if self._debug:
                self._log[-1] += f" -> NOJMP"

    def _less_than(self, mode):
        i, j, k = self._extract_params(3, mode)
        a, b = self.read_value(i), self.read_value(j)
        val = 1 if a < b else 0
        self.write_value(k, val)
        if self._debug:
            self._log += [f"[{self.program_counter:#4}] LT {i.print(a)}, {j.print(b)} : {val} => [{k.data}]"]
        self.program_counter += 4

    def _equals(self, mode):
        i, j, k = self._extract_params(3, mode)
        a, b = self.read_value(i), self.read_value(j)
        val = 1 if a == b else 0
        self.write_value(k, val)
        if self._debug:
            self._log += [f"[{self.program_counter:#4}] EQ {i.print(a)}, {j.print(b)} : {val} => [{k.data}]"]
        self.program_counter += 4

    def _adjust_relative_base(self, mode):
        k, = self._extract_params(1, mode)
        val = self.read_value(k)
        self.relative_base += val
        if self._debug:
            self._log += [f"[{self.program_counter:#4}] RELBASE {k.print(val)} -> {self.relative_base}"]
        self.program_counter += 2

    def _halt(self, mode):
        self.state = ProgramState.halt
        if self._debug:
            self._log += [f"[{self.program_counter:#4}] HLT"]
