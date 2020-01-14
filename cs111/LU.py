# From in-class transcripts from Lectures 3-4, January 14-16, 2020

import numpy as np

#############################################################################
# Factor A = L@U with no pivoting                                           #
#############################################################################

def LUfactorNoPiv(A):
    """Factor a square matrix, A == L @ U (no partial pivoting)
    Parameters: 
      A: the matrix.
    Outputs (in order):
      L: the lower triangular factor, same dimensions as A, with ones on the diagonal
      U: the upper triangular factor, same dimensions as A
    """
    
    # Check the input
    m, n = A.shape
    assert m == n, 'input matrix A must be square'
    
    # Make a copy of the matrix that we will transform into L and U
    LU = A.astype(np.float64).copy()
    
    # Eliminate each column in turn
    for piv_col in range(n):
            
        # Update the rest of the matrix
        pivot = LU[piv_col, piv_col]
        assert pivot != 0., "pivot is zero, can't continue"
        for row in range(piv_col + 1, n):
            multiplier = LU[row, piv_col] / pivot
            LU[row, piv_col] = multiplier
            LU[row, (piv_col+1):] -= multiplier * LU[piv_col, (piv_col+1):]
            
    # Separate L and U in the result
    U = np.triu(LU)
    L = LU - U + np.eye(n)
    
    return (L, U)

#############################################################################
# Solve a unit lower triangular system L@y = b by forward substitution      #
#############################################################################

def Lsolve(L, b):
    """Forward solve a unit lower triangular system Ly = b for y
    Parameters: 
      L: the matrix, must be square, lower triangular, with ones on the diagonal
      b: the right-hand side vector
    Output:
      y: the solution vector to L @ y == b
    """
    
    # Check the input
    m, n = L.shape
    assert m == n, "matrix L must be square"
    assert np.all(np.tril(L) == L), "matrix L must be lower triangular"
    assert np.all(np.diag(L) == 1), "matrix L must have ones on the diagonal"
    
    # Make a copy of b that we will transform into the solution
    y = b.astype(np.float64).copy()
    
    # Forward solve
    for col in range(n):
        y[col+1:] -= y[col] * L[col+1:, col]
        
    return y



#############################################################################
# Solve an upper triangular system U@x = y by back substitution             #
#############################################################################

def Usolve(U, y):
    """Backward solve an upper triangular system Ux = y for x
    Parameters: 
      U: the matrix, must be square, upper triangular, with nonzeros on the diagonal
      y: the right-hand side vector
    Output:
      x: the solution vector to U @ x == y
    """
    
    raise NotImplemented("you will write Usolve in hw2")
        
    return 


#############################################################################
# Factor A = L@U with (optional) partial pivoting                           #
#############################################################################

def LUfactor(A, pivoting = True):
    """Factor a square matrix with partial pivoting, A[p,:] == L @ U
    Parameters: 
      A: the matrix.
      pivoting: whether or not to do partial pivoting
    Outputs (in order):
      L: the lower triangular factor, same dimensions as A, with ones on the diagonal
      U: the upper triangular factor, same dimensions as A
      p: the permutation vector that permutes the rows of A by partial pivoting
    """
    
    # Check the input
    m, n = A.shape
    assert m == n, 'input matrix A must be square'
    
    # Initialize p to be the identity permutation
    p = np.array(range(n))
    
    # Make a copy of the matrix that we will transform into L and U
    LU = A.astype(np.float64).copy()
    
    # Eliminate each column in turn
    for piv_col in range(n):
        
        # Choose the pivot row and swap it into place
        if pivoting:
            piv_row = piv_col + np.argmax(LU[piv_col:, piv_col]) 
            assert LU[piv_row, piv_col] != 0., "can't find nonzero pivot, matrix is singular"
            LU[[piv_col, piv_row], :]  = LU[[piv_row, piv_col], :]
            p[[piv_col, piv_row]]      = p[[piv_row, piv_col]]
            
        # Update the rest of the matrix
        pivot = LU[piv_col, piv_col]
        assert pivot != 0., "pivot is zero, can't continue"
        for row in range(piv_col + 1, n):
            multiplier = LU[row, piv_col] / pivot
            LU[row, piv_col] = multiplier
            LU[row, (piv_col+1):] -= multiplier * LU[piv_col, (piv_col+1):]
            
    # Separate L and U in the result
    U = np.triu(LU)
    L = LU - U + np.eye(n)
    
    return (L, U, p)


#############################################################################
# Solve A@x = b by LU factorization with partial pivoting                   #
#############################################################################

def LUsolve(A, b):
    """Solve a linear system Ax = b for x by LU factorization with partial pivoting.
    Parameters: 
      A: the matrix.
      b: the right-hand side
    Outputs (in order):
      x: the computed solution
      rel_res: relative residual norm,
        norm(b - Ax) / norm(b)
    """
    
    # Check the input
    m, n = A.shape
    assert m == n, 'input matrix A must be square'
    
    # LU factorization
    L, U, p = LUfactor(A)
    
    # Forward and back substitution
    y = Lsolve(L,b[p])
    x = Usolve(U,y)
    
    # Residual norm
    rel_res = npla.norm(b - A@x) / npla.norm(b)
    
    return (x, rel_res)

