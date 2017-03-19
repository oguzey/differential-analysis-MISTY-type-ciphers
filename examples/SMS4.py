from variable import Variable
from variable import TypeVariable
from side import Side
from transition import Transition
from transition import SystemTransition

a1 = Variable(TypeVariable.INPUT)
a2 = Variable(TypeVariable.INPUT)
a3 = Variable(TypeVariable.INPUT)
a4 = Variable(TypeVariable.INPUT)
a5 = Variable(TypeVariable.INPUT)

g1 = Variable(TypeVariable.OUTPUT)
g2 = Variable(TypeVariable.OUTPUT)
g3 = Variable(TypeVariable.OUTPUT)
g4 = Variable(TypeVariable.OUTPUT)
g5 = Variable(TypeVariable.OUTPUT)

b1 = Variable(TypeVariable.UNKNOWN)
b2 = Variable(TypeVariable.UNKNOWN)
b3 = Variable(TypeVariable.UNKNOWN)
b4 = Variable(TypeVariable.UNKNOWN)
b5 = Variable(TypeVariable.UNKNOWN)
b6 = Variable(TypeVariable.UNKNOWN)
b7 = Variable(TypeVariable.UNKNOWN)
b8 = Variable(TypeVariable.UNKNOWN)
b9 = Variable(TypeVariable.UNKNOWN)
b10 = Variable(TypeVariable.UNKNOWN)

# 3 blocks
three_blocks_systems = {}

# 3 rounds
ts1 = Transition(Side(a2, a3), Side(g1, a1))
ts2 = Transition(Side(a3, g1), Side(g2, a2))
ts3 = Transition(Side(g1, g2), Side(g3, a3))
system = SystemTransition(ts1, ts2, ts3)
three_blocks_systems["3"] = system

# 4 rounds
ts1 = Transition(Side(a2, a3), Side(b1, a1))
ts2 = Transition(Side(a3, b1), Side(g1, a2))
ts3 = Transition(Side(b1, g1), Side(g2, a3))
ts4 = Transition(Side(g1, g2), Side(g3, b1))
system = SystemTransition(ts1, ts2, ts3, ts4)
three_blocks_systems["4"] = system

# 5 rounds
ts1 = Transition(Side(a2, a3), Side(b1, a1))
ts2 = Transition(Side(a3, b1), Side(b2, a2))
ts3 = Transition(Side(b1, b2), Side(g1, a3))
ts4 = Transition(Side(b2, g1), Side(g2, b1))
ts5 = Transition(Side(g1, g2), Side(g3, b2))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5)
three_blocks_systems["5"] = system

#  6 rounds
ts1 = Transition(Side(a2, a3), Side(b1, a1))
ts2 = Transition(Side(a3, b1), Side(b2, a2))
ts3 = Transition(Side(b1, b2), Side(b3, a3))
ts4 = Transition(Side(b2, b3), Side(g1, b1))
ts5 = Transition(Side(b3, g1), Side(g2, b2))
ts6 = Transition(Side(g1, g2), Side(g3, b3))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6)
three_blocks_systems["6"] = system

# 7
ts1 = Transition(Side(a2, a3), Side(b1, a1))
ts2 = Transition(Side(a3, b1), Side(b2, a2))
ts3 = Transition(Side(b1, b2), Side(b3, a3))
ts4 = Transition(Side(b2, b3), Side(b4, b1))
ts5 = Transition(Side(b3, b4), Side(g1, b2))
ts6 = Transition(Side(b4, g1), Side(g2, b3))
ts7 = Transition(Side(g1, g2), Side(g3, b4))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7)
three_blocks_systems["7"] = system

# 8
ts1 = Transition(Side(a2, a3), Side(b1, a1))
ts2 = Transition(Side(a3, b1), Side(b2, a2))
ts3 = Transition(Side(b1, b2), Side(b3, a3))
ts4 = Transition(Side(b2, b3), Side(b4, b1))
ts5 = Transition(Side(b3, b4), Side(b5, b2))
ts6 = Transition(Side(b4, b5), Side(g1, b3))
ts7 = Transition(Side(b5, g1), Side(g2, b4))
ts8 = Transition(Side(g1, g2), Side(g3, b5))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8)
three_blocks_systems["8"] = system

