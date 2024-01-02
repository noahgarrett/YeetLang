# YeetLang

## GenZ Approved Features
Normal language keywords have alternates for the gen z people to feel safe.
- `fn` -> `bruh` | `bruh main() { }`
- `return` -> `pause` | `bruh main() { pause 1; }`
- `;` -> `rn` | `=` -> `be` | `let` -> `lit`
- `if/else` -> `sus/imposter`
```js
// Example GenZ Approved Program
bruh main() -> int {
    lit a: int be 25 rn

    sus a == 25 {
        printf("oh boi") rn
    } imposter {
        printf("yesssssir") rn
    }

    pause a rn
}
```

## Tests
- Mandelbrot Set script `src/debug/mandel.yeet`
![Mandelbrot](mandel_example.png)

## Features so far
- Every program must have a `main` function defined and it must return an integer code
```
fn main() -> int {
    return 1;
}
```

- Datatypes
    - int
    - float
    - str

- Function Definitions + Function Calling
    - **TEMP** Strings are not allowed to be returned from functions. Working out a bug here
```
fn add(a: int, b: int) -> int {
    return a + b;
}

fn main() -> int {
    return add(1, 2);
}
```

- Variable Assignment + Re-assignment
```
fn main() -> int {
    let a: int = 25;
    a = 5;

    return a;
}
```

- Basic Arithmetic (+-*/)
```
fn main() -> int {
    let a: float = 1 + 2 - 3 * 4 / (4 - 2);

    return a;
}
```

- Built-in Functions
    - `printf` (C-like printf function)
```
fn main() -> int {
    printf("I have %i apples..", 69);
    
    return 1;
}
```

- Loops
    - While Loops
```
fn main() -> int {
    let a: int = 25;

    while a < 50 {
        a = a + 1;
        printf("yeet: %i\n", a);
    }

    return a;
}
```

- Conditionals
```
fn main() -> int {
    let a: int = 0;

    if a == 0 {
        printf("A BE ZERO");
    } else {
        printf("NO ZERO HERE");
    }

    return 0;
}
```
