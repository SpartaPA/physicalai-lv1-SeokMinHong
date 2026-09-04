"""문제 1 — 벡터 연산 모듈. (학생 작성용 템플릿)

내적 · 사이각 · 정규화 · 정사영 · 반대칭행렬(외적) · 평면 법선과
가우스 소거 기반의 rank / 행렬식 / 역행렬을 **직접** 구현한다.

규칙
----
- `np.linalg` 는 노트북에서 **검산용으로만** 쓰고, 이 모듈 안에서는 쓰지 않는다.
  (`inverse_gauss_jordan` 이 던지는 `np.linalg.LinAlgError` 예외 타입만 예외)
- 각 함수의 docstring 에 적힌 계약(입력/출력/예외)을 그대로 지킨다.
  노트북의 검증 셀과 `tests/` 가 이 계약을 기준으로 채점된다.
- 구현을 마치면 `raise NotImplementedError(...)` 줄을 지운다.
"""

from __future__ import annotations

import numpy as np

__all__ = [
    "as_vector",
    "dot",
    "norm",
    "angle_between",
    "normalize",
    "project",
    "reject",
    "skew",
    "cross",
    "plane_normal",
    "row_echelon",
    "rank",
    "det",
    "gauss_eliminate",
    "inverse_gauss_jordan",
]


# ---------------------------------------------------------------- 기본 연산

def as_vector(v) -> np.ndarray:
    """입력(리스트/튜플/배열)을 1차원 float 배열로 변환한다.

    1차원이 아니면 ValueError 를 던진다.

    [구현 예시] 아래 세 줄이 이 파일에서 기대하는 코드 스타일이다.
    나머지 함수도 이런 식으로 채워 넣으면 된다.
    """
    arr = np.asarray(v, dtype=float)
    if arr.ndim != 1:
        raise ValueError(f"1차원 벡터가 필요합니다. 받은 shape={arr.shape}")
    return arr


def dot(a, b) -> float:
    """내적. sum(a_i * b_i) 를 직접 계산한다 (`np.dot` 사용 금지).

    두 벡터의 차원이 다르면 ValueError.
    """
    # TODO: 문제 1-1
    a, b = as_vector(a), as_vector(b)
    if a.shape != b.shape:
        raise ValueError("a와 b의 차원이 다릅니다.")
    return float(np.sum(a * b))


def norm(v) -> float:
    """유클리드 노름. sqrt(v·v) — 위에서 만든 dot 을 재사용한다."""
    # TODO: 문제 1-1
    v = as_vector(v)
    return float(np.sqrt(dot(v, v)))


def angle_between(a, b, degrees: bool = True) -> float:
    """두 벡터 사이각. degrees=True 면 도(°), False 면 라디안.

    cos(theta) = (a·b) / (|a||b|)

    주의 1. 영벡터가 들어오면 사이각이 정의되지 않는다 -> ValueError.
    주의 2. 부동소수점 오차로 |cos| 가 1 을 아주 조금 넘으면 arccos 가 nan 을 낸다.
            [-1, 1] 로 clip 해야 무작위 입력에서도 안전하다.
    """
    # TODO: 문제 1-1
    na, nb = norm(a), norm(b)
    if na < 1e-12 or nb < 1e-12:
        raise ValueError("벡터 중 하나가 영벡터입니다.")

    theta = np.arccos(np.clip(dot(a, b) / (na * nb), -1., 1.))
    return float(np.degrees(theta)) if degrees else float(theta)


def normalize(v, eps: float = 1e-12) -> np.ndarray:
    """단위벡터로 정규화한다. v / |v|

    영벡터를 어떻게 처리할지는 **문제 1-2 에서 직접 정한다.**
    노트북 1-2 에서 (1) 아무 처리 없이 나눴을 때 무슨 일이 나는지 관찰하고,
    (2) 선택한 처리 방식과 근거를 마크다운에 적은 뒤, 그 방식대로 여기에 구현한다.
    선택에 따라 노트북/테스트의 검증 코드도 그 방식에 맞춰 작성한다.
    """
    # TODO: 문제 1-2
    v = as_vector(v)
    n = norm(v)
    if n < eps:
        raise ValueError(f"v가 영벡터입니다.")
    return v / n


