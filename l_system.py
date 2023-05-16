import random

class LSystem:

    def __init__(self, start: str, rules: dict):
        self.start = start
        self.rules = rules
        self.current = start
        self.curr_iter = 0
    
    def iterate(self):
        result = ""
        for c in self.current:
            if c in self.rules:
                result += self.rules[c]
            else:
                result += c
        
        self.current = result
        self.curr_iter += 1

    def iterate_rand(self, num_choices: int):
        random.seed()
        result = ""
        for c in self.current:
            new_c = c + str(random.randint(1, num_choices))
            if new_c in self.rules:
                result += self.rules[new_c]
            elif c in self.rules:
                result += self.rules[c]
            else:
                result += c
        
        self.current = result
        self.curr_iter += 1
    
    def reset(self):
        self.current = self.start