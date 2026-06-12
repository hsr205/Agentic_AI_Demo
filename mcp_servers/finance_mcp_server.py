import csv
import logging
import sys
from pathlib import Path

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

    def register_tools(self) -> None:
        @self.mcp.tool()
        def download_historical_stock_data(ticker_list: list[str], start_date_str: str, end_date_str: str,
                                           csv_path: str):
            """Retrieves a precise list of ticker data based on values for a specific ticker and the data

            Args:
                ticker_list: A list of stock ticker symbols (e.g., AAPL, GOOGL, TSLA).
                start_date_str: The exact date of to begin fetching stock data from in ISO format YYYY-MM-DD (e.g., '2026-06-09').
                end_date_str: The exact date of to end fetching stock data from in ISO format YYYY-MM-DD (e.g., '2026-06-09').
                csv_path: The CSV path to which the financial data is saved to for later data analysis (e.g., /Claude_Agent/data/)
            """

            dataframe: pd.DataFrame = yf.download(tickers=ticker_list,
                                                  start=start_date_str,
                                                  end=end_date_str).reset_index()

            filtered_spark_dataframe: DataFrame = self._get_filtered_spark_dataframe(dataframe=dataframe,
                                                                                     ticker_list=ticker_list)

            filtered_spark_dataframe.coalesce(1).write.csv(path=csv_path, header=True)

        @self.mcp.tool()
        def execute_monte_carlo_simulation():
            """
            """
            pass

        @self.mcp.tool()
        def create_visualization_for_data_analysis():
            """
            """
            pass



    def _get_filtered_spark_dataframe(self, dataframe: pd.DataFrame, ticker_list: list[str]) -> DataFrame:
        spark_dataframe: DataFrame = self._spark_session.createDataFrame(data=dataframe)

        spark_dataframe.createOrReplaceTempView("financial_data")

        filtered_columns_list: list[str] = self._get_filtered_columns_from_dataframe(
            spark_dataframe=spark_dataframe)

        dataframe_column_name_list: list[str] = self._get_column_names(ticker_list=ticker_list)

        filtered_dataframe: DataFrame = spark_dataframe.select(*filtered_columns_list).toDF(*dataframe_column_name_list)

        return filtered_dataframe

    def _get_column_names(self, ticker_list) -> list[str]:

        result_list: list[str] = ["Date"]

        for ticker_str in ticker_list:
            column_name: str = ticker_str + "_Close_Price"
            result_list.append(column_name)

        return result_list

    def _get_filtered_columns_from_dataframe(self, spark_dataframe: DataFrame) -> list[str]:
        columns_list: list[str] = []

        for column_name_str in spark_dataframe.columns:
            if "Date" in column_name_str or "Close" in column_name_str:
                columns_list.append(column_name_str)

        return columns_list


if __name__ == "__main__":
    finance_mcp_server: FinanceMCPServer = FinanceMCPServer()
    finance_mcp_server.run_stdio_transport()
