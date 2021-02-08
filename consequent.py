from sympy import symbols, RR, poly

class Consequent():
    def __init__(self):
        return
    
    def trapesium(self, a, b, c, d, universe):
        '''
        input:
            a, b, c, d = int interval membership trapesium
            universe = (intStart, intEnd)
        return:
            [poly], [(interval_start, interval_end]
        '''
        z = symbols('z')
        poly_member = []
        poly_interval = []

        #Interval pertama
        if a > universe[0]:
            poly_member.append(poly(0, z, domain=RR))
            poly_interval.append((universe[0], a))

        #Interval kedua
        if b - a != 0:
            poly_member.append(poly((z-a)/(b-a), z, domain=RR))
            poly_interval.append((a, b))

        #Interval ketiga
        poly_member.append(poly(1., z, domain=RR))
        poly_interval.append((b, c))

        #Interval keempat
        if d - c != 0:
            poly_member.append(poly((d-z)/(d-c), z, domain=RR))
            poly_interval.append((c, d))

        #Interval kelima  
        if d < universe[1]:
            poly_member.append(poly(0, z, domain=RR))
            poly_interval.append((d, universe[1]))


        return poly_member, poly_interval