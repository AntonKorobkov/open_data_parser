# coding=utf-8


def test_kw(**kwargs):

    test = list(kwargs.keys())[0]

    print(test)
    print(kwargs[test])

test_kw(spam='eggs', foo='bar')
