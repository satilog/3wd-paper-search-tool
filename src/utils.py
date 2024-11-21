import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def load_env_var(var_name):
    """Load an environment variable."""
    return os.getenv(var_name)


def save_to_csv(data, file_name):
    """Save data to a CSV file, appending if the file already exists."""
    df = pd.DataFrame(data)
    if not os.path.exists(file_name):
        df.to_csv(file_name, index=False)
    else:
        existing_df = pd.read_csv(file_name)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_csv(file_name, index=False)
