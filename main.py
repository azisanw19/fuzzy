from antecedent import Antecedent
from consequent import Consequent
from tnorm import TNorm
from implikasi import Implikasi
from inference import InferenceEngine
from deffuzifier import Deffuzifier

def fuzzy():

    # membership function
    antecedent = Antecedent()
    consequent = Consequent()

    universe_suhu = (20, 38)
    member_suhu_dingin = antecedent.trapesium(20, 20, 23, 26, universe_suhu)
    member_suhu_sejuk = antecedent.trapesium(23, 26, 29, 32, universe_suhu)
    member_suhu_panas = antecedent.trapesium(29, 32, 38, 38, universe_suhu)

    universe_angin = (0, 6)
    member_angin_lambat = antecedent.trapesium(0, 0, 1, 4, universe_angin)
    member_angin_kencang = antecedent.trapesium(1, 4, 6, 6, universe_angin)

    universe_jemuran = (30, 540)
    member_jemuran_cepat = consequent.trapesium(30, 30, 120, 240, universe_jemuran)
    member_jemuran_sedang = consequent.trapesium(120, 240, 360, 480, universe_jemuran)
    member_jemuran_lama = consequent.trapesium(360, 480, 540, 540, universe_jemuran)
    
    # input
    suhu = float(input("Suhu in celcius [20, 38]: "))
    angin = float(input("Kecepatan angin in m/s [0, 6]: "))

    # get input score
    score_suhu_dingin = antecedent.get_score(member_suhu_dingin, suhu)
    score_suhu_sejuk = antecedent.get_score(member_suhu_sejuk, suhu)
    score_suhu_panas = antecedent.get_score(member_suhu_panas, suhu)

    score_angin_lambat = antecedent.get_score(member_angin_lambat, angin)
    score_angin_kencang = antecedent.get_score(member_angin_kencang, angin)
    
    # t-norm
    t_norm = TNorm()
    
    t_norm_r1 = t_norm.minimum(score_suhu_dingin, score_angin_lambat)
    t_norm_r2 = t_norm.minimum(score_suhu_dingin, score_angin_kencang)
    t_norm_r3 = t_norm.minimum(score_suhu_sejuk, score_angin_lambat)
    t_norm_r4 = t_norm.minimum(score_suhu_sejuk, score_angin_kencang)
    t_norm_r5 = t_norm.minimum(score_suhu_panas, score_angin_lambat)
    t_norm_r6 = t_norm.minimum(score_suhu_panas, score_angin_kencang)
    
    # Implikasi
    implikasi = Implikasi()

    implikasi_r1 = implikasi.mamdani_min(t_norm_r1, member_jemuran_lama)
    implikasi_r2 = implikasi.mamdani_min(t_norm_r2, member_jemuran_lama)
    implikasi_r3 = implikasi.mamdani_min(t_norm_r3, member_jemuran_lama)
    implikasi_r4 = implikasi.mamdani_min(t_norm_r4, member_jemuran_sedang)
    implikasi_r5 = implikasi.mamdani_min(t_norm_r5, member_jemuran_sedang)
    implikasi_r6 = implikasi.mamdani_min(t_norm_r6, member_jemuran_cepat)
    
    # Supremum
    inferenceEngine = InferenceEngine()

    poli = []
    poli.append(implikasi_r1[0])
    poli.append(implikasi_r2[0])
    poli.append(implikasi_r3[0])
    poli.append(implikasi_r4[0])
    poli.append(implikasi_r5[0])
    poli.append(implikasi_r6[0])

    inte_poli = [implikasi_r1[1],
                implikasi_r2[1],
                implikasi_r3[1],
                implikasi_r4[1],
                implikasi_r5[1],
                implikasi_r6[1]]

    
    polinomial, inter_supre = inferenceEngine.supremum(poli, inte_poli, universe_jemuran)
    
    # polinomial defuzzifier & interval defuzzifier
    # print(polinomial)
    # print(inter_supre)

    # Centroid
    deffuzifier = Deffuzifier()

    hasil = deffuzifier.centroid(polinomial, inter_supre)
    print(int(hasil), "menit")

if __name__ == "__main__":
    fuzzy()