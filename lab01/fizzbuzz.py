class FizzBuzz:
    """A suite of tools for FizzBuzzing"""
    
    @staticmethod
    def fizzbuzz(n):
        """Prints numbers from 1 to n using fizzbuzz rules"""
        for n in range(1,n+1):
            if n % 3 == 0:
                if n % 5 == 0: print("FizzBuzz")
                else: print("Fizz")
            elif n % 5 == 0: print ("Buzz")
            else: print(n)

if __name__ == "__main__":
    FizzBuzz.fizzbuzz(100)