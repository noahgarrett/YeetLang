# YeetLang

## Features so far
- Every program must have a `main` function defined and it must return an integer code
```
fn main() {
    return 1;
}
```

- Function Definitions
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
}
```