# Language Spec

```cpp
# As of right now, functions cannot return strings.


# All Yeet programs require a 'main' function to serve as the entry point
# This main function returns an `int` data type similar to C
fn main() -> int {
    # Mutable Variable Declaration
    # TODO: Allow the declaration of types
    x = 69          # int
    y = 69.420      # float
    z = "yeet"      # str

    # For Loops | While Loops | Continue | Break
    for i = 0; i < 10; i = i + 1 {
        if i == 4 {
            break
        }

        printf("i = %i\n", i)
    }

    while x < 420 {
        x = x + 10

        if x == 79 {
            continue
        }

        printf("x = %i\n", x)
    }

    # Function Declaration
    fn inside_scope() -> int {
        inside_num = 49
        return inside_num
    }
    
    # Function Calling
    printf("inside_scope = %i", inside_scope())

    # Return Statements
    return 1
}
```