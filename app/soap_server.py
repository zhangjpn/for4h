#-*- coding:utf-8 -*-

# from ladon.ladonizer import ladonize
# from ladon.types.ladontype import LadonType
#
#
# class Calculator(object):
#
#     class Table(LadonType):
#         slno = int
#         colTitle = str
#         colSize = int
#         colAlign = str
#
#     @ladonize([Table], rtype=int)  # notice the [], around table that means the input will be a list of Table LadonTypes.
#     def setTables(self, tables):
#
#         return len(tables)

from ladon.ladonizer import ladonize

class Calculator(object):

    @ladonize(int, int, rtype=int)
    def add(self, a, b):
        return a + b