# 9
ts1 = Transition(Side(a2, a3), Side(b1, a1))
ts2 = Transition(Side(a3, b1), Side(b2, a2))
ts3 = Transition(Side(b1, b2), Side(b3, a3))
ts4 = Transition(Side(b2, b3), Side(b4, b1))
ts5 = Transition(Side(b3, b4), Side(b5, b2))
ts6 = Transition(Side(b4, b5), Side(b6, b3))
ts7 = Transition(Side(b5, b6), Side(g1, b4))
ts8 = Transition(Side(b6, g1), Side(g2, b5))
ts9 = Transition(Side(g1, g2), Side(g3, b6))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9)
three_blocks_systems["9"] = system

# 10
ts1 = Transition(Side(a2, a3), Side(b1, a1))
ts2 = Transition(Side(a3, b1), Side(b2, a2))
ts3 = Transition(Side(b1, b2), Side(b3, a3))
ts4 = Transition(Side(b2, b3), Side(b4, b1))
ts5 = Transition(Side(b3, b4), Side(b5, b2))
ts6 = Transition(Side(b4, b5), Side(b6, b3))
ts7 = Transition(Side(b5, b6), Side(b7, b4))
ts8 = Transition(Side(b6, b7), Side(g1, b5))
ts9 = Transition(Side(b7, g1), Side(g2, b6))
ts10 = Transition(Side(g1, g2), Side(g3, b7))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10)
three_blocks_systems["10"] = system

# 11
ts1 = Transition(Side(a2, a3), Side(b1, a1))
ts2 = Transition(Side(a3, b1), Side(b2, a2))
ts3 = Transition(Side(b1, b2), Side(b3, a3))
ts4 = Transition(Side(b2, b3), Side(b4, b1))
ts5 = Transition(Side(b3, b4), Side(b5, b2))
ts6 = Transition(Side(b4, b5), Side(b6, b3))
ts7 = Transition(Side(b5, b6), Side(b7, b4))
ts8 = Transition(Side(b6, b7), Side(b8, b5))
ts9 = Transition(Side(b7, b8), Side(g1, b6))
ts10 = Transition(Side(b8, g1), Side(g2, b7))
ts11 = Transition(Side(g1, g2), Side(g3, b8))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10, ts11)
three_blocks_systems["11"] = system

# 12
ts1 = Transition(Side(a2, a3), Side(b1, a1))
ts2 = Transition(Side(a3, b1), Side(b2, a2))
ts3 = Transition(Side(b1, b2), Side(b3, a3))
ts4 = Transition(Side(b2, b3), Side(b4, b1))
ts5 = Transition(Side(b3, b4), Side(b5, b2))
ts6 = Transition(Side(b4, b5), Side(b6, b3))
ts7 = Transition(Side(b5, b6), Side(b7, b4))
ts8 = Transition(Side(b6, b7), Side(b8, b5))
ts9 = Transition(Side(b7, b8), Side(b9, b6))
ts10 = Transition(Side(b8, b9), Side(g1, b7))
ts11 = Transition(Side(b9, g1), Side(g2, b8))
ts12 = Transition(Side(g1, g2), Side(g3, b9))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10, ts11, ts12)
three_blocks_systems["12"] = system

# 13
ts1 = Transition(Side(a2, a3), Side(b1, a1))
ts2 = Transition(Side(a3, b1), Side(b2, a2))
ts3 = Transition(Side(b1, b2), Side(b3, a3))
ts4 = Transition(Side(b2, b3), Side(b4, b1))
ts5 = Transition(Side(b3, b4), Side(b5, b2))
ts6 = Transition(Side(b4, b5), Side(b6, b3))
ts7 = Transition(Side(b5, b6), Side(b7, b4))
ts8 = Transition(Side(b6, b7), Side(b8, b5))
ts9 = Transition(Side(b7, b8), Side(b9, b6))
ts10 = Transition(Side(b8, b9), Side(b10, b7))
ts11 = Transition(Side(b9, b10), Side(g1, b8))
ts12 = Transition(Side(b10, g1), Side(g2, b9))
ts13 = Transition(Side(g1, g2), Side(g3, b10))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10, ts11, ts12, ts13)
three_blocks_systems["13"] = system


# 4 blocks
four_blocks_systems = {}

# 4 rounds
ts1 = Transition(Side(a2, a3, a4), Side(g1, a1))
ts2 = Transition(Side(a3, a4, g1), Side(g2, a2))
ts3 = Transition(Side(a4, g1, g2), Side(g3, a3))
ts4 = Transition(Side(g1, g2, g3), Side(g4, a4))
system = SystemTransition(ts1, ts2, ts3, ts4)
four_blocks_systems["4"] = system

# 5 rounds
ts1 = Transition(Side(a2, a3, a4), Side(b1, a1))
ts2 = Transition(Side(a3, a4, b1), Side(g1, a2))
ts3 = Transition(Side(a4, b1, g1), Side(g2, a3))
ts4 = Transition(Side(b1, g1, g2), Side(g3, a4))
ts5 = Transition(Side(g1, g2, g3), Side(g4, b1))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5)
four_blocks_systems["5"] = system