def project(a, b) -> np.ndarray:
    """a 를 b 방향으로 정사영한 성분.

        proj_b(a) = (a·b / b·b) * b

    분모가 |b|^2 이므로 b 를 미리 정규화할 필요는 없다.
    b 가 영벡터면 ValueError.
    """
    # TODO: 문제 1-3
    a, b = as_vector(a), as_vector(b)
    if a.shape != b.shape:
        raise ValueError("차원이 다릅니다.")
    elif norm(b) < 1e-12:
        raise ValueError("b가 영벡터입니다.")
    return np.multiply(dot(a, b) / dot(b, b), b)


def reject(a, b) -> np.ndarray:
    """a 에서 b 방향 성분을 뺀 나머지(수직 성분). a = project + reject 가 성립해야 한다."""
    # TODO: 문제 1-3
    a, b = as_vector(a), as_vector(b)
    return a - project(a, b)


def skew(a) -> np.ndarray:
    """3차원 벡터 a 에 대응하는 반대칭행렬 [a]_x 를 만든다.

        [a]_x = [[  0, -a3,  a2],
                 [ a3,   0, -a1],
                 [-a2,  a1,   0]]

    만족해야 하는 성질: [a]_x @ b == a x b,  [a]_x.T == -[a]_x
    3차원이 아니면 ValueError.
    """
    # TODO: 문제 1-4
    x = as_vector(a)
    if x.shape != (3,):
        raise ValueError("3차원 벡터가 아닙니다.")
    return np.array([
        [0, -x[2], x[1]],
        [x[2], 0, -x[0]],
        [-x[1], x[0], 0]
    ])


def cross(a, b) -> np.ndarray:
    """외적을 **반대칭행렬 곱으로** 계산한다 (`np.cross` 사용 금지)."""
    # TODO: 문제 1-4
    a, b = as_vector(a), as_vector(b)
    if a.shape != (3,) or b.shape != (3,):
        raise ValueError("a 또는 b가 3차원 벡터가 아닙니다.")
    skew_a = skew(a)
    return skew_a @ b


def plane_normal(P1, P2, P3) -> np.ndarray:
    """세 점이 이루는 평면의 **단위** 법선 벡터.

    두 모서리 벡터(P2-P1, P3-P1)의 외적이 평면에 수직이다.
    세 점이 일직선이면 외적이 영벡터가 되어 평면이 하나로 정해지지 않는다 -> ValueError.
    """
    # TODO: 문제 1-5
    P1, P2, P3 = as_vector(P1), as_vector(P2), as_vector(P3)
    n = cross(P2 - P1, P3 - P1)
    if norm(n) < 1e-12:
        raise ValueError("세 포인트가 직선입니다.")
    return normalize(n)


# ------------------------------------------------- 가우스 소거 기반 선형대수

def row_echelon(A, pivoting: bool = True):
    """행 사다리꼴(row echelon form) 로 만든다.

    Parameters
    ----------
    pivoting : True 면 부분 피벗팅(각 열에서 절댓값이 가장 큰 행을 피벗으로 올림)

    Returns
    -------
    U : (m, n) 상삼각 형태 행렬
    pivot_cols : 피벗이 선 열 인덱스 리스트
    n_swaps : 행 교환 횟수 (행렬식 부호 계산에 필요)

    힌트: 0 인지 판정할 때는 `== 0` 대신 허용오차(tol)를 쓴다.
          예) tol = max(m, n) * np.finfo(float).eps * max(1.0, np.max(np.abs(U)))
    """
    # TODO: 문제 1-6 / 문제 4
    result = np.array(A, dtype=float, copy=True)
    if result.ndim != 2:
        raise ValueError("행렬이 아닙니다.")

    m, n = result.shape
    row = 0
    n_swaps = 0
    pivot_cols = []
    tol = max(m, n) * np.finfo(float).eps * max(1.0, np.max(np.abs(A)))
    for col in range(n):
        if row >= m:
            break
        pivot = row
        if pivoting:
            pivot = row + np.argmax(np.abs(result[row:, col]))
        if np.abs(result[pivot, col]) < tol:
            continue
        if pivot != row:
            n_swaps += 1
            result[[row, pivot]] = result[[pivot, row]]
        for r in range(row + 1, m):
            factor = result[r, col] / result[row, col]
            result[r, col:] -= result[row, col:] * factor
        pivot_cols.append(col)
        row += 1
    return result, pivot_cols, n_swaps


def rank(A) -> int:
    """행 사다리꼴의 피벗 개수 = rank."""
    # TODO: 문제 1-6
    _, pivot, _ = row_echelon(A)
    return len(pivot)


