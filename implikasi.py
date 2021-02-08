from sympy import symbols, RR, poly

class Implikasi():
    def __init__(self):
        return

    def find_interval_intersection(self, poly_target, target):
        '''
        input:
            poly_target = poly
            target = float
        return:
            float
        '''
        z = symbols('z')
        inters = poly_target - poly(target, z, domain=RR)
        y = inters.root(0)
        return y
        
    def mamdani_min(self, antecedent, consequent):
        '''
        input:
            antecedent = float
            consequent = ([poly], [(interval_start, interval_end)])
        return:
            [poly], [(intervalStart, end)]
        '''
        z = symbols('z')
        if antecedent == 0.0:
            return [poly(0.0, z, domain=RR)], [(consequent[1][0][0], consequent[1][-1][1])]
        member_c = consequent[0]
        interval_c = consequent[1]
        mamdani_poly = []
        mamdani_interval = []
        for index in range(len(member_c)):
            member_i = member_c[index]
            interval_i = interval_c[index]
            if member_i(interval_i[0]) == 0 and member_i(interval_i[1]) == 0:
                continue
            elif member_i.degree() == 0:
                mamdani_poly.append(poly(antecedent, z, domain=RR))
                mamdani_interval.append((interval_i[0], interval_i[1]))
            else:
                if member_i.LC() > 0:
                    mamdani_poly.append(member_i)

                    interval_end = self.find_interval_intersection(member_i, antecedent)
                    mamdani_interval.append((interval_i[0], interval_end))

                    # update interval next
                    mamdani_poly.append(poly(antecedent, z, domain=RR))
                    mamdani_interval.append((interval_end, interval_i[1]))
                else:
                    mamdani_poly.append(poly(antecedent, z, domain=RR))

                    interval_end = self.find_interval_intersection(member_i, antecedent)

                    mamdani_interval.append((interval_i[0], interval_end))

                    mamdani_poly.append(member_i)
                    mamdani_interval.append((interval_end, interval_i[1]))

        return mamdani_poly, mamdani_interval