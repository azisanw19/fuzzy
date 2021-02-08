from sympy import symbols, RR, poly

class InferenceEngine():
    def __init__(self):
        return

    def intersection(self, poly1, poly2):
        '''
        input:
            poly1 = poly
            poly2 = poly
        return:
            float
        '''
        inters = poly1 - poly2
        y = inters.root(0)
        return y

    def findMax(self, poly_subject, poly_target, interval_f):
        '''
        input:
            poly_subject = poly
            poly_target = poly
            interval_f = (start, end)

        output: 
            poly = list[poly]
            interval_f = list[(start, end)]
        '''
        polyD = poly_subject.degree()
        targetD = poly_target.degree()
        if poly_target(interval_f[0]) == 0 and poly_target(interval_f[1]) == 0:
            # poly_target = 0
            return [poly_subject], [interval_f]
        if polyD == 0 and targetD == 0:
            # poly_subject = horizontal line & poly_target = horizontal line
            subject = poly_subject(interval_f[1])
            target = poly_target(interval_f[1])
            if target > subject:
                # poly_target above
                return [poly_target], [interval_f]
            else:
                # poly_subject above
                return [poly_subject], [interval_f]
        elif polyD == 1:
            # y = mx + c. m != 0
            # gradient poly_subject != 0
            if targetD == 1:
                # y = mx + c. m != 0
                # gradient poly_target != 0
                subject_start = poly_subject(interval_f[0])
                target_start = poly_target(interval_f[0])
                subject_end = poly_subject(interval_f[1])
                target_end = poly_target(interval_f[1])
                if subject_start <= target_start:
                    # poly_subject bottom in start
                    if subject_end <= target_end:
                        # poly_subject bottom in end
                        # not intersect, poly_target above
                        return [poly_target], [interval_f]
                    else:
                        # poly_subject above in end
                        # intersect with poly_target first
                        inter = self.intersection(poly_subject, poly_target)
                        poly_res = [poly_target, poly_subject]
                        intervals_res = [(interval_f[0], inter), (inter, interval_f[1])]
                        return poly_res, intervals_res
                elif subject_start > target_start:
                    # poly_subject above in start
                    if subject_end < target_end:
                        # poly_subject bottom in end
                        # intersect with poly_subject first
                        inter = self.intersection(poly_subject, poly_target)
                        poly_res = [poly_subject, poly_target]
                        intervals_res = [(interval_f[0], inter), (inter, interval_f[1])]
                        return poly_res, intervals_res
                    else:
                        # poly_subject above in end
                        # no intersect
                        return [poly_subject], [interval_f]
            elif targetD == 0:
                # gradient poly_target == 0
                # horizontal line
                if poly_subject(interval_f[0]) > poly_target(interval_f[0]):
                    # poly_subject above in start
                    if poly_subject(interval_f[1]) < poly_target(interval_f[1]):
                        # poly_subject bottom in end'
                        # intersect with poly_subject first
                        inter = self.intersection(poly_subject, poly_target)
                        poly_res = [poly_subject, poly_target]
                        interval_res = [(interval_f[0], inter), (inter, interval_f[1])]
                        return poly_res, interval_res
                    else:
                        # poly_subject above in end
                        # no intersect
                        return [poly_subject], [interval_f]
                elif poly_subject(interval_f[0]) <= poly_target(interval_f[0]):
                    # poly_subject bottom in start
                    if poly_subject(interval_f[1]) > poly_target(interval_f[1]):
                        # poly_subject above in end
                        # intersect with poly_target first
                        inter = self.intersection(poly_subject, poly_target)
                        poly_res = [poly_target, poly_subject]
                        interval_res = [(interval_f[0], inter), (inter, interval_f[1])]
                        return poly_res, interval_res
                    else:
                        # poly_subject bottom in end
                        return [poly_target], [interval_f]
        elif polyD == 0 and targetD == 1:
            # poly_subject gradient = 0 / horizontal line
            # poly_ target gredient != 0
            if poly_target(interval_f[0]) < poly_subject(interval_f[0]):
                # poly_target bottom in start
                if poly_target(interval_f[1]) > poly_subject(interval_f[1]):
                    # poly_target above in end
                    # intersect with poly_subject first
                    inter = self.intersection(poly_subject, poly_target)
                    poly_res = [poly_subject, poly_target]
                    interval_res = [(interval_f[0], inter), (inter, interval_f[1])]
                    return poly_res, interval_res
                else:
                    # poly_target bottom in end
                    return [poly_subject], [interval_f]
            else:
                # poly_target above in start
                if poly_target(interval_f[1]) < poly_subject(interval_f[1]):
                    # poly_target bottom in end
                    # intersect with poly_target first
                    inter = self.intersection(poly_subject, poly_target)
                    poly_res = [poly_target, poly_subject]
                    interval_res = [(interval_f[0], inter), (inter, interval_f[1])]
                    return poly_res, interval_res
                else:
                    # poly_target above in end
                    return [poly_target], [interval_f]
    
    def supremum(self, members, intervals, sistem_interval):
        '''
        input: 
            members = list[[poly]]
            intervals = list[[(start, end)]]
            sistem_inter
        return 
            members as list[poly -> variable z]
            intervals as list[(start, end)]
        '''
        z = symbols("z")
        # initial supremum
        members_supremum = [poly(0.0000000000000000000000000001, z, domain=RR)]
        intervals_supremum = [sistem_interval]
        for member_role, interval_role in zip(members, intervals):
            for member, interval_m in zip(member_role, interval_role):
                for index_supremum in range(len(members_supremum)):
                    member_supremum = members_supremum[index_supremum]
                    interval_supremum = intervals_supremum[index_supremum]
                    if interval_supremum[0] == interval_m[0]:
                        # interval supremum start == interval member start
                        ''' 
                        analogi
                        ---------------------- supremum
                        -------     member => K1
                        --------    supremum
                        --------    member => K2
                        ----- supremum
                        -------------- member => K3
                        K2 identik K3
                        '''
                        # K1
                        if interval_supremum[1] > interval_m[1]:
                            # interval_supremum more than interval member
                            supremum_temp = member_supremum
                            interval_temp = (interval_supremum[0], interval_m[1])
                            poly_list, interval_list = self.findMax(supremum_temp, member, interval_temp)
                            if len(poly_list) == 1:
                                # poly_list max no intersect
                                if poly_list[0](interval_supremum[0]) == supremum_temp(interval_supremum[0]):
                                    # no update poly_supremum
                                    continue
                                else:
                                    # update poly_supremum
                                    index_hasil = len(poly_list)-1
                                    while index_hasil >= 0:
                                        poly_hasil = poly_list[index_hasil]
                                        interval_hasil = interval_list[index_hasil]
                                        
                                        # insert update supremum
                                        members_supremum.insert(index_supremum, poly_hasil)
                                        intervals_supremum.insert(index_supremum, interval_hasil)

                                        # update interval supremum
                                        list_tuple = list(intervals_supremum[index_supremum+1])
                                        list_tuple[0]  = interval_hasil[1]
                                        intervals_supremum[index_supremum+1] = tuple(list_tuple)
                                        index_hasil -= 1
                            else:
                                # poly_list max with intersect
                                index_hasil = len(poly_list)-1
                                while index_hasil >= 0:
                                    poly_hasil = poly_list[index_hasil]
                                    interval_hasil = interval_list[index_hasil]

                                    # insert update supremum
                                    members_supremum.insert(index_supremum, poly_hasil)
                                    intervals_supremum.insert(index_supremum, interval_hasil)

                                    # update interval supremum
                                    list_tuple = list(intervals_supremum[index_supremum+1])
                                    list_tuple[0]  = interval_hasil[1]
                                    intervals_supremum[index_supremum+1] = tuple(list_tuple)
                                    index_hasil -= 1
                        # K2 K3
                        elif interval_supremum[1] <= interval_m[1]:
                            # poly_supremum less than member
                            supremum_temp = member_supremum
                            interval_temp = (interval_supremum[0], interval_supremum[1])
                            poly_list, interval_list = self.findMax(supremum_temp, member, interval_temp)
                            if len(poly_list) == 1:
                                # poly_list max no intersect
                                if poly_list[0](interval_supremum[0]) == supremum_temp(interval_supremum[0]):
                                    # no update poly_supremum
                                    continue
                                else:
                                    # update poly_supremum
                                    index_hasil = len(poly_list)-1
                                    while index_hasil >= 0:
                                        poly_hasil = poly_list[index_hasil]
                                        interval_hasil = interval_list[index_hasil]
                    
                                        # insert update supremum
                                        members_supremum.insert(index_supremum, poly_hasil)
                                        intervals_supremum.insert(index_supremum, interval_hasil)
                                        
                                        # update interval supremum
                                        del members_supremum[index_supremum+1]
                                        del intervals_supremum[index_supremum+1]
                                        index_hasil -= 1
                            else:
                                # poly_list max with intersect
                                index_hasil = len(poly_list)-1
                                while index_hasil >= 0:
                                    poly_hasil = poly_list[index_hasil]
                                    interval_hasil = interval_list[index_hasil]

                                    # insert update supremum
                                    members_supremum.insert(index_supremum, poly_hasil)
                                    intervals_supremum.insert(index_supremum, interval_hasil)
                                    index_hasil -= 1
                                
                                # update supremum
                                del members_supremum[index_supremum+2]
                                del intervals_supremum[index_supremum+2]
                    elif interval_supremum[0] < interval_m[0]:
                        # supremum less than member in start
                        '''
                        analogi kemungkinan
                        -------------       supremum
                            -----           member => K1
                        -------------       supremum
                            -------------   member
                        -------------       supremum
                                        --- member => K3
                        '''
                        # K3
                        if interval_supremum[1] <= interval_m[0]:
                            # no update supremum
                            continue
                        # K1
                        elif interval_supremum[1] > interval_m[1]:
                            # supremum more than member in end
                            supremum_temp = member_supremum
                            interval_temp = (interval_m[0], interval_m[1])
                            poly_list, interval_list = self.findMax(supremum_temp, member, interval_temp)
                            if len(poly_list) == 1:
                                # poly_list max no intersect
                                if poly_list[0](interval_supremum[0]) == supremum_temp(interval_supremum[0]):
                                    # no update poly_supremum
                                    continue
                                else:
                                    # update poly_supremum
                                    index_hasil = len(poly_list)-1
                                    while index_hasil >= 0:
                                        poly_hasil = poly_list[index_hasil]
                                        interval_hasil = interval_list[index_hasil]
                                        
                                        # insert update supremum
                                        members_supremum.insert(index_supremum, poly_hasil)
                                        intervals_supremum.insert(index_supremum, interval_hasil)

                                        # update interval supremum
                                        list_tuple = list(intervals_supremum[index_supremum+1])
                                        awal = list_tuple[0]
                                        list_tuple[0]  = interval_hasil[1]
                                        intervals_supremum[index_supremum+1] = tuple(list_tuple)
                                        members_supremum.insert(index_supremum, members_supremum[index_supremum+1])
                                        intervals_supremum.insert(index_supremum, (awal, interval_hasil[0]))
                                        index_hasil -= 1
                            else:
                                # poly_list max with intersect
                                index_hasil = len(poly_list)-1
                                while index_hasil >= 0:
                                    poly_hasil = poly_list[index_hasil]
                                    interval_hasil = interval_list[index_hasil]
                                    
                                    # insert update supremum
                                    members_supremum.insert(index_supremum, poly_hasil)
                                    intervals_supremum.insert(index_supremum, interval_hasil)

                                    # update interval supremum
                                    list_tuple = list(intervals_supremum[index_supremum+1])
                                    awal = list_tuple[0]
                                    list_tuple[0]  = interval_hasil[1]
                                    intervals_supremum[index_supremum+1] = tuple(list_tuple)
                                    if index_hasil == 0:
                                        # update supremum first in
                                        members_supremum.insert(index_supremum, members_supremum[index_supremum+1])
                                        intervals_supremum.insert(index_supremum, (awal, interval_hasil[0]))
                                    index_hasil -= 1
                        # K2
                        elif interval_supremum[1] <= interval_m[1]:
                            # interval_supremum less than interval member
                            supremum_temp = member_supremum
                            interval_temp = (interval_m[0], interval_supremum[1])
                            poly_list, interval_list = self.findMax(supremum_temp, member, interval_temp)
                            if len(poly_list) == 1:
                                # poly_list max no intersect
                                if poly_list[0](interval_supremum[0]) == supremum_temp(interval_supremum[0]):
                                    # no update poly_supremum
                                    continue
                                else:
                                    # update poly_supremum
                                    index_hasil = len(poly_list)-1
                                    while index_hasil >= 0:
                                        poly_hasil = poly_list[index_hasil]
                                        interval_hasil = interval_list[index_hasil]

                                        # insert update supremum
                                        members_supremum.insert(index_supremum+1, poly_hasil)
                                        intervals_supremum.insert(index_supremum+1, interval_hasil)

                                        # update interval supremum
                                        list_tuple = list(intervals_supremum[index_supremum])
                                        list_tuple[1]  = interval_hasil[0]
                                        intervals_supremum[index_supremum] = tuple(list_tuple)
                                        index_hasil -= 1
                            else:
                                # poly_list max with intersect
                                index_hasil = len(poly_list)-1
                                while index_hasil >= 0:
                                    poly_hasil = poly_list[index_hasil]
                                    interval_hasil = interval_list[index_hasil]

                                    # insert update supremum
                                    members_supremum.insert(index_supremum+1, poly_hasil)
                                    intervals_supremum.insert(index_supremum+1, interval_hasil)

                                    if index_hasil == 0:
                                        # update supremum first in
                                        list_tuple = list(intervals_supremum[index_supremum])
                                        list_tuple[1]  = interval_hasil[0]
                                        intervals_supremum[index_supremum] = tuple(list_tuple)
                                    index_hasil -= 1
                    
                    elif interval_supremum[0] > interval_m[0]:
                        # interval_supremum more than interval member in start
                        '''
                        analogi
                            --------------  supremum
                        ------------        member => K1
                            --------------  supremum
                        --                  member => K2
                            --------------  supremum
                        ------------------- member => K3
                        '''
                        # K2
                        if interval_m[1] <= interval_supremum[0]:
                            # no update supremum
                            continue
                        # K1
                        elif interval_supremum[1] > interval_m[1]:
                            # supremum more than member in end
                            supremum_temp = member_supremum
                            interval_temp = (interval_supremum[0], interval_m[1])
                            poly_list, interval_list = self.findMax(supremum_temp, member, interval_temp)
                            if len(poly_list) == 1:
                                # poly_list no intersect
                                if poly_list[0](interval_supremum[0]) == supremum_temp(interval_supremum[0]):
                                    # no update poly_supremum
                                    continue
                                else:
                                    index_hasil = len(poly_list)-1
                                    while index_hasil >= 0:
                                        poly_hasil = poly_list[index_hasil]
                                        interval_hasil = interval_list[index_hasil]

                                        # insert update supremum
                                        members_supremum.insert(index_supremum, poly_hasil)
                                        intervals_supremum.insert(index_supremum, interval_hasil)
                                        
                                        # update interval supremum
                                        list_tuple = list(intervals_supremum[index_supremum+1])
                                        list_tuple[0]  = interval_hasil[1]
                                        intervals_supremum[index_supremum+1] = tuple(list_tuple)
                                        index_hasil -= 1
                            else:
                                # poly_list max with intersect
                                index_hasil = len(poly_list)-1
                                while index_hasil >= 0:
                                    poly_hasil = poly_list[index_hasil]
                                    interval_hasil = interval_list[index_hasil]

                                    # insert update supremum
                                    members_supremum.insert(index_supremum, poly_hasil)
                                    intervals_supremum.insert(index_supremum, interval_hasil)

                                    if index_hasil == 1:
                                        # update supremum last in
                                        list_tuple = list(intervals_supremum[index_supremum+1])
                                        list_tuple[0]  = interval_hasil[1]
                                        intervals_supremum[index_supremum+1] = tuple(list_tuple)
                                    index_hasil -= 1
                        # K3
                        elif interval_supremum[1] <= interval_m[1]:
                            # interval supremum less than member
                            supremum_temp = member_supremum
                            interval_temp = (interval_supremum[0], interval_supremum[1])
                            poly_list, interval_list = self.findMax(supremum_temp, member, interval_temp)
                            if len(poly_list) == 1:
                                # poly_list no intersect
                                if poly_list[0](interval_supremum[0]) == supremum_temp(interval_supremum[0]):
                                    # no update supremum
                                    continue
                                else:
                                    # update poly_supremum
                                    index_hasil = len(poly_list)-1
                                    while index_hasil >= 0:
                                        poly_hasil = poly_list[index_hasil]
                                        interval_hasil = interval_list[index_hasil]

                                        # insert update supremum
                                        members_supremum.insert(index_supremum, poly_hasil)
                                        intervals_supremum.insert(index_supremum, interval_hasil)
                                        index_hasil -= 1

                                    # update supremum
                                    del members_supremum[index_supremum+1]
                                    del intervals_supremum[index_supremum+1]
                            else:
                                # poly_list max with intersect
                                index_hasil = len(poly_list)-1
                                while index_hasil >= 0:
                                    poly_hasil = poly_list[index_hasil]
                                    interval_hasil = interval_list[index_hasil]

                                    # insert update supremum
                                    members_supremum.insert(index_supremum, poly_hasil)
                                    intervals_supremum.insert(index_supremum, interval_hasil)
                                    index_hasil -= 1
                                
                                # update supremum
                                del members_supremum[index_supremum+2]
                                del intervals_supremum[index_supremum+2]
        
        # delete with interval start == interval end
        length = len(members_supremum)
        index_del = 0
        while index_del < length:
            member = members_supremum[index_del]
            interval_y = intervals_supremum[index_del]
            index_del2 = 0
            while index_del2 < length:
                interval2 = intervals_supremum[index_del2]
                if index_del == index_del2:
                    index_del2 += 1
                elif interval2[0] == interval_y[0] and interval2[1] == interval_y[1]:
                    del members_supremum[index_del2]
                    del intervals_supremum[index_del2]
                    length -= 1
                else:
                    index_del2 += 1
            if interval_y[0] >= interval_y[1]:
                del members_supremum[index_del]
                del intervals_supremum[index_del]
                length -= 1
            elif member(interval_y[0]) < 0.000000000000000000000000001:
                del members_supremum[index_del]
                del intervals_supremum[index_del]
                length -= 1
            else:
                index_del += 1
            
            
        return members_supremum, intervals_supremum