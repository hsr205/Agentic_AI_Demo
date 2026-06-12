import logging
import sys

import pandas as pd
import yfinance as yf
from fastmcp import FastMCP
from pyspark.sql import SparkSession, DataFrame

from logger.logger import AppLogger


class FinanceMCPServer:

    def __init__(self) -> None:
        self.mcp: FastMCP = FastMCP(
            name="finance-data-management-server",
            version="1.2.0"
        )

        self.register_tools()

        self._spark_session: SparkSession = SparkSession.builder.appName(name="SparkSession").getOrCreate()

        self._logger = AppLogger.get_logger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, stream=sys.stderr, force=True)

    def run_stdio_transport(self) -> None:
        self.mcp.run(transport="stdio")


    # TODO: Need to include the dates for each observation in the dataset
    def register_tools(self) -> None:
        @self.mcp.tool()
        def download_historical_stock_data(ticker_list: list[str], start_date_str: str, end_date_str: str, csv_path: str):
            """Retrieves a precise list of ticker data based on values for a specific ticker and the data

            Args:
                ticker_list: A list of stock ticker symbols (e.g., AAPL, GOOGL, TSLA).
                start_date_str: The exact date of to begin fetching stock data from in ISO format YYYY-MM-DD (e.g., '2026-06-09').
                end_date_str: The exact date of to end fetching stock data from in ISO format YYYY-MM-DD (e.g., '2026-06-09').
                csv_path: The CSV path to which the financial data is saved to for later data analysis (e.g., /Claude_Agent/data/)
            """

            dataframe: pd.DataFrame = yf.download(tickers=ticker_list,
                                                  start=start_date_str,
                                                  end=end_date_str)
            spark_dataframe: DataFrame = self._spark_session.createDataFrame(data=dataframe)
            spark_dataframe.createOrReplaceTempView("financial_data")

            close_columns_list: list[str] = [column_name_str for column_name_str in spark_dataframe.columns if
                                             "Close" in column_name_str]

            filtered_spark_dataframe = spark_dataframe.select(*close_columns_list)

            filtered_spark_dataframe.write.csv(path=csv_path, header=True)


if __name__ == "__main__":
    finance_mcp_server: FinanceMCPServer = FinanceMCPServer()
    finance_mcp_server.run_stdio_transport()
