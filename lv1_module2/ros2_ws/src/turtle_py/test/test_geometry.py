"""액션 서버의 순수 계산 함수 테스트. ROS 노드를 생성하지 않는다."""

import math

import pytest

from turtle_py.ex06_polygon_action_server import (
    angle_to_goal, distance_between, is_reached, normalize_angle,
)


@pytest.mark.parametrize('coords, expected', [
    ((1, 2, 4, 6), 5),
    ((4, 6, 1, 2), 5),
    ((-3, -4, 0, 0), 5),
    ((2, 2, 2, 2), 0),
])
def test_distance_normal_and_boundary(coords, expected):
    assert distance_between(*coords) == pytest.approx(expected)


def test_distance_invalid_input():
    with pytest.raises(TypeError):
        distance_between(0, 0, 'invalid', 1)


@pytest.mark.parametrize('theta, gx, gy, expected', [
    (0, 1, 0, 0),
    (0, 0, 1, math.pi / 2),
    (math.pi / 2, 1, 0, -math.pi / 2),
    (0, -1, 0, math.pi),
    (-3 * math.pi / 4, -1, 1, -math.pi / 2),
    (3 * math.pi / 4, -1, -1, math.pi / 2),
])
def test_angle_normal_and_wrap_boundary(theta, gx, gy, expected):
    assert angle_to_goal(0, 0, theta, gx, gy) == pytest.approx(expected)


def test_angle_translated_position():
    assert angle_to_goal(2, 3, 0, 2, 4) == pytest.approx(math.pi / 2)


def test_angle_invalid_input():
    with pytest.raises(TypeError):
        angle_to_goal(0, 0, 'invalid', 1, 1)


@pytest.mark.parametrize('angle, expected', [
    (0, 0), (3 * math.pi, math.pi), (-3 * math.pi, -math.pi),
    (2 * math.pi + 0.3, 0.3),
])
def test_normalize_angle(angle, expected):
    assert normalize_angle(angle) == pytest.approx(expected)


def test_normalize_angle_range():
    for k in range(-500, 501):
        assert -math.pi <= normalize_angle(k * 0.037) <= math.pi


def test_normalize_angle_invalid_input():
    with pytest.raises(ValueError):
        normalize_angle(math.inf)


@pytest.mark.parametrize('gx, gy, tolerance, expected', [
    (0.1, 0, 0.2, True),
    (0.5, 0, 0.2, False),
    (0.3, 0.4, 0.5, True),  # 정확히 경계에 있으면 도달
    (0.3, 0.4, math.nextafter(0.5, 0), False),
    (0.3, 0.4, math.nextafter(0.5, math.inf), True),
    (0, 0, 0, True),
    (0.0001, 0, 0, False),
])
def test_is_reached_normal_and_boundary(gx, gy, tolerance, expected):
    assert is_reached(0, 0, gx, gy, tolerance) is expected


def test_is_reached_negative_tolerance():
    with pytest.raises(ValueError):
        is_reached(0, 0, 1, 1, -0.1)


def test_is_reached_invalid_input():
    with pytest.raises(TypeError):
        is_reached(0, 0, 1, 1, 'invalid')
