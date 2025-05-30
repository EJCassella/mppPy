import pandas as pd
import pytest


@pytest.fixture
def get_jv_test_data(scope="session"):
	test_data = pd.read_csv("tests/data/jv_test_data.csv", header=None)
	return test_data
