import random
import re
from collections import OrderedDict

class RegexGenerator:
    def __init__(self, max_repeat=5):
        self.max_repeat = max_repeat
        self.processing_steps = OrderedDict()

    def _log_step(self, stage, before, after, explanation):
        self.processing_steps[stage] = {
            'before': before,
            'after': after,
            'explanation': explanation
        }

    def generate(self, pattern):
        self.processing_steps.clear()
        original = pattern
        self._log_step("0_Start", pattern, None, "Original pattern")

        pattern = self._process_exponents(pattern)
        pattern = self._process_alternations(pattern)
        pattern = self._process_quantifiers(pattern)
        pattern = self._clean_special_chars(pattern)

        return {
            'original': original,
            'result': pattern,
            'steps': self.processing_steps
        }

    def _process_exponents(self, pattern):
        """Handle ^+, ^*, and ^n for both characters and groups"""
        original = pattern

        pattern = re.sub(
            r'(\([^)]+\)|\w)\^\+',
            lambda m: f"{m.group(1)}{{1,{self.max_repeat}}}",
            pattern
        )

        pattern = re.sub(
            r'(\([^)]+\)|\w)\^\*',
            lambda m: f"{m.group(1)}{{0,{self.max_repeat}}}",
            pattern
        )

        pattern = re.sub(
            r'(\([^)]+\)|\w)\^\((\d+)\)',
            lambda m: f"{m.group(1)}{{{m.group(2)}}}",
            pattern
        )

        self._log_step("1_Exponents", original, pattern,
                       "Converted ^+ to {1,N}, ^* to {0,N}, and ^(n) to {n}")
        return pattern

    def _process_alternations(self, pattern):
        """Resolve (a|b|c) patterns by picking one randomly"""
        new_pattern = pattern
        while '|' in new_pattern:
            prev = new_pattern
            new_pattern = re.sub(
                r'\(([^()]*\|[^()]*)\)',
                lambda m: random.choice(m.group(1).split('|')),
                new_pattern
            )
            if new_pattern != prev:
                self._log_step("2_Alternations", prev, new_pattern,
                               f"Resolved alternation: {prev} → {new_pattern}")
        return new_pattern

    def _process_quantifiers(self, pattern):
        """Process {n,m}, {n}, *, +, ? quantifiers"""
        new_pattern = pattern

        # Handle {n,m}
        new_pattern = re.sub(
            r'(\w)\{(\d+),(\d+)\}',
            lambda m: m.group(1) * random.randint(int(m.group(2)), int(m.group(3))),
            new_pattern
        )

        # Handle {n}
        new_pattern = re.sub(
            r'(\w)\{(\d+)\}',
            lambda m: m.group(1) * int(m.group(2)),
            new_pattern
        )

        # Handle *, +, ?
        quant_map = [
            (r'(\w)\*', lambda m: m.group(1) * random.randint(0, self.max_repeat)),
            (r'(\w)\+', lambda m: m.group(1) * random.randint(1, self.max_repeat)),
            (r'(\w)\?', lambda m: m.group(1) if random.random() > 0.5 else '')
        ]

        for q_pattern, q_func in quant_map:
            prev = new_pattern
            new_pattern = re.sub(q_pattern, q_func, new_pattern)
            if new_pattern != prev:
                self._log_step("3_Quantifiers", prev, new_pattern,
                               f"Applied quantifier pattern {q_pattern}")

        return new_pattern

    def _clean_special_chars(self, pattern):
        """Remove leftover special chars like ^ and ·"""
        cleaned = pattern.replace('·', '').replace('^', '')
        if cleaned != pattern:
            self._log_step("4_Cleanup", pattern, cleaned,
                           "Removed special characters like · and ^")
        return cleaned

    def print_processing_steps(self, result):
        print(f"\n{' REGEX PROCESSING STEPS ':=^60}")
        print(f"Original: {result['original']}\n")

        for stage, data in result['steps'].items():
            step_num = stage.split('_')[0]
            print(f"{step_num}. {data['explanation']}")
            if data['after'] is not None:
                print(f"   Before: {data['before']}")
                print(f"   After:  {data['after']}")
            print()

        print(f"Final Result: {result['result']}")
        print('=' * 60 + "\n")


def generate_variant1_with_bonus():
    generator = RegexGenerator()

    print("\n" + "=" * 20 + " PATTERN 1 " + "=" * 20)
    p1 = "(a|b)(c|d)E^+G?"
    result1 = generator.generate(p1)
    print(f"Generated: {result1['result']}")
    generator.print_processing_steps(result1)

    print("\n" + "=" * 20 + " PATTERN 2 " + "=" * 20)
    p2 = "P(Q|R|S)T(uv|w|x)^*Z^+"
    result2 = generator.generate(p2)
    print(f"Generated: {result2['result']}")
    generator.print_processing_steps(result2)

    print("\n" + "=" * 20 + " PATTERN 3 " + "=" * 20)
    p3 = "1(0|1)^*2(3|4)^(5)36"
    result3 = generator.generate(p3)
    print(f"Generated: {result3['result']}")
    generator.print_processing_steps(result3)


generate_variant1_with_bonus()
