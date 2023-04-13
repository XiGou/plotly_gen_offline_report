import unittest
import tempfile
import os
import random


from plotly_offline_report.gen_report import ReportGenerator, ReportData

TMP_DIR = "/tmp/plotly_gen_report"


class TestGenReport(unittest.TestCase):
    def setUp(self) -> None:
        if not (os.path.exists(TMP_DIR) and os.path.isdir(TMP_DIR)):
            os.mkdir(TMP_DIR)
    def _get_sample_ts_data(self, count):
        tmp_num = 0
        result = []
        for i in range(count):
            tmp_num += random.randint(-3, 3)
            result.append({"timestamp": i, "value": tmp_num})
        return result

    def test_gen_report(self):
        report_data = ReportData()
        report_data.tabular_data = [[f"col_{i}" for i in range(10)]]
        report_data.tabular_data.extend(
            [[random.randint(-100, 100) for i in range(10)] for j in range(5)]
        )
        report_data.bar_chart_data = [
            {"value": i, "count": random.randint(1, 100)} for i in range(10)
        ]
        report_data.time_series_data = self._get_sample_ts_data(1000)
        test_report_file = tempfile.NamedTemporaryFile(
            dir=TMP_DIR, delete=False, suffix=".html"
        )
        ReportGenerator(report_data, test_report_file.name).gen_report_file()


if __name__ == "__main__":
    unittest.main()