def det(A) -> float:
    """행렬식 = 행 사다리꼴 대각성분의 곱 x (-1)^(행 교환 횟수).

    피벗이 n 개보다 적으면(특이행렬) 0.0 을 돌려준다.
    정사각 행렬이 아니면 ValueError.
    """
    # TODO: 문제 1-6
    A = np.array(A, dtype=np.float64)

    if A.ndim != 2:
        raise ValueError("A가 행렬이 아닙니다.")

    row, col = A.shape
    if row != col:
        raise ValueError("A가 정사각행렬이 아닙니다.")
    U, _, swaps = row_echelon(A)
    return ((-1.) if swaps % 2 else 1.) * np.diagonal(U).prod()


def gauss_eliminate(A, b, pivoting: bool = True, verbose: bool = False):
    """가우스 소거법 + 후진대입으로 Ax = b 를 푼다.

    Parameters
    ----------
    pivoting : True 면 부분 피벗팅을 적용한다. False 면 피벗을 그대로 쓴다
               (문제 4-4 에서 두 경우의 오차를 비교하므로 **둘 다 동작해야 한다**).
    verbose  : True 면 각 소거 단계의 첨가행렬 [A|b] 를 출력한다
               (문제 4-1 이 요구하는 '단계별 출력').

    Returns
    -------
    x : 해 벡터
    steps : 단계별 첨가행렬 [A|b] 스냅샷 리스트 (초기 상태 포함)

    피벗이 0 이면 해가 유일하지 않다 -> ZeroDivisionError.
    """
    # TODO: 문제 4-1
    A = np.array(A, dtype=np.float64)
    if A.ndim != 2:
        raise ValueError("행렬이 아닙니다.")

    m, n = A.shape
    if m != n:
        raise ValueError("정방행렬이 아닙니다.")

    b = as_vector(b)
    if m != b.shape[0]:
        raise ValueError("행 개수가 일치하지 않습니다.")

    U = np.hstack((A, b.reshape(-1, 1)))
    if verbose:
        print(f"첨가 행렬 생성")
        print(U)
    steps = [U.copy()]
    m, n = A.shape
    for row, col in enumerate(n):
        if row >= m:
            break
        pivot = row
        if pivoting:
            pivot = row + np.argmax(np.abs(U[row:, col]))
        if abs(U[pivot, col]) < 1e-18:
            raise ZeroDivisionError("0 on pivot")
        if pivot != row:
            U[[row, pivot]] = U[[pivot, row]]
            if verbose:
                print("피봇팅")
                print(U)
            steps.append(U.copy())
        for r in range(row + 1, m):
            factor = U[r, col] / U[row, col]
            U[r, col:] -= U[row, col:] * factor
        if verbose:
            print("가우스 소거")
            print(U)
        steps.append(U.copy())

    root = []
    for row in range(n):
        foo = 0
        for col in range(row):
            foo += root[col] * U[n - row - 1, n - col - 1]
        root.append((U[-1 - row, -1] - foo) / U[-1 - row, -1 - row - 1])
    root.reverse()

    if verbose:
        print("후진 대입")
        print(root)
    return root, steps


def inverse_gauss_jordan(A) -> np.ndarray:
    """가우스-조던 소거로 역행렬을 구한다. [A|I] -> [I|A^-1].

    정사각이 아니면 ValueError, 특이행렬이면 np.linalg.LinAlgError.
    (`np.linalg.inv` 를 부르지 말고 소거로 직접 구한다)
    """
    # TODO: 문제 4-3
    A = np.array(A, dtype=np.float64)

    if A.ndim != 2:
        raise ValueError("A 행렬이 아닙니다.")

    n, m = A.shape
    if n != m:
        raise np.linalg.LinAlgError("row col이 일치하지 않습니다.")

    I = np.eye(A.shape[0])
    U = np.hstack((A, I))

    for row, col in enumerate(n):
        if row >= m:
            break
        pivot = row + np.argmax(np.abs(U[row:, col]))
        if abs(U[pivot, col]) < 1e-18:
            raise ValueError("역행렬이 없습니다.")
        if pivot != row:
            U[[row, pivot]] = U[[pivot, row]]
        U[row] /= U[row, col]
        for r in range(m):
            if r == row:
                continue
            factor = U[r, col] / U[row, col]
            U[r, col:] -= U[row, col:] * factor
    return U[:, m:]
