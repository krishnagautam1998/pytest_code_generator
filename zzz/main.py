# class Sum:
#     def add(self):
#         a = int(input("Enter the first number: "))
#         b = int(input("Enter the second number: "))
#         return a + b

# res = Sum()
# c = res.add()
# print(c)

# main.py
class Sum:
    def add(self, a: int, b: int) -> int:
        return a + b
    
    def mul(self, a:int,b:int) -> int:
        return a*b
    
    def subs(self, a:int,b:int) -> int:
        return a -b 
    
    def dvd(self, a:int,b:int) -> int:
        return a/b 
