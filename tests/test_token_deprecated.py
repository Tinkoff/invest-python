import os
import uuid
import warnings


def test_warns_when_token_imported():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        os.environ["INVEST_TOKEN"] = uuid.uuid4().hex

        import tinkoff.invest.token as token

        assert token

        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message)