# 6 rounds
ts1 = Transition(Side(a2, a3, a4), Side(b1, a1))
ts2 = Transition(Side(a3, a4, b1), Side(b2, a2))
ts3 = Transition(Side(a4, b1, b2), Side(g1, a3))
ts4 = Transition(Side(b1, b2, g1), Side(g2, a4))
ts5 = Transition(Side(b2, g1, g2), Side(g3, b1))
ts6 = Transition(Side(g1, g2, g3), Side(g4, b2))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6)
four_blocks_systems["6"] = system

# 7 rounds
ts1 = Transition(Side(a2, a3, a4), Side(b1, a1))
ts2 = Transition(Side(a3, a4, b1), Side(b2, a2))
ts3 = Transition(Side(a4, b1, b2), Side(b3, a3))
ts4 = Transition(Side(b1, b2, b3), Side(g1, a4))
ts5 = Transition(Side(b2, b3, g1), Side(g2, b1))
ts6 = Transition(Side(b3, g1, g2), Side(g3, b2))
ts7 = Transition(Side(g1, g2, g3), Side(g4, b3))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7)
four_blocks_systems["7"] = system

# 8 rounds
ts1 = Transition(Side(a2, a3, a4), Side(b1, a1))
ts2 = Transition(Side(a3, a4, b1), Side(b2, a2))
ts3 = Transition(Side(a4, b1, b2), Side(b3, a3))
ts4 = Transition(Side(b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b2, b3, b4), Side(g1, b1))
ts6 = Transition(Side(b3, b4, g1), Side(g2, b2))
ts7 = Transition(Side(b4, g1, g2), Side(g3, b3))
ts8 = Transition(Side(g1, g2, g3), Side(g4, b4))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8)
four_blocks_systems["8"] = system

# 9 rounds
ts1 = Transition(Side(a2, a3, a4), Side(b1, a1))
ts2 = Transition(Side(a3, a4, b1), Side(b2, a2))
ts3 = Transition(Side(a4, b1, b2), Side(b3, a3))
ts4 = Transition(Side(b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b2, b3, b4), Side(b5, b1))
ts6 = Transition(Side(b3, b4, b5), Side(g1, b2))
ts7 = Transition(Side(b4, b5, g1), Side(g2, b3))
ts8 = Transition(Side(b5, g1, g2), Side(g3, b4))
ts9 = Transition(Side(g1, g2, g3), Side(g4, b5))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9)
four_blocks_systems["9"] = system

# 10 rounds
ts1 = Transition(Side(a2, a3, a4), Side(b1, a1))
ts2 = Transition(Side(a3, a4, b1), Side(b2, a2))
ts3 = Transition(Side(a4, b1, b2), Side(b3, a3))
ts4 = Transition(Side(b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b2, b3, b4), Side(b5, b1))
ts6 = Transition(Side(b3, b4, b5), Side(b6, b2))
ts7 = Transition(Side(b4, b5, b6), Side(g1, b3))
ts8 = Transition(Side(b5, b6, g1), Side(g2, b4))
ts9 = Transition(Side(b6, g1, g2), Side(g3, b5))
ts10 = Transition(Side(g1, g2, g3), Side(g4, b6))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10)
four_blocks_systems["10"] = system

# 11 rounds
ts1 = Transition(Side(a2, a3, a4), Side(b1, a1))
ts2 = Transition(Side(a3, a4, b1), Side(b2, a2))
ts3 = Transition(Side(a4, b1, b2), Side(b3, a3))
ts4 = Transition(Side(b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b2, b3, b4), Side(b5, b1))
ts6 = Transition(Side(b3, b4, b5), Side(b6, b2))
ts7 = Transition(Side(b4, b5, b6), Side(b7, b3))
ts8 = Transition(Side(b5, b6, b7), Side(g1, b4))
ts9 = Transition(Side(b6, b7, g1), Side(g2, b5))
ts10 = Transition(Side(b7, g1, g2), Side(g3, b6))
ts11 = Transition(Side(g1, g2, g3), Side(g4, b7))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10, ts11)
four_blocks_systems["11"] = system

