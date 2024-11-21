import pandas as pd


def save_to_csv(data, file_name):
    """Save data to CSV."""
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
