from plotly.offline.offline import get_plotlyjs
import pkgutil
import pandas as pd
import plotly.express as px


class ReportData:
    tabular_data = None  # [["header"], [1]]
    time_series_data = []  # [{"timestamp":1, "value": 1}]
    bar_chart_data = []  # [{"value":1, "count": 1}]


PKG_NAME = "plotly_offline_report"


class ReportGenerator:
    _report_html_template = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Data Report</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <!-- import Bootstrap -->
            {style}
        </head>
        <body>
            {scripts}
            <div class="container-fluid">
                <div class="row">
                <div class="col-md-1"></div>
                <div class="col-md-10">
                    <h1>Data Report</h1>
                    {report_sections}
                </div>
                <div class="col-md-1"></div>
                </div>
            </div>
        </body>
    </html>
    """
    _window_plotly_config = """\
    <script type="text/javascript">\
    window.PlotlyConfig = {MathJaxConfig: 'local'};\
    </script>"""

    def __init__(self, report_data, report_filename):
        self._report_data: ReportData = report_data
        self._report_filename = report_filename
        self._report_sections = []

    def add_report_section(self, report_section):
        self._report_sections.append(report_section)

    def _compose_report_sections(self):
        composed_sections = ""
        for item in self._report_sections:
            composed_sections += f"""
         <div class="row" style="margin-top:100px"> 
            <div class="col-md-12"> 
               {item} 
            </div>
         </div>
         """
        return composed_sections

    def _gen_report_html_str_for_ts_data(self):
        data = self._report_data.time_series_data
        data.sort(key=lambda x: x["timestamp"])
        # plot sth
        x = [d["timestamp"] for d in data]
        y = [d["value"] for d in data]
        df = pd.DataFrame({"x": x, "y": y})
        fig = px.line(
            df.groupby(["x"]).sum().sort_index(),
            render_mode="svg",
        )
        fig.update_layout(
            height=900,
            xaxis_title="Time(s)",
            yaxis_title="Value",
        )
        return f"""
            <h3> Time Series Data </h3>
            {fig.to_html(full_html=False, include_plotlyjs=False)}
        """

    def _gen_report_html_str_for_barchart_data(self):
        data = self._report_data.bar_chart_data
        data.sort(key=lambda x: x["value"])
        # plot sth
        x = [d["value"] for d in data]
        y = [d["count"] for d in data]
        df = pd.DataFrame({"x": x, "y": y})
        fig = px.bar(
            df.groupby(["x"]).sum().sort_index(),
        )
        fig.update_layout(
            height=900,
            xaxis_title="Time(s)",
            yaxis_title="Value",
        )
        return f"""
            <h3> Bar Chart Data </h3>
            {fig.to_html(full_html=False, include_plotlyjs=False)}
        """

    def _gen_report_html_str_for_tabular_data(self):
        data = self._report_data.tabular_data
        df = pd.DataFrame(data[1:])
        df.columns = data[0]
        df_stylers = (
            df.style.bar(
                subset=list(df.columns)[1:],
                align="zero",
                color=["PaleVioletRed", "LightSkyBlue"],
            )
            .set_table_attributes('class="table table-bordered border-dark"')
            .format(
                precision=2,
                thousands=",",
            )
            .set_sticky(axis="columns")
        )
        return f"""
            <h2> Tabular Data </h2>
            {df_stylers.to_html()}
        """

    def gen_report_html_str(self):
        self._report_sections = [
            self._gen_report_html_str_for_tabular_data(),
            self._gen_report_html_str_for_barchart_data(),
            self._gen_report_html_str_for_ts_data(),
        ]
        plotlyjs_script = f"""
        {self._window_plotly_config}
        <script type="text/javascript">{get_plotlyjs()}</script>
        """
        bootstrapjs = f"""<script>{pkgutil.get_data(f"{PKG_NAME}.assets", "bootstrap.bundle.min.js").decode("utf-8")}</script>"""
        bootstrapcss = f"""<style>{pkgutil.get_data(f"{PKG_NAME}.assets", "bootstrap.min.css").decode("utf-8")}</style>"""
        return self._report_html_template.format(
            report_sections=self._compose_report_sections(),
            style=bootstrapcss,
            scripts=f"{plotlyjs_script}\n{bootstrapjs}",
        )

    def gen_report_file(self):
        with open(self._report_filename, "w", encoding="utf-8") as f:
            f.write(self.gen_report_html_str())
