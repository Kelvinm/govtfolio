from dagster import asset

@asset
def load_trades():
    """
    Load trades data into the database
    """
    # TODO: Implement trades loading
    pass

assets = [load_trades] 