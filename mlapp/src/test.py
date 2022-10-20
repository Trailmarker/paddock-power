# -*- coding: utf-8 -*-
from functools import partialmethod

def decorate(text):
    def wrapper(method):
        def func(*args, **kwargs):
            print(f"{text}!")
            return method(*args, **kwargs)
        return func
    return wrapper

def decorate2(text):
    def wrapper(method):
        def func(*args, **kwargs):
            print(f"{text}!")
            return partialmethod(method)
        return func
    return wrapper


class Test:

    @decorate("Bar")
    def foo(self):
        print("Foo!")

    def baz(self):
        print("Baz!")

    baz = decorate("Qux")(baz)

    @decorate2("Bam")
    def boom(self):
        print("Boom!")