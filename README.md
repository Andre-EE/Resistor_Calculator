This Python class, ResistorCalculator, is designed to assist users in calculating 
resistor values and finding optimal combinations for gain and divider ratios.

Users can interact with ResistorCalculator by instantiating the ResistorCalculator 
class and calling the 'get_resistors' or 'get_ratios' function with appropriate 
parameters. They can specify the target value, desired topology (single, parallel, 
or series), and ratio type (ratio or divider) to find matching resistor combinations.

Usage example:
```
resistor_calculator = ResistorCalculator()
```
Case 1:
```
resistor_calculator.get_ratios(0.75, 'single', 'divider')
```
Result:
```
target ratio: 0.75
18.7, 56.2; error: -0.1779%
17.4, 52.3; error: -0.1912%
16.2, 48.7; error: -0.2053%
15.8, 47.5; error: -0.2105%
14.7, 44.2; error: -0.2262%
```
Case 2:
```
resistor_calculator.get_ratios(2.33, 'parallel', 'ratio')
```
Result:
```
target ratio: 2.33
23.7, 15.0 // 31.6; error:  0.0000%
13.3, 10.0 // 13.3; error:  0.0000%
45.3, 24.9 // 88.7; error: -0.0005%
80.6, 57.6 // 86.6; error:  0.0009%
30.1, 15.0 // 93.1; error: -0.0011%
53.6, 38.3 // 57.6; error:  0.0014%
```
Case 3:
```
resistor_calculator.get_resistors(41.0, 'series')
```
Result:
```
target resistor: 41.0
13.0 + 28.0; error:  0.0000%
14.3 + 26.7; error:  0.0000%
17.8 + 23.2; error:  0.0000%
20.0 + 21.0; error:  0.0000%
20.5 + 20.5; error:  0.0000%
```
