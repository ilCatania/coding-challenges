# Challenge directions 

Implement the method `nextNum()` and a minimal but effective set of unit
tests.
As a quick check, given `RandomNumbers` are `[-1, 0, 1, 2, 3]` and
`Probabilities` are `[0.01, 0.3, 0.58, 0.1, 0.01]` if we call
`nextNum()` 100 times we may get the following results.

```
-1: 1 times
0: 22 times
1: 57 times
2: 20 times
3: 0 times
```

## Python
You may use `random.random()` which returns a pseudo random number
between 0 and 1.

```python
import random

class RandomGen(object):
  # Values that may be returned by next_num()
  _random_nums = []
  # Probability of the occurence of random_nums
  _probabilities = []

  def next_num(self):
  """
  Returns one of the randomNums. When this method is called
  multiple times over a long period, it should return the
  numbers roughly with the initialized probabilities.
  """
  pass
```

Please describe how you might implement this more "pythonically"

## Java

You may use `Random.nextFloat()` which returns a pseudo random number
between 0 and 1.

```java
public class RandomGen {
  // Values that may be returned by nextNum()
  private int[] randomNums;
  // Probability of the occurence of randomNums
  private float[] probabilities;
  /**
    Returns one of the randomNums. When this method is called
    multiple times over a long period, it should return the
    numbers roughly with the initialized probabilities.
  */
  public int nextNum() {
  }
}
```

# Solutions

## Python

The python based solutions can be found under the `python` subfolder.
They are made up of:

1. `random_numbers.py`: a basic implementation following the above
template
2. `random_numbers_pythonic.py`: a more pythonic implementation
3. `tests.py`: a test suite for the above (it tests the pythonic
version by default but this can be toggled by uncommenting the relevant
lines)

The tests can be run from the command line with any python 3
interpreter, for example:

```bash
python3 -m unittest
```

and the expected output would be something like this:

```
.......
----------------------------------------------------------------------
Ran 7 tests in 0.037s

OK
```

Code coverage can be run with `coverage.py`, provided it has been
installed.

## Java

The Java based solution can be found under the `java` subfolder, and it
can be built and tested with gradle. Once built, it can also be run from
the command line, for example:

```bash
java -jar build/libs/random_numbers.jar 4,12,2 .4,.4,.2
```

Code coverage can be run with the `jacocoTestReport` gradle task.
