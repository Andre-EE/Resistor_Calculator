"""
Program Name: ResistorCalculator.py

Purpose:
This Python class, ResistorCalculator, is designed to assist users in calculating 
resistor values and finding optimal combinations for gain and divider ratios.

Usage:
Users can interact with ResistorCalculator by instantiating the ResistorCalculator 
class and calling the 'get_resistors' or 'get_ratios' function with appropriate 
parameters. They can specify the target value, desired topology (single, parallel, 
or series), and ratio type (ratio or divider) to find matching resistor combinations.

Dependencies:
ResistorCalculator has no external dependencies and only utilizes standard Python libraries.

"""

class ResistorCalculator:
    def __init__(self, series: int = 96):
        """
        Initializes the ResistorCalculator with the specified series.

        Parameters:
        series (int): The E-series of standard resistors values.
        """
        self.error_msg = ''

        if series in [3, 6, 12, 24, 48, 96, 192]:
            self.series = series
        else:
            self.series = 96

        self.minimum_number_of_results = 5

        self.resistor_list  = []
        self.parallel_resistor_dict = {}
        self.series_resistor_dict = {}
        self.resistor_ratios = {}
        self.matches = []

        self.gen_resistor_list()
        self.adjust_list_for_coverage()
        self.gen_parallel_and_series_dicts()

    def gen_resistor_list(self):
        """Generates the list of resistors based on the series."""
        if self.series in [3, 6, 12, 24]:
            decimal_points = 0
        else:  
            decimal_points = 1

        for idx in range(self.series + 1):
            r = 10 ** (1 + (idx / self.series))
            r = round(r, decimal_points)
            self.resistor_list.append(r)

    def adjust_list_for_coverage(self):
        """Adjusts values to increase coverage (match real world values)."""
        if self.series in [3, 6, 12, 24]:
            idx = self.resistor_list.index(46)
            self.resistor_list[idx] = 47

        if self.series in [6, 12, 24]:  
            idx = self.resistor_list.index(32)
            self.resistor_list[idx] = 33

        if self.series in [12, 24]:  
            idx = self.resistor_list.index(26)
            self.resistor_list[idx] = 27
            idx = self.resistor_list.index(38)
            self.resistor_list[idx] = 39
            idx = self.resistor_list.index(83)
            self.resistor_list[idx] = 82

        if self.series == 24:
            idx = self.resistor_list.index(29)
            self.resistor_list[idx] = 30
            idx = self.resistor_list.index(35)
            self.resistor_list[idx] = 36
            idx = self.resistor_list.index(42)
            self.resistor_list[idx] = 43

        if self.series == 192:
            idx = self.resistor_list.index(91.9)
            self.resistor_list[idx] = 92.0

    def gen_parallel_and_series_dicts(self):
        """Generates dictionaries containing parallel and series combinations of resistors."""
        for idx, x in enumerate(self.resistor_list):
            for y in self.resistor_list[idx:]:
                self.parallel_resistor_dict[(x, y)] = x * y / (x + y)
                self.series_resistor_dict[(x, y)]   = x + y

    def gen_resistor_ratios(self, topology: str = 'single'):
        """Generates two and three resistor combination ratios"""
        if topology == 'single':
            for x in self.resistor_list:
                for y in self.resistor_list:
                    self.resistor_ratios[(x, y)] = x / y

        elif topology == 'parallel':
            for x in self.resistor_list:
                for key, y in self.parallel_resistor_dict.items():
                    self.resistor_ratios[(x, key)] = x / y
                    self.resistor_ratios[(key, x)] = y / x

        elif topology == 'series':
            for x in self.resistor_list:
                for key, y in self.series_resistor_dict.items():
                    self.resistor_ratios[(x, key)] = x / y
                    self.resistor_ratios[(key, x)] = y / x

    def get_resistors(self, target_resistor, topology: str = 'single'):
        """
        This function finds single resistors or combinations of two resistors that match a given value.

        Parameters:
        target_resistor: The resistor value you're looking for
        topology (str): 'single', 'series', or 'parallel' combination.

        Returns:
        None, instead results are printed in console.
        """
        
        # use smaller error increments for when using series or parallel resistors        
        error_increment = 0.01 if topology == 'single' else 0.001
        self.matches = []
        max_error = 0.0

        if topology == 'single':
            while len(self.matches) < self.minimum_number_of_results:
                for resistor in self.resistor_list:
                    error = (resistor - target_resistor) / target_resistor * 100
                    if (abs(error) < max_error) and (resistor not in self.matches):   
                        self.matches.append(resistor)
                max_error = max_error + error_increment
            # sort matches so lowest error combinations show up first
            self.matches.sort(key=lambda x: abs(x - target_resistor) / target_resistor * 100)
        else:
            if topology == 'parallel':
                resistor_data = self.parallel_resistor_dict
            else: #topology == 'series'
                resistor_data = self.series_resistor_dict

            while len(self.matches) < self.minimum_number_of_results:
                for key, item in resistor_data.items():
                    error = (item - target_resistor) / target_resistor * 100
                    if (abs(error) < max_error) and (key not in self.matches):   
                        self.matches.append(key)
                max_error = max_error + error_increment
            # sort matches so lowest error combinations show up first
            self.matches.sort(key=lambda x: abs(resistor_data[x] - target_resistor) / target_resistor * 100)

        self.print_resistor_results(target_resistor, topology)

    def get_ratios(self, target_ratio: float, topology: str = 'single', ratio_type: str = 'ratio'):
        """
        This function finds ratios of two resistors or combinations of three resistors that match a given ratio.

        Parameters:
        target_ratio: The ratio value you're looking for.
        topology (str): 'single', 'series', or 'parallel' combination.
        ratio_type (str): 'ratio' and 'divider' specify the type of ratio to return: 'x / y' or 'x / (x + y)'

        Returns:
        None, instead results are printed in console.
        """
        self.gen_resistor_ratios(topology)

        # use smaller error increments for when using series or parallel resistors
        error_increment = 0.01 if topology == 'single' else 0.001
        max_error = 0.0
        self.matches = []

        # compute the target ratio if resistor divider ratio is requested
        if ratio_type == 'divider':
            if target_ratio > 1.0:
                self.error_msg = 'divider ratio cannot be greater than 1'
            else:
                target_ratio = 1 / target_ratio - 1

        # find matching resistor combinations using brute force 
        if self.error_msg == '':    
            while len(self.matches) < self.minimum_number_of_results:
                for key, item in self.resistor_ratios.items():
                    error = (item - target_ratio) / target_ratio * 100
                    if (abs(error) < max_error) and (key not in self.matches):   
                        self.matches.append(key)
                max_error = max_error + error_increment

            # sort matches so lowest error combinations show up first
            self.matches.sort(key=lambda x: abs(self.resistor_ratios[x] - target_ratio) / target_ratio * 100)

            self.print_ratio_results(target_ratio, topology, ratio_type)

        else:
            print(self.error_msg)

    def print_resistor_results(self, target_resistor, topology: str = 'single'):
        
        print(f"target resistor: {target_resistor}")

        for resistor in self.matches:
            if topology == 'single':
                error = (resistor - target_resistor) / target_resistor * 100
                print(f"{resistor}; error: {error:7.4f}%")
            elif topology == 'parallel':
                error = (self.parallel_resistor_dict[resistor] - target_resistor) / target_resistor * 100
                print(f"{resistor[0]} // {resistor[1]}; error: {error:7.4f}%")
            elif topology == 'series':
                error = (self.series_resistor_dict[resistor] - target_resistor) / target_resistor * 100
                print(f"{resistor[0]} + {resistor[1]}; error: {error:7.4f}%")

    def print_ratio_results(self, target_ratio: float, topology: str = 'single', ratio_type: str = 'ratio'):

        print_ratio = target_ratio if ratio_type == 'ratio' else (1 / (target_ratio + 1))
        print(f"target ratio: {print_ratio}")

        for key in self.matches:
            error = (self.resistor_ratios[key] - target_ratio) / target_ratio * 100

            if topology == 'single':
                print(f"{key[0]}, {key[1]}; error: {error:7.4f}%")

            elif topology == 'parallel':
                if type(key[0]) is tuple:
                    print(f"{key[0][0]} // {key[0][1]}, {key[1]}; error: {error:7.4f}%")
                else:
                    print(f"{key[0]}, {key[1][0]} // {key[1][1]}; error: {error:7.4f}%")

            elif topology == 'series':
                if type(key[0]) is tuple:
                    print(f"{key[0][0]} + {key[0][1]}, {key[1]}; error: {error:7.4f}%")
                else:
                    print(f"{key[0]}, {key[1][0]} + {key[1][1]}; error: {error:7.4f}%")
                
resistor_calculator = ResistorCalculator()

resistor_calculator.get_ratios(0.75, 'single', 'ratio')
resistor_calculator.get_resistors(45.0, 'series')