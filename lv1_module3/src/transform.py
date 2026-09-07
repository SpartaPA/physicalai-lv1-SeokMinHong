"""문제 5 — 4x4 동차변환 모듈. (학생 작성용 템플릿)

동차변환 생성/역변환, 점과 방향의 구분, 벡터화된 점군 변환,
정규방정식 기반 최소자승법을 직접 구현한다.
"""

from __future__ import annotations

import numpy as np

from .vectors import inverse_gauss_jordan

__all__ = [
    "inv_T",
    "inv_T_batch",
    "least_squares_normal_equation",
    "make_T",
    "rmse",
    "to_homogeneous",
    "transform_direction",
    "transform_point",
    "transform_points",
]


def make_T(R, t) -> np.ndarray:
    """회전 R(3x3)과 병진 t(3,)로 4x4 동차변환을 만든다.

        T = [[R, t],
             [0, 1]]

    R 이 3x3 이 아니면 ValueError.
    """
    # TODO: 문제 5-1
    R = np.array(R, dtype=float)
    if R.shape != (3, 3):
        raise ValueError("R이 3x3이 아닙니다.")

    t = np.array(t, dtype=float)
    if t.shape != (3, ):
        raise ValueError("t가 3, 이 아닙니다.")

    return np.vstack((np.hstack((R, t.reshape(-1, 1))), np.array([0., 0., 0., 1.], dtype=float)))


def inv_T(T) -> np.ndarray:
    """동차변환의 역변환. **일반 역행렬 함수를 쓰지 않고** 공식으로 구한다.

        T^-1 = [[R^T, -R^T t],
                [  0,      1]]

    유도: T^-1 을 [[S, u], [0, 1]] 로 두고 T T^-1 = I 를 풀면
          R S = I -> S = R^T (R 이 직교),  R u + t = 0 -> u = -R^T t.

    4x4 가 아니면 ValueError.
    """
    # TODO: 문제 5-1
    T = np.array(T, dtype=float)
    if T.shape != (4,4):
        raise ValueError("T가 4x4가 아닙니다.")

    R, t = T[:3, :3], T[:3, -1]
    return np.vstack((np.hstack((R.T, -R.T @ t.reshape(-1, 1))), np.array([0., 0., 0., 1.], dtype=float)))


def inv_T_batch(Ts) -> np.ndarray:
    """(N, 4, 4) 동차변환 묶음을 **반복문 없이** 한 번에 역변환한다.

    `inv_T` 와 같은 공식을 배치 축으로 확장한 것이다.
    문제 5-4 의 속도 비교에서 쓴다 — 단건 호출은 파이썬/NumPy 호출 오버헤드가
    지배해서 연산량 차이가 드러나지 않기 때문이다.

    힌트: 전치는 `np.swapaxes(..., 1, 2)`, 배치 행렬-벡터 곱은
          `np.einsum("nij,nj->ni", ...)` 로 쓸 수 있다.
    """
    # TODO: 문제 5-4
    Ts = np.array(Ts, dtype=float)
    if Ts.ndim != 3 or Ts.shape[1] != 4 or Ts.shape[2] != 4:
        raise ValueError("동차변환의 묶음이 아닙니다.")

    T_inv = np.zeros_like(Ts)
    Rs = np.swapaxes(Ts[:, :3, :3], 1, 2)
    T_inv[:, :3, :3] = Rs

    np.einsum("nij,nj->ni", Rs, Ts[:, :3, 3], out=T_inv[:, :3, 3])
    T_inv[:, :3, 3] *= -1

    T_inv[:, 3, 3] = 1.
    return T_inv


def to_homogeneous(P, w: float = 1.0) -> np.ndarray:
    """(3,) 또는 (N,3) 좌표에 마지막 성분 w 를 붙인다.

    w = 1 이면 점(위치), w = 0 이면 방향(벡터).
    """
    # TODO: 문제 5-2
    P = np.array(P, dtype=float)
    if not ((P.ndim == 1 and P.shape == (3,)) or (P.ndim == 2 and P.shape[1] == 3)):
        raise ValueError("점 또는 점들이 3차원이 아닙니다.")

    return np.hstack((P, np.full((P.shape[0], 1), w) if P.ndim == 2 else np.full((1,), w)))


def transform_point(T, p) -> np.ndarray:
    """점 변환 (w = 1): 회전과 병진이 모두 적용된다. 반환은 (3,)."""
    # TODO: 문제 5-2
    T = np.array(T, dtype=float)
    if T.shape != (4,4):
        raise ValueError("동차 행렬이 아닙니다.")

    p = np.array(p, dtype=float)
    if p.shape != (3, ) or p.ndim != 1:
        raise ValueError("점이 아닙니다.")

    return (T @ np.append(p, 1.))[:3]


def transform_direction(T, v) -> np.ndarray:
    """방향 변환 (w = 0): 회전만 적용되고 병진은 무시된다. 반환은 (3,)."""
    # TODO: 문제 5-2
    T = np.array(T, dtype=float)
    if T.shape != (4, 4):
        raise ValueError("동차 행렬이 아닙니다.")

    v = np.array(v, dtype=float)
    if v.shape != (3,) or v.ndim != 1:
        raise ValueError("벡터가 아닙니다.")

    return (T @ np.append(v, 0.))[:3]


def transform_points(T, P, w: float = 1.0) -> np.ndarray:
    """(N,3) 점군을 **반복문 없이** 한 번에 변환한다. (3,) 입력도 받아야 한다.

    힌트: (T @ P_h.T).T 대신 P_h @ T.T 를 쓰면 전치가 한 번으로 끝나고
          메모리 접근도 행 방향이라 캐시에 유리하다.
    """
    # TODO: 문제 5-2 / 6-2
    T = np.array(T, dtype=float)
    if T.shape != (4, 4):
        raise ValueError("동차 행렬이 아닙니다.")

    P = np.array(P, dtype=float)
    if not ((P.ndim == 1 and P.shape == (3,)) or (P.ndim == 2 and P.shape[1] == 3)):
        raise ValueError("점군 또는 점이 아닙니다.")

    P_h = to_homogeneous(P, w)
    return (P_h @ T.T)[:3] if P_h.ndim == 1 else (P_h @ T.T)[:, :3]


def least_squares_normal_equation(A, b):
    """정규방정식 (A^T A) x = A^T b 를 직접 세워 최소자승해를 구한다.

    - (A^T A) 의 역행렬은 문제 4 에서 만든 `inverse_gauss_jordan` 으로 구한다
      (`np.linalg.lstsq` 는 노트북에서 **비교 대상**으로만 쓴다).
    - 근거: 잔차 r = b - A x 가 최소일 때 r 은 A 의 열공간에 수직이므로 A^T r = 0.

    Returns
    -------
    x : 최소자승해
    residual : b - A x
    """
    # TODO: 문제 5-5
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    A_inv = inverse_gauss_jordan(A.T @ A)
    x = A_inv @ (A.T @ b)
    return x, b - A @ x


def rmse(residual) -> float:
    """잔차의 RMSE = sqrt(mean(r^2))."""
    # TODO: 문제 5-5
    return float(np.sqrt(np.mean(residual ** 2)))
