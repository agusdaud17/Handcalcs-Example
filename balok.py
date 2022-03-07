from math import*
from handcalcs import handcalc
import forallpeople
forallpeople.environment("structural", top_level=True)

@handcalc(jupyter_display=True, override="long")
def balok(M_u=float, b_w=float, h=float, f_y=420*MPa, f_c=21*MPa, D=16*mm, Dv=10*mm, d_s=40*mm):
    M_u # momen ultimit
    h # tinggi balok
    b_w #lebar balok
    f_c # kuat tekan beton
    f_y # kuat leleh baja tulangan
    D # diameter tulangan pokok
    Dv # diameter tulangan sengkang
    d_s # tebal selimut beton
    d = h - (d_s + Dv + D/2)
    phi = 0.9 # asumsi terkendali tarik
    jd = 0.9*d
    A_s = M_u / (phi*f_y*jd)
    a = (A_s*f_y) / (0.85*f_c*b_w)
    As_min1 = (0.25*sqrt(f_c)*MPa)/f_y *b_w*d
    As_min2 = (1.4*MPa)/f_y *b_w*d
    A_s = max(A_s,As_min1,As_min2) # luas tulangan perlu
    As_tul = 0.25*pi*D**2
    n_tul = max( ceil(A_s / As_tul), 2) # jumlah tulangan perlu
    spasi = (b_w - (2*(d_s+Dv) + (n_tul*D)) ) / (n_tul - 1)
    if spasi >= 25*mm: kontrol = "spasi memenuhi"
    elif spasi < 25*mm: kontrol = "tidak memenuhi"
    A_s = n_tul*As_tul
    a = (A_s*f_y) / (0.85*f_c*b_w)
    if 17*MPa <= f_c <= 28*MPa: beta_1 = 0.85
    elif 28*MPa <= f_c < 55*MPa: beta_1 = 0.85 - (0.05*(f_c-28) / 7)
    elif f_c >= 55*MPa: beta_1 = 0.65 
    c = a/beta_1
    epsilon_t = ((d-c)/c) * 0.003
    epsilon_ty = 0.002
    if epsilon_t <= epsilon_ty : phi=0.65
    elif epsilon_ty <= epsilon_t < 0.005: phi = 0.65 + 0.25*((et - ety)/(0.005-ety))
    elif epsilon_t >= 0.005: phi = 0.9
    M_n = A_s*f_y*(d - a/2)
    phi_Mn = phi*M_n # Momen nominal terfaktor
    if phi_Mn > M_u : kontrol="memenuhi"
    else: kontrol = "tidak memenuhi"