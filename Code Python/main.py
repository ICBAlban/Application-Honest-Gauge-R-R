import tkinter as tk
from tkinter.font import Font
from tkinter.messagebox import showerror
from tkinter import ttk
from random import gauss
import numpy as np

def d2_d3_d2b(n_ite, n):
    A = np.random.normal(0, 1, (n_ite, n))
    r= np.zeros((n_ite))
    for i in range(n_ite):
        r[i] = (max(A[i,:])-min(A[i,:]))
    d2 = np.mean(r)
    d3 = np.std(r)
    return (d2, d3)

class app:
    def __init__(self):
        # Variables
        self._frame = None
        self._L_donnee = []
        
        self._fn = tk.Tk()
        self._police =  Font(family = "Time", size = 9)
        self._police_g =  Font(family = "Time", size = 13)
        self._fn.title('Gauge R&R')
        for i in range(3):
            self._fn.rowconfigure(i, weight=1)
            self._fn.columnconfigure(i, weight=1)

        self._var_nb_it = tk.IntVar(self._fn, value = 10_000_000)
        self._var_USL = tk.DoubleVar(self._fn, value = 1)
        self._var_LSL = tk.DoubleVar(self._fn, value = 0)

        self._s = ttk.Style()
        self._s.theme_use('winnative')

        self._parametre()
        self._affichage_variable()
        self._fn.mainloop()

    def _parametre(self):
        self._var_op = tk.IntVar(self._fn, value =3)
        self._var_piec = tk.IntVar(self._fn, value =10)
        self._var_app = tk.IntVar(self._fn, value =3)
        
        cdr = ttk.Frame(self._fn)
        cdr.grid(row=0, column = 0)
        lb = ttk.Label(cdr, text = "Number of operators: ")
        lb.grid(row=0, column=0 )
        sp = ttk.Spinbox(cdr, from_=1, to=99, width=2,
                         textvariable = self._var_op)
        sp.grid(row=0, column=1)

        cdr = ttk.Frame(self._fn)
        cdr.grid(row=0, column = 1)
        lb = ttk.Label(cdr, text = "Number of measures per piece: ")
        lb.grid(row=0, column=0 ) 
        sp = ttk.Spinbox(cdr, from_=1, to=99, width=2,
                         textvariable = self._var_piec)
        sp.grid(row=0, column=1)

        cdr = ttk.Frame(self._fn)
        cdr.grid(row=0, column = 2)
        lb = ttk.Label(cdr, text = "Number of pieces: ")
        lb.grid(row=0, column=0 ) 
        sp = ttk.Spinbox(cdr, from_=1, to=99, width=2,
                         textvariable = self._var_app)
        sp.grid(row=0, column=1)

        bout = ttk.Button(self._fn, text="Validate",
                          command=self._affichage_variable)
        bout.grid(row=0, column=3)

    def _affichage_variable(self):
        if self._frame != None:
            self._frame.destroy()
        self._frame = ttk.Frame(self._fn)
        self._frame.grid(row=1, column =0, columnspan=4)

        if int(self._var_op.get()) < 1 :
            self._var_op.set(1)
        elif int(self._var_op.get()) > 99 :
            self._var_op.set(99)

        if int(self._var_piec.get()) < 1 :
            self._var_piec.set(1)
        elif int(self._var_piec.get()) > 99 :
            self._var_piec.set(99)

        if int(self._var_app.get()) < 1 :
            self._var_app.set(1)
        elif int(self._var_app.get()) > 99 :
            self._var_app.set(99)

        label = tk.LabelFrame(self._frame, text = "N°", font=self._police_g)
        label.grid(row=0, column=0, sticky="NEWS")

        for j in range(int(self._var_piec.get())):
            lab = ttk.Label(label, text = str(j+1), font=self._police_g)
            lab.grid(row=j, column=0)

        self._L_donnee = []       
        for i in range(int(self._var_op.get())):
            label = tk.LabelFrame(self._frame, text="Operator: "+str(i+1), font=self._police_g)
            label.grid(row=0, column=i+1)
            L_case = []
            for j in range(int(self._var_piec.get())):
                L = []
                label.rowconfigure(j, weight=1)
                for k in range(int(self._var_app.get())):                   
                    label.columnconfigure(k, weight=1)
                    
                    var = tk.DoubleVar(self._fn, value=0.0)
                    lab = ttk.Entry(label, width=10, font=self._police,
                         textvariable = var)
                    lab.grid(row=j, column=k)

                    L.append(var)
                L_case.append(L)
            self._L_donnee.append(L_case)
        
        label = ttk.Frame(self._fn)
        label.grid(row=2, column=0)

        lab = ttk.Label(label, text="Iteration")
        lab.grid(row=0, column=0)

        lab = ttk.Entry(label, width=12,
                         textvariable = self._var_nb_it)
        lab.grid(row=0, column=1)

        lab = ttk.Label(label, text="USL")
        lab.grid(row=0, column=2)

        lab = ttk.Entry(label, width=12,
                         textvariable = self._var_USL)
        lab.grid(row=0, column=3)

        lab = ttk.Label(label, text="LSL")
        lab.grid(row=0, column=4)

        lab = ttk.Entry(label, width=12,
                         textvariable = self._var_LSL)
        lab.grid(row=0, column=5)

        bout = ttk.Button(self._fn, text="Calculation", command=self.calcul_RR)
        bout.grid(row=2, column =1, columnspan=4)

    def calcul_RR(self):
        o = len(self._L_donnee)
        if o > 0:
            n = len(self._L_donnee[0])
            if n > 0 :
                p = len(self._L_donnee[0][0])
                if p > 0 :
                    L_o_r = []
                    L_o_R = []
                    L_o_p = []
                    for i in range(o):
                        L_p_r = []
                        L_p_R = []
                        L_p_p = []
                        for k in range(p):
                            L_tot = [float(self._L_donnee[i][j][k].get()) for j in range(n)]
                            L_p_r.append(np.max(L_tot)-np.min(L_tot))
                            L_p_R.append(np.mean(L_tot))
                            L_p_p.append(np.mean(L_tot))
                        L_o_r.append(np.mean(L_p_r))
                        L_o_R.append(np.mean(L_p_R)) 
                        L_o_p.append(np.max(L_p_p)-np.min(L_p_p))
                    R_r = np.mean(L_o_r)
                    R_R = np.max(L_o_R) - np.min(L_o_R)
                    R_p = np.mean(L_o_p)

                    (d_2_r, d_3_r) = d2_d3_d2b(int(self._var_nb_it.get()), n)
                    d_2_s_r = np.sqrt(d_2_r**2 + (d_3_r**2)/(o*p))
                    D_4_r = (1+3*(d_3_r/d_2_r))                    

                    (d_2_R, d_3_R) = d2_d3_d2b(int(self._var_nb_it.get()), o)
                    d_2_s_R = np.sqrt(d_2_R**2 + d_3_R**2)

                    (d_2_p, d_3_p) = d2_d3_d2b(int(self._var_nb_it.get()), p)
                    d_2_s_p = np.sqrt(d_2_p**2 + d_3_p**2)

                    cond = False
                    for elmt in L_p_r:
                        if elmt > D_4_r*R_r:
                            cond = True
                            break
                    if cond:
                        showerror("Error", "Problem: the subgroup range exceeed the upper range limit")

                    nb_arrondi = int(0.5*(len(str(int(self._var_nb_it.get())))-1))
                    fn = tk.Toplevel(self._fn)
                    fn.title("Result")
                    L_sigma_r = [R_r/d_2_r, R_r/d_2_s_r]

                    text = "Repeatability (σr): \n- Rr/d2: "+str(round(L_sigma_r[0], nb_arrondi)) \
                            +"\n- Rr/d2* : "+str(round(L_sigma_r[1], nb_arrondi))
                    ttk.Label(fn, text = text).grid(row=0, column=0)

                    if (R_R/d_2_s_R)**2 > (L_sigma_r[0]**2)/(n*p) and \
                            (R_R/d_2_s_R)**2 > (L_sigma_r[1]**2)/(n*p):
                        L_sigma_R = [R_R/d_2_R, R_R/d_2_s_R, 
                                    np.sqrt((R_R/d_2_s_R)**2 - (L_sigma_r[0]**2)/(n*p)),
                                    np.sqrt((R_R/d_2_s_R)**2 - (L_sigma_r[1]**2)/(n*p))]
                        text = "Reproducibility (σR): \n- RR/d2: "+str(round(L_sigma_R[0], nb_arrondi))\
                                + "\n- RR/d2* : "+str(round(L_sigma_R[1], nb_arrondi))\
                                + "\n- √(RR/d2*)² - σr²/np: "+str(round(L_sigma_R[2], nb_arrondi)) \
                                + "\n- √(RR/d2*)² - σr*²/np: "+str(round(L_sigma_R[3],  nb_arrondi))
                        ttk.Label(fn, text = text).grid(row=0, column=1) 
                    else:
                        L_sigma_R = [R_R/d_2_R, R_R/d_2_s_R, R_R/d_2_s_R, R_R/d_2_s_R]
                        text = "Reproducibility (σR): \n- RR/d2: "+str(round(L_sigma_R[0], nb_arrondi))\
                                + "\n- RR/d2*: "+str(round(L_sigma_R[1], nb_arrondi))
                        ttk.Label(fn, text = text).grid(row=0, column=1) 

                    if (R_p/d_2_s_p)**2 > (L_sigma_r[0]**2)/(n*o) and\
                        (R_p/d_2_s_p)**2 > (L_sigma_r[1]**2)/(n*o):
                        L_sigma_p = [R_p/d_2_p, R_p/d_2_s_p, 
                                    np.sqrt((R_p/d_2_s_p)**2 - (L_sigma_r[0]**2)/(n*o)),
                                    np.sqrt((R_p/d_2_s_p)**2 - (L_sigma_r[1]**2)/(n*o))]

                        text = "Product (σp): \n- Rp/d2: "+str(round(L_sigma_p[0], nb_arrondi))\
                                + "\n- Rp/d2*: "+str(round(L_sigma_p[1], nb_arrondi))\
                                + "\n- √(Rp/d2*)² - σr²/no: "+str(round(L_sigma_p[2], nb_arrondi))\
                                + "\n- √(Rp/d2*)² - σr*²/no: "+str(round(L_sigma_p[3], nb_arrondi))
                        ttk.Label(fn, text = text).grid(row=0, column=2) 
                    else:
                        L_sigma_p = [R_p/d_2_p, R_p/d_2_s_p, R_p/d_2_s_p, R_p/d_2_s_p]

                        text = "Product (σp): \n- Rp/d2: "+str(round(L_sigma_p[0], nb_arrondi))\
                                + "\n- Rp/d2*: "+str(round(L_sigma_p[1], nb_arrondi))
                        ttk.Label(fn, text = text).grid(row=0, column=2) 

                    sigma_RR_2 = L_sigma_r[1]**2 + L_sigma_R[3]**2
                    sigma_Var_2 = sigma_RR_2 + L_sigma_p[3]**2
                    
                    text = "Repeatability and Reproducibility (σrR): "+str(round(np.sqrt(sigma_RR_2), nb_arrondi))\
                            +"\nTotal standard deviation (σvar): "+str(round(np.sqrt(sigma_Var_2), nb_arrondi))

                    L_prop = [(L_sigma_r[1]**2)/sigma_Var_2,
                            (L_sigma_R[3]**2)/sigma_Var_2,
                            sigma_RR_2/sigma_Var_2,
                            (L_sigma_p[1]**2)/sigma_Var_2]
                    Att = 1- np.sqrt(L_prop[3])
                    text += "\n\nRepeatability Proportion of Total Variation (%): "+str(round(100*L_prop[0], 2))\
                            +"\nReproducibility Proportion of Total Variation (%): "+str(round(100*L_prop[1], 2))\
                            +"\nCombined Repeatability and Reproducibility Proportion of Total Variation (%): "+str(round(100*L_prop[2], 2))\
                            +"\nThat proportion of the Total Variance that is consumed by Product Variation (%): "+str(round(100*L_prop[3], 2))\
                            +"\n\nIntraclass Correlation Coefficient: "+str(round(L_prop[3], nb_arrondi+2))\
                            +"\nProduction process signals will be attenuated by: "+str(round(100*Att, nb_arrondi))+" %"

                    C = (float(self._var_USL.get())-float(self._var_LSL.get()))/(6*L_sigma_r[1])
                    L_C = [C*np.sqrt(1-.8), C*np.sqrt(1-.5), C*np.sqrt(1-.2)] 

                    text += "\n\nCan track process improvement up to Cp80: "+str(round(L_C[0], nb_arrondi))+ " while a First Class Monitor."\
                            "\nCan track process improvement up to Cp50: "+str(round(L_C[1], nb_arrondi))+ " while a Second Class Monitor."\
                            "\nCan track process improvement up to Cp20: "+str(round(L_C[2], nb_arrondi))+ " while a Third Class Monitor."
                    PE = 0.675*np.sqrt(L_sigma_r[1]**2)

                    text += "\n\nThe Probable Error of a single measurement is: "+str(round(PE, nb_arrondi))\
                            +"\nThe Smallest Effective Measurement Increment is: "+str(round(0.2*PE, nb_arrondi))\
                            +"\nThe Largest Effective Measurement Increment is: "+str(round(2*PE, nb_arrondi))\
                            +"\nThe Specifications Limits are "+str(round(self._var_LSL.get(), nb_arrondi))+" and "+str(round(self._var_USL.get(), nb_arrondi))\
                            +"\nThe Watershed Specifications are "+str(round(float(self._var_LSL.get())-0.2*PE, nb_arrondi))+" and "\
                            +str(round(float(self._var_USL.get())+0.2*PE, nb_arrondi))\
                            +"\n96% Manufacturing Specifications are thus "+str(round(float(self._var_LSL.get())+2*PE, nb_arrondi))+" to "\
                            +str(round(float(self._var_USL.get())-2*PE, nb_arrondi))
                    ttk.Label(fn, text = text, justify="left").grid(row=1, column=0, columnspan=3) 
                    fn.mainloop()

    def __del__(self):
        pass

if '__main__' == __name__:
    fn = app()
