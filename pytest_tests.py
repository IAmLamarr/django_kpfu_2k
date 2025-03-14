import pytest

@pytest.mark.parametrize(
    ('a', 'b', 'expected'),
    [
        (1, 2, 3),
        (4, 5, 9),
        (10, 7, 17)
    ]
)
def test_sum(a, b, expected):
    assert a + b == expected


@pytest.fixture
def petya_fixture():
    user = {
        'first_name': 'Petya',
        'last_name': 'Invanov',
        'age': 10,
    }
    
    return user

def test_if_petya_is_10_years_old(petya_fixture):
    assert petya_fixture.get('age') == 10