from l_system import LSystem
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import io

class Plant:
    PLANT_OPTIONS = {
        "basic_plant": {
            "start": "X",
            "rules": {
                "X": "F+[[X]-X]-F[-FX]+X",
                "F": "FF"
            }
        },
        'random_basic_plant': {
            "start": "X",
            "rules": {
                "X1": "F+[[X]-X]-F[-FX]+X",
                "X2": "F-[[X]+X]+F[+FX]-X",
                "F": "FF"
            }           
        }
    }

    DEFAULT_PLOTTING_RULES = {
        "F": lambda x, y, angle: (x + np.cos(angle), y + np.sin(angle)),
        "[": "save",
        "]": "restore",
        "+": "turn_left",
        "-": "turn_right"
    }

    def __init__(self, plant_type: str, new_start: str = None, plotting_rules: dict = DEFAULT_PLOTTING_RULES, angle_increment: float = np.pi / 6, random: bool = False, random_choices: int = 2):
        self.plant_type = plant_type
        self.angle_increment = angle_increment
        if (plant_type not in self.PLANT_OPTIONS):
            raise ValueError("Invalid plant type")
        
        if (new_start is not None):
            self.l_system = LSystem(start=new_start, rules=self.PLANT_OPTIONS[plant_type]["rules"])
        else:
            self.l_system = LSystem(start=self.PLANT_OPTIONS[plant_type]["start"], rules=self.PLANT_OPTIONS[plant_type]["rules"])
        
        self.random = random
        self.random_choices = random_choices
        self.plotting_rules = plotting_rules
        

    def grow(self, iterations: int):
        for _ in range(iterations):
            if self.random:
                self.l_system.iterate_rand(self.random_choices)
            else:
                self.l_system.iterate()
    
    def plot_plant(self) -> io.BytesIO:
        data_stream = io.BytesIO()
        x = 0
        y = 0
        angle = np.pi / 2
        stack = []
        x_vals = []
        y_vals = []

        x_plots = []
        y_plots = []
        for c in self.l_system.current:
            if c not in self.plotting_rules:
                continue
            match self.plotting_rules[c]:
                case "save":
                    stack.append((x, y, angle))
                case "restore":
                    x_plots.append(x_vals)
                    y_plots.append(y_vals)
                    x_vals = []
                    y_vals = []
                    x, y, angle = stack.pop()
                case "turn_left":
                    angle += self.angle_increment
                case "turn_right":
                    angle -= self.angle_increment
                case _:
                    x_vals.append(x)
                    y_vals.append(y)
                    x, y = self.DEFAULT_PLOTTING_RULES[c](x, y, angle)
        
        plt.axis('off')
        plt.plot(x_vals, y_vals, color="darkgoldenrod")
        for i in range(len(x_plots)):
            plt.plot(x_plots[i], y_plots[i], color="darkgoldenrod")
        plt.savefig(data_stream, format="png", bbox_inches='tight', pad_inches=0)
        plt.close()

        return data_stream