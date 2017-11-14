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
