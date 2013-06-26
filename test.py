from phbrainfuck import VM

myvm = VM()
myvm.setCode("++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")
output = myvm.parseCode()
print "".join([chr(x) for x in output])

myvm.reset()
myvm.setCode(">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]<.>+++++++++++[<++++++++>-]<-.--------.+++.------.--------.[-]>++++++++[<++++>-]<+.[-]++++++++++.")

output = myvm.parseCode()
print "".join([chr(x) for x in output])
