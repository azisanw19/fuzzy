from sympy import symbols, RR, poly

class Antecedent():

    def __init__(self):
        return


    def trapesium(self, a, b, c, d, universe):
        '''input:
            a, b, c, d = int interval membership trapesium
            universe = (intStart, intEnd)
        return:
            [poly], [(interval_start, interval_end)]'''
        x = symbols('x')
        poly_member = []
        poly_interval = []

        #Untuk rentang yang pertama
        if a > universe[0]:
            poly_member.append(poly(0, x, domain=RR))
            poly_interval.append((universe[0], a))
        
        #Untuk rentang yang kedua
        if b - a != 0:
            poly_member.append(poly((x-a)/(b-a), x, domain=RR))
            poly_interval.append((a, b))

        #Untuk rentang yang ketiga
        poly_member.append(poly(1., x, domain=RR))
        poly_interval.append((b, c))


        #Untuk rentang yang keempat
        if d - c != 0:
            poly_member.append(poly((d-x)/(d-c), x, domain=RR))
            poly_interval.append((c, d))

        #Untuk rentang yang kelima
        if d < universe[1]:
            poly_member.append(poly(0, x, domain=RR))
            poly_interval.append((d, universe[1]))

        return poly_member, poly_interval

    def get_score(self, membership, target):
        '''
        input:
            membership = ([polynomial], [(intervalStart, end)])
            target = float
        return
            float
        '''
        member_score = membership[0]
        interval_score = membership[1]
        for poly_member, poly_interval in zip(member_score, interval_score):
            if poly_interval[0] <= target <= poly_interval[1]:
                return poly_member(target)