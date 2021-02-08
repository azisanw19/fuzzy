from sympy import symbols, RR, poly

class Deffuzifier():
    def __init__(self):
        return

    def centroid(self, members, intervals):
        '''
        input: 
            members = list[Poly] -> variable z
            intervals = list[(awal, akhir)]

        return float
        '''
        z = symbols("z")

        # initial numerator and denominator (area)
        numerator = 0
        denominator = 0
        for member, interval_m in zip(members, intervals):
            # integral numerator
            num = member.mul(poly(z, domain=RR)).integrate()
            # add numerator
            numerator += num(interval_m[1]) - num(interval_m[0])
            # integral area dnominator
            den = member.integrate()
            # add denominator / area
            denominator += den(interval_m[1]) - den(interval_m[0])

        return numerator/denominator