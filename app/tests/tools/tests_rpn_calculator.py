import pytest

from tools.rpn_calculator import RPNCalculator, RPNCalculatorError


@pytest.mark.parametrize(
    "expression, expected",
    [
        pytest.param('2 5 +', 7),
        pytest.param('4 1 -', 3),
        pytest.param('5 2 *', 10),
        pytest.param('6 3 /', 2),
        pytest.param('10 4 %', 2),
    ],
)
def test_calculate_basic_operators(expression, expected):
    assert RPNCalculator(expression).solve() == expected


@pytest.mark.parametrize(
    "expression, expected",
    [
        pytest.param('2 3 ^', 8),
        pytest.param('5 !', 120),
        pytest.param('9 sqrt', 3),
        pytest.param('6 3 /', 2),
        pytest.param('e ln', 1),
        pytest.param('e 8 ^', 2980.957987041727),
        pytest.param('100 log', 2),
    ],
)
def test_calculate_advanced_operators(expression, expected):
    assert RPNCalculator(expression).solve() == expected


@pytest.mark.parametrize(
    "expression, expected",
    [
        pytest.param('pi cos', -1),
        pytest.param('0.56 acos', 0.9764105267938343),
        pytest.param('38 sin', 0.2963685787093853),
        pytest.param('0.94 asin', 1.2226303055219356),
        pytest.param('176 tan', 0.07092999229222396),
        pytest.param('68 tan', -2.0400815980159464),
    ],
)
def test_calculate_trigonometric_operators(expression, expected):
    assert RPNCalculator(expression).solve() == expected


@pytest.mark.parametrize(
    "expression, expected",
    [
        pytest.param('2 3 2 ^ ^', 512),
        pytest.param('5 3 ! ^', 15625),
        pytest.param('2 3 ^ 4 ! *', 192),
        pytest.param('5 sin 2 ^ cos', 0.6061894378341296),
        pytest.param('2 3 + 4 ^ 5 *', 3125),
        pytest.param('3 ! exp ln', 6),
        pytest.param('pi 2 * 3 / sin 3 ^ exp 15 sqrt log * cos 0.2 / exp', 8.601139193813882),
    ],
)
def test_calculate_complex_operators(expression, expected):
    assert RPNCalculator(expression).solve() == expected


@pytest.mark.parametrize(
    "expression, expected",
    [
        pytest.param('2 +', "Insufficient operands for operator."),
        pytest.param('1 0 /', "ZeroDivisionError: float division by zero."),
        pytest.param('5 hello -', "KeyError: Invalid expression. ('hello')"),
        pytest.param("0.5 !", "Factorial operator need a integer."),
        pytest.param("5 ! 5 + 2", "Multiple elements left on stack. Invalid expression."),
    ],
)
def test_calculate_errors_operators(expression, expected):
    with pytest.raises(RPNCalculatorError) as exc_info:
        RPNCalculator(expression).solve()

    assert exc_info.value.message == expected