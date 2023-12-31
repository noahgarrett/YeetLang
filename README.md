# YeetLang

## GenZ Approved Features
Normal language keywords have alternates for the gen z people to feel safe.
- `fn` -> `bruh` | `bruh main() { }`
- `return` -> `pause` | `bruh main() { pause 1; }`
- `;` -> `rn` | `=` -> `be` | `let` -> `lit`
```js
// Example GenZ Approved Program
bruh main() {
    lit a be 25 rn

    pause a rn
}
```

## Features so far
- Every program must have a `main` function defined and it must return an integer code
```
fn main() {
    return 1;
}
```

- Datatypes
    - int, float, string

- Function Definitions + Function Calling
    - **TEMP** Only i32 data types are allowed to be passed in as parameters and return values for functions
```
fn add(a, b) {
    return a + b;
}

fn main() {
    return add(1, 2);
}
```

- Variable Assignment + Re-assignment
```
fn main() {
    let a = 25;
    a = 5;

    return a;
}
```

- Basic Arithmetic (+-*/)
```
fn main() {
    let a = 1 + 2 - 3 * 4 / (4 - 2);

    return a;
}
```

- Built-in Functions
    - `printf` (C-like printf function)
```
fn main() {
    printf("I have %i apples..", 69);
    
    return 1;
}
```