# 12 rounds
ts1 = Transition(Side(a2, a3, a4), Side(b1, a1))
ts2 = Transition(Side(a3, a4, b1), Side(b2, a2))
ts3 = Transition(Side(a4, b1, b2), Side(b3, a3))
ts4 = Transition(Side(b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b2, b3, b4), Side(b5, b1))
ts6 = Transition(Side(b3, b4, b5), Side(b6, b2))
ts7 = Transition(Side(b4, b5, b6), Side(b7, b3))
ts8 = Transition(Side(b5, b6, b7), Side(b8, b4))
ts9 = Transition(Side(b6, b7, b8), Side(g1, b5))
ts10 = Transition(Side(b7, b8, g1), Side(g2, b6))
ts11 = Transition(Side(b8, g1, g2), Side(g3, b7))
ts12 = Transition(Side(g1, g2, g3), Side(g4, b8))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10, ts11, ts12)
four_blocks_systems["12"] = system

# 13 rounds
ts1 = Transition(Side(a2, a3, a4), Side(b1, a1))
ts2 = Transition(Side(a3, a4, b1), Side(b2, a2))
ts3 = Transition(Side(a4, b1, b2), Side(b3, a3))
ts4 = Transition(Side(b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b2, b3, b4), Side(b5, b1))
ts6 = Transition(Side(b3, b4, b5), Side(b6, b2))
ts7 = Transition(Side(b4, b5, b6), Side(b7, b3))
ts8 = Transition(Side(b5, b6, b7), Side(b8, b4))
ts9 = Transition(Side(b6, b7, b8), Side(b9, b5))
ts10 = Transition(Side(b7, b8, b9), Side(g1, b6))
ts11 = Transition(Side(b8, b9, g1), Side(g2, b7))
ts12 = Transition(Side(b9, g1, g2), Side(g3, b8))
ts13 = Transition(Side(g1, g2, g3), Side(g4, b9))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10, ts11, ts12, ts13)
four_blocks_systems["13"] = system


# 5 blocks
five_blocks_systems = {}

# 5rounds
ts1 = Transition(Side(a2, a3, a4, a5), Side(g1, a1))
ts2 = Transition(Side(a3, a4, a5, g1), Side(g2, a2))
ts3 = Transition(Side(a4, a5, g1, g2), Side(g3, a3))
ts4 = Transition(Side(a5, g1, g2, g3), Side(g4, a4))
ts5 = Transition(Side(g1, g2, g3, g4), Side(g5, a5))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5)
five_blocks_systems["5"] = system

# 6 rounds
ts1 = Transition(Side(a2, a3, a4, a5), Side(b1, a1))
ts2 = Transition(Side(a3, a4, a5, b1), Side(g1, a2))
ts3 = Transition(Side(a4, a5, b1, g1), Side(g2, a3))
ts4 = Transition(Side(a5, b1, g1, g2), Side(g3, a4))
ts5 = Transition(Side(b1, g1, g2, g3), Side(g4, a5))
ts6 = Transition(Side(g1, g2, g3, g4), Side(g5, b1))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6)
five_blocks_systems["6"] = system

# 7 rounds
ts1 = Transition(Side(a2, a3, a4, a5), Side(b1, a1))
ts2 = Transition(Side(a3, a4, a5, b1), Side(b2, a2))
ts3 = Transition(Side(a4, a5, b1, b2), Side(g1, a3))
ts4 = Transition(Side(a5, b1, b2, g1), Side(g2, a4))
ts5 = Transition(Side(b1, b2, g1, g2), Side(g3, a5))
ts6 = Transition(Side(b2, g1, g2, g3), Side(g4, b1))
ts7 = Transition(Side(g1, g2, g3, g4), Side(g5, b2))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7)
five_blocks_systems["7"] = system

# 8 rounds
ts1 = Transition(Side(a2, a3, a4, a5), Side(b1, a1))
ts2 = Transition(Side(a3, a4, a5, b1), Side(b2, a2))
ts3 = Transition(Side(a4, a5, b1, b2), Side(b3, a3))
ts4 = Transition(Side(a5, b1, b2, b3), Side(g1, a4))
ts5 = Transition(Side(b1, b2, b3, g1), Side(g2, a5))
ts6 = Transition(Side(b2, b3, g1, g2), Side(g3, b1))
ts7 = Transition(Side(b3, g1, g2, g3), Side(g4, b2))
ts8 = Transition(Side(g1, g2, g3, g4), Side(g5, b3))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8)
five_blocks_systems["8"] = system

# 9 rounds
ts1 = Transition(Side(a2, a3, a4, a5), Side(b1, a1))
ts2 = Transition(Side(a3, a4, a5, b1), Side(b2, a2))
ts3 = Transition(Side(a4, a5, b1, b2), Side(b3, a3))
ts4 = Transition(Side(a5, b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b1, b2, b3, b4), Side(g1, a5))
ts6 = Transition(Side(b2, b3, b4, g1), Side(g2, b1))
ts7 = Transition(Side(b3, b4, g1, g2), Side(g3, b2))
ts8 = Transition(Side(b4, g1, g2, g3), Side(g4, b3))
ts9 = Transition(Side(g1, g2, g3, g4), Side(g5, b4))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9)
five_blocks_systems["9"] = system

# 10 rounds
ts1 = Transition(Side(a2, a3, a4, a5), Side(b1, a1))
ts2 = Transition(Side(a3, a4, a5, b1), Side(b2, a2))
ts3 = Transition(Side(a4, a5, b1, b2), Side(b3, a3))
ts4 = Transition(Side(a5, b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b1, b2, b3, b4), Side(b5, a5))
ts6 = Transition(Side(b2, b3, b4, b5), Side(g1, b1))
ts7 = Transition(Side(b3, b4, b5, g1), Side(g2, b2))
ts8 = Transition(Side(b4, b5, g1, g2), Side(g3, b3))
ts9 = Transition(Side(b5, g1, g2, g3), Side(g4, b4))
ts10 = Transition(Side(g1, g2, g3, g4), Side(g5, b5))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10)
five_blocks_systems["10"] = system

# 11 rounds
ts1 = Transition(Side(a2, a3, a4, a5), Side(b1, a1))
ts2 = Transition(Side(a3, a4, a5, b1), Side(b2, a2))
ts3 = Transition(Side(a4, a5, b1, b2), Side(b3, a3))
ts4 = Transition(Side(a5, b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b1, b2, b3, b4), Side(b5, a5))
ts6 = Transition(Side(b2, b3, b4, b5), Side(b6, b1))
ts7 = Transition(Side(b3, b4, b5, b6), Side(g1, b2))
ts8 = Transition(Side(b4, b5, b6, g1), Side(g2, b3))
ts9 = Transition(Side(b5, b6, g1, g2), Side(g3, b4))
ts10 = Transition(Side(b6, g1, g2, g3), Side(g4, b5))
ts11 = Transition(Side(g1, g2, g3, g4), Side(g5, b6))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10, ts11)
five_blocks_systems["11"] = system

# 12 rounds
ts1 = Transition(Side(a2, a3, a4, a5), Side(b1, a1))
ts2 = Transition(Side(a3, a4, a5, b1), Side(b2, a2))
ts3 = Transition(Side(a4, a5, b1, b2), Side(b3, a3))
ts4 = Transition(Side(a5, b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b1, b2, b3, b4), Side(b5, a5))
ts6 = Transition(Side(b2, b3, b4, b5), Side(b6, b1))
ts7 = Transition(Side(b3, b4, b5, b6), Side(b7, b2))
ts8 = Transition(Side(b4, b5, b6, b7), Side(g1, b3))
ts9 = Transition(Side(b5, b6, b7, g1), Side(g2, b4))
ts10 = Transition(Side(b6, b7, g1, g2), Side(g3, b5))
ts11 = Transition(Side(b7, g1, g2, g3), Side(g4, b6))
ts12 = Transition(Side(g1, g2, g3, g4), Side(g5, b7))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10, ts11, ts12)
five_blocks_systems["12"] = system

# 13 rounds
ts1 = Transition(Side(a2, a3, a4, a5), Side(b1, a1))
ts2 = Transition(Side(a3, a4, a5, b1), Side(b2, a2))
ts3 = Transition(Side(a4, a5, b1, b2), Side(b3, a3))
ts4 = Transition(Side(a5, b1, b2, b3), Side(b4, a4))
ts5 = Transition(Side(b1, b2, b3, b4), Side(b5, a5))
ts6 = Transition(Side(b2, b3, b4, b5), Side(b6, b1))
ts7 = Transition(Side(b3, b4, b5, b6), Side(b7, b2))
ts8 = Transition(Side(b4, b5, b6, b7), Side(b8, b3))
ts9 = Transition(Side(b5, b6, b7, b8), Side(g1, b4))
ts10 = Transition(Side(b6, b7, b8, g1), Side(g2, b5))
ts11 = Transition(Side(b7, b8, g1, g2), Side(g3, b6))
ts12 = Transition(Side(b8, g1, g2, g3), Side(g4, b7))
ts13 = Transition(Side(g1, g2, g3, g4), Side(g5, b8))
system = SystemTransition(ts1, ts2, ts3, ts4, ts5, ts6, ts7, ts8, ts9, ts10, ts11, ts12, ts13)
five_blocks_systems["13"] = system