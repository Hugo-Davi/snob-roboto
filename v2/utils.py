import bs4

def isTag(prioriTag, key):
    if not isinstance(prioriTag, bs4.element.Tag):
        print(f'{key} erro não é tag')
        return False
    return True