import numpy as np
from scipy.optimize import minimize, LinearConstraint, Bounds

# -------------------------
# Método de Newton
# -------------------------
def maxent_newton(G, a, tol=1e-8, maxit=100, max_time_s=None):
    """
    Solver MaxEnt via Newton.
    Retorna (p, n_iter)
    """
    import time
    start_time = time.perf_counter()

    M, N = G.shape
    rank_check_matrix = np.vstack([np.ones((1, N)), G])
    if np.linalg.matrix_rank(rank_check_matrix) < (M + 1):
        raise ValueError("Restrições não são linearmente independentes.")

    z = np.zeros((M, 1))
    for k in range(maxit):
        if max_time_s is not None and time.perf_counter() - start_time > max_time_s:
            raise TimeoutError("Solver Newton excedeu tempo limite.")

        s = G.T @ z
        s -= np.max(s)
        exp_s = np.exp(s)
        p = exp_s / np.sum(exp_s)
        h = G @ p - a

        if np.linalg.norm(h) < tol:
            break

        Pmat = np.diag(p.flatten())
        H = G @ Pmat @ G.T - (G @ p) @ (G @ p).T
        try:
            dz = -np.linalg.solve(H, h)
        except np.linalg.LinAlgError:
            raise np.linalg.LinAlgError("Hessiana singular")

        z += dz

    return p.flatten(), k + 1


# -------------------------
# BFGS / L-BFGS via primal (SLSQP)
# -------------------------
def _resolver_maxent_primal(G, a, tol=1e-9, maxit=1000, max_time_s=None):
    """
    Solver MaxEnt via otimização primal (SLSQP).
    Retorna (p, n_iter)
    """
    import time
    start_time = time.perf_counter()

    M, N = G.shape

    def objetivo(p):
        p_stable = p + 1e-18
        return np.sum(p_stable * np.log(p_stable))

    A_eq = np.vstack([G, np.ones((1, N))])
    b_eq = np.vstack([a, np.array([[1]])]).flatten()
    constraints = LinearConstraint(A_eq, b_eq, b_eq)
    bounds = Bounds(0, 1)
    p0 = np.full(N, 1 / N)

    # Função wrapper para checar timeout
    def callback(pk):
        if max_time_s is not None and time.perf_counter() - start_time > max_time_s:
            raise TimeoutError("Solver primal excedeu tempo limite.")

    resultado = minimize(
        fun=objetivo,
        x0=p0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints,
        tol=tol,
        options={'maxiter': maxit, 'disp': False},
        callback=callback
    )

    return resultado.x, getattr(resultado, "nit", 0)


def maxent_bfgs(G, a, tol=1e-9, maxit=1000, max_time_s=None):
    return _resolver_maxent_primal(G, a, tol=tol, maxit=maxit, max_time_s=max_time_s)


def maxent_lbfgs(G, a, tol=1e-9, maxit=1000, max_time_s=None):
    return _resolver_maxent_primal(G, a, tol=tol, maxit=maxit, max_time_s=max_time_s)
