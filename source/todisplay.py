#the medium
from extratraits import ExtraTraits

def round_list(xs):
    return [round(item) for item in xs]

def sig(n, form=None):

    if isinstance(n, str):
        return n

    if isinstance(n, int):
        if form:
            fn = str(n)
            while n < 10 ** (form-1):
                n *= 10
                fn = str(0) + fn
            return fn
        return str(n)

    if isinstance(n, (float)):
        if n < 1:
            n = round(n*100)/100
        elif n < 1000:
            n = round(n*10)/10
        elif n < 10000:
            n = str(round(n/10)/100) + 'k'
        else:
            n = str((round(n/100))/10) + 'k'
        return str(n)
    
    if isinstance(n, ExtraTraits):
        if not n:
            return "{}"
        else:
            return str(n)
    
    if isinstance(n, type(None)):
        return "N/A"
    
    return "type_error : " + str(type(n))

def sig_list(xs):   #not used?
    return [sig(item) for item in xs]

def to_display(data, form=None):
    if data == "flood":
        return "/" * (88 + 128)
    elif isinstance(data, list) or isinstance(data, tuple):
        return "[" + "|".join([to_display(datum) for datum in data]) + "], "
    else:
        return sig(data, form)
    
def display(data):
    print(to_display(data))

def flood():
    display("flood")