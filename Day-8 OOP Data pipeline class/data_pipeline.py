import pandas as pd
import os

class DataPipeline:
    """
    A reusable data pipeline for loading, cleaning,
    describing, filtering, and exporting CSV data.

    Mirrors ML engineering patterns used in production systems.
    """

    def __init__(self, filepath: str):
        """
        Initialize the pipeline with a path to a CSV file.

        Args:
            filepath (str): Path to the CSV file.
        """
        self.filepath = filepath   # Store the file path as an instance variable
        self.df = None             # Placeholder — data hasn't been loaded yet

    def load(self) -> "DataPipeline":
        """
        Load the CSV file into a pandas DataFrame.

        Returns:
            self: Allows method chaining (e.g., pipeline.load().clean())

        Raises:
            FileNotFoundError: If the CSV file does not exist.
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")

        self.df = pd.read_csv(self.filepath)
        print(f"Loaded {len(self.df)} rows and {len(self.df.columns)} columns.")
        return self   # Returning self enables method chaining

    def clean(self) -> "DataPipeline":
        """
        Clean the DataFrame by:
          - Dropping fully duplicate rows
          - Stripping whitespace from string columns
          - Filling missing numeric values with column medians

        Returns:
            self: Allows method chaining.

        Raises:
            ValueError: If data has not been loaded yet.
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load() first.")

        before = len(self.df)

        # Drop rows that are 100% identical duplicates
        self.df = self.df.drop_duplicates()

        # For every column that holds strings, strip leading/trailing spaces
        for col in self.df.select_dtypes(include="object").columns:
            self.df[col] = self.df[col].str.strip()

        # Fill missing numbers with that column's median (robust to outliers)
        for col in self.df.select_dtypes(include="number").columns:
            self.df[col] = self.df[col].fillna(self.df[col].median())

        after = len(self.df)
        print(f"Cleaned data. Removed {before - after} duplicate rows.")
        return self

    def describe(self) -> "DataPipeline":
        """
        Print a statistical summary of the loaded DataFrame.

        Returns:
            self: Allows method chaining.

        Raises:
            ValueError: If data has not been loaded yet.
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load() first.")

        print("\n--- DataFrame Info ---")
        print(self.df.info())           # Column names, types, null counts

        print("\n--- Statistical Summary ---")
        print(self.df.describe())       # Count, mean, std, min, max per column

        print("\n--- Missing Values ---")
        print(self.df.isnull().sum())   # Count of nulls per column

        return self

    def filter(self, column: str, value) -> "DataPipeline":
        """
        Filter rows where the given column matches the given value.

        Args:
            column (str): The column name to filter on.
            value: The value to match (any type).

        Returns:
            self: Allows method chaining.

        Raises:
            ValueError: If data is not loaded or column doesn't exist.
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load() first.")

        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found. "
                             f"Available: {list(self.df.columns)}")

        before = len(self.df)
        self.df = self.df[self.df[column] == value]  # Boolean mask filter
        print(f"Filtered '{column}' == '{value}'. "
              f"{len(self.df)} of {before} rows remain.")
        return self

    def export(self, output_path: str) -> None:
        """
        Export the current DataFrame to a new CSV file.

        Args:
            output_path (str): Destination file path for the exported CSV.

        Raises:
            ValueError: If data has not been loaded yet.
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load() first.")

        self.df.to_csv(output_path, index=False)  # index=False omits row numbers
        print(f"Data exported to: {output_path}")


# --- Run it ---
if __name__ == "__main__":
    pipeline = DataPipeline("your_file.csv")

    # Method chaining: each method returns self so calls stack neatly
    pipeline.load().clean().describe()

    # Filter to a specific value (adjust column/value to match your CSV)
    # pipeline.filter("Region", "West")

    pipeline.export("cleaned_output.csv")