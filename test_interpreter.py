import sys
from compiler import run, global_env

def run_test(name, lisp_code, expected_result):
    print(f"\nTesting {name}:")
    print(f"Code: {lisp_code}")
    
    # Write test to temporary file
    with open("temp_test.lisp", "w") as f:
        f.write(lisp_code)
    
    # Run the test
    result = run("temp_test.lisp")
    
    # Check result
    success = str(result) == str(expected_result)
    print(f"Expected: {expected_result}")
    print(f"Got: {result}")
    print("✓ PASS" if success else "✗ FAIL")
    return success

def run_all_tests():
    tests = [
        # Basic Tests
        ("Basic Arithmetic", """
        (+ 1 2)
        """, 3),
        
        ("Variable Definition", """
        (define x 10)
        (define y 20)
        (+ x y)
        """, 30),
        
        ("Simple Function", """
        (define square (lambda (x) (* x x)))
        (square 5)
        """, 25),
        
        ("Nested Arithmetic", """
        (+ (* 2 3) (- 10 5))
        """, 11),
        
        ("Conditional", """
        (if (> 5 3) 1 0)
        """, 1),
        
        ("Lists", """
        (define lst (list 1 2 3 4))
        (car lst)
        """, 1),
        
        ("Quote", """
        'x
        """, Symbol("x")),
        
        ("Quoted List", """
        '(1 2 3)
        """, List([Number(1), Number(2), Number(3)])),
        
        ("Lambda with Multiple Args", """
        (define sum (lambda (x y) (+ x y)))
        (sum 5 3)
        """, 8),
        
        ("List Operations", """
        (define lst (list 1 2 3 4))
        (car (cdr lst))
        """, 2),
        
        ("Higher Order Function", """
        (define double (lambda (x) (* x 2)))
        (map double (list 1 2 3))
        """, List([Number(2), Number(4), Number(6)])),

        # Advanced Tests
        ("Nested Lists and Functions", """
        (define lst1 (list 1 2 3))
        (define lst2 (list 4 5 6))
        (list (car lst1) (car (cdr lst2)))
        """, List([Number(1), Number(5)])),

        ("Complex Recursion - Fibonacci", """
        (define fibonacci 
          (lambda (n) 
            (if (< n 2)
                n
                (+ (fibonacci (- n 1)) 
                   (fibonacci (- n 2))))))
        (fibonacci 7)
        """, 13),

        ("Higher Order Function with Lambda", """
        (map (lambda (x) (* x x)) (list 1 2 3 4))
        """, List([Number(1), Number(4), Number(9), Number(16)])),

        ("Nested Lambda Functions", """
        (define make-adder 
          (lambda (x) 
            (lambda (y) (+ x y))))
        (define add5 (make-adder 5))
        (add5 3)
        """, 8),

        ("List Processing - Reverse", """
        (define reverse-helper
          (lambda (lst acc)
            (if (null? lst)
                acc
                (reverse-helper (cdr lst) 
                              (cons (car lst) acc)))))
        (define reverse
          (lambda (lst)
            (reverse-helper lst '())))
        (reverse (list 1 2 3 4))
        """, List([Number(4), Number(3), Number(2), Number(1)])),

        ("Complex Arithmetic", """
        (define square (lambda (x) (* x x)))
        (define cube (lambda (x) (* x x x)))
        (+ (square 3) (cube 2) (* 2 (+ 3 4)))
        """, 31),

        ("List Filter", """
        (define filter
          (lambda (pred lst)
            (if (null? lst)
                '()
                (if (pred (car lst))
                    (cons (car lst) (filter pred (cdr lst)))
                    (filter pred (cdr lst))))))
        (filter (lambda (x) (> x 2)) (list 1 2 3 4 5))
        """, List([Number(3), Number(4), Number(5)])),

        ("Function Composition", """
        (define compose
          (lambda (f g)
            (lambda (x)
              (f (g x)))))
        (define double (lambda (x) (* 2 x)))
        (define square (lambda (x) (* x x)))
        ((compose double square) 3)
        """, 18),

        ("Recursive Factorial", """
        (define factorial 
          (lambda (n) 
            (if (= n 0) 
                1 
                (* n (factorial (- n 1))))))
        (factorial 5)
        """, 120),

        ("Error Handling", """
        (if (= 1 1)
            (+ 1 2)
            (error "This should not happen"))
        """, 3),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, code, expected in tests:
        if run_test(name, code, expected):
            passed += 1
            
    print(f"\nTest Summary: {passed}/{total} tests passed")
    return passed == total

if __name__ == "__main__":
    from compiler import Number, Symbol, List
    success = run_all_tests()
    sys.exit(0 if success else 1) 