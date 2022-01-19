## the function calculates partial correlation between variables
## it is equal to pcorr() function in R

def partial_corr(C):
    """ 
    first-order correlation coefficient
    Partial correlation between X,Y,Z variables
    r(XY/Z), r(XZ/Y), r(YZ/X)
    
    C: array-like matrix 
    """
    C = np.asarray(C)
    p = C.shape[1]
    P_corr = np.zeros((p, p), dtype=np.float64) # sample linear partial correlation coefficients

    corr = np.corrcoef(C,rowvar=False) # Pearson product-moment correlation coefficients.
    corr_inv = np.linalg.inv(corr) # the (multiplicative) inverse of a matrix.

    for i in range(p):
        P_corr[i, i] = 1
        for j in range(i+1, p):
            pcorr_ij = -corr_inv[i,j]/(np.sqrt(corr_inv[i,i]*corr_inv[j,j]))
            P_corr[i,j]=pcorr_ij
            P_corr[j,i]=pcorr_ij

    return P_corr
