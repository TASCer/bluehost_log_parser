

def test_sample_logs(test_fetch_logs):
    logs = test_fetch_logs
    assert len(logs) >= 1
    # print(logs)
