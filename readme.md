# dndlang-interpreter

dndlang-interpreter (name subject to change) is a program used to execute code written in dndlang (name subject to change).
dndlang (name subject to change) allows for programming and calculating using dice notation.

## Installation

Download the source code.

## Usage

In the main folder of the project:

```bash
python main.py FILE_PATH
```

Where FILE_PATH is the path to the text file with code written in dndlang (name subject to change).

## Programming language tutorial

### General rules

Every instruction ends with semicolon (';') or an instruction block surrounded with curly brackets ('{' '}'). The variable types are Number, String and Dice.
Number is an integer number.

### Dice notation

The most important feature of dndlang (name subject to change) is the implementation of dice type. For the proper usage knowledge of the dice notation is required.

https://en.wikipedia.org/wiki/Dice_notation

**NOTE:** At the moment d4, d6, etc. isn't an acceptable way of notating the dice value, use 1d4, 1d6, etc. accordingly.

### Examples

Mandatory "Hello, world!" example:

```
?"Hello, world!";
```

Variable declaration:

```
Number num;
String str;
Dice dice;
```

Variable assignment (after declaring variables as shown above):

```
num = 3;
str = "Hello, world!";
dice = 2d6;
```

Printing values:

```
?num;
?str;
?dice;
```
This will result in the following output:

```
3
Hello, world!
2d6
```

Using dice:
```
Dice dice;
dice = 2d6;
?^dice;
```
You can roll without using a variable as well:
```
?^2d6;
```
Both will result in the output ranging from 2 to 12 (as one could expect from rolling a pair of 6-faced dice). But the probability for each number isn't equal: in theory you are six times as likely to roll 7 than 2.

https://en.wikipedia.org/wiki/Central_limit_theorem

Although typing float values in the code isn't possible, you can calculate with fractions using division operator:
```
Number result;
result = 3/4 + 3/4;
?result;
```
Output:
```
1.5
```

Since dice rolls result in a random number, it's possible to do arithmetic operations using them, just like you'd do with normal numbers:
```
?2 * ^1d6 + 3;
```

Defining and calling functions:
```
function add(a, b) {
    return a + b;
}

Number result;
result = add(3, 4);
?result;
result = add(^1d4, ^2d6)
?result;
```

Loops:
```
Number i;
i = 0;
while (i < 10) {
    ?i;
    i = i + 1;
}
```
Output:
```
0
1
2
3
4
5
6
7
8
9
```

Conditional blocks:
```
Number i;
i = 0;
if (i > 0) {
    ?"i is bigger than 0.";
}
else {
    ?"i is not bigger than 0.";
}

if (i == 0) {
    ?"i is equal to 0.";
}
```
Output:
```
i is not bigger than 0.
i is equal to 0.
```
