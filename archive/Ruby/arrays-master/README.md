# Arrays

## Setup

### All Platforms:

Install ruby dependencies

```
    $ bundle install
``` 

### On Windows (and only at home):

[Install ansicon](http://softkube.com/blog/ansi-command-line-colors-under-windows) (if not already installed)

Install win32console

```
    $ gem install win32console
```

## Testing

Run the entire test suite

```
    $ ruby arrays_test.rb
```

Run only a specific test

```
    $ ruby arrays_test.rb --name type_test_method_name_here
```

## Goal

Write the following methods. Start with the tests, then use them to create your method.

1. middles

    Given two arrays, each length 3, return a new array containing just their middle elements.
2. max

    Use a loop to find the maximum element in a given numerical array.
3. lucky13?

    An array is lucky13 iff (if and only if) it contains no 1's and no 3's.
4. repeat_separator

    Given two strings, **word** and a **separator**, and a **count**, make a string that has **count** repetitions of **word**, each separated by **separator**. Example: repeat_separator('This', 'And', 2) => 'ThisAndThis'.
5. same_ends?

    Given an array and a length n to check, return true if the n numbers at the start and end of the array are the same. For example, with the array
    [5, 6, 45, 99, 23, 5, 6], the ends are the same for n = 0 and n = 2, and false for n = 1 and n = 3. You may assume n is in the range 0..nums.length .
6. starry?

    A string is starry iff every individual '*' character not at the ends of the string is surrounded by the same character on both sides.
7. plus_it

    Given two strings, word and token, return a version of word where all characters have been replaced by pluses ('+'), except for appearances of the token which are preserved unchanged.
8. zero_front

	Given an array of integers, return an array that contains the exact same numbers but rearranged so that all the zeros are grouped at the start of the array. The relative order of the other numbers should not be changed. Example: [5, 0, 3, 1, 0, 6] => [0, 0, 5, 3, 1, 6]. You may modify and return the given array or make a new array.
9. ten_run

    For each multiple of 10 in the given array, change all the values following it to be that multiple of 10, until encountering another multiple of 10. Example: [2, 10, 3, 4, 20, 5] => [2, 10, 10, 10, 20, 20]
10. max_span

    Consider the leftmost and rightmost appearances of some value in an array. We define the span of this value as the number of elements between the left and right spots, inclusive. A single value has a span of 1. Return the largest span found in the given array. Efficiency is not a priority. Examples (not exhaustive):

    * [1, 2, 1, 1, 3] => 4
    * [1, 4, 2, 1, 4, 1, 4] => 6
    * [1, 4, 2, 1, 4, 4, 4] => 6
