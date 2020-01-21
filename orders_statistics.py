import pandas as pd


# get dataframe from csv file
def get_dataframe(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(
        filepath_or_buffer=filepath,
        sep=';',
        decimal=',',
    )
    return df


# TODO: ask round result or cut 2 values after point
def get_profit_sum(df: pd.DataFrame) -> str:
    profit_sum = df['Profit'].sum()
    return f'{profit_sum:.{2}f}'


def main():
    # TODO: parse path from args
    filepath = 'Orders.csv'
    df = get_dataframe(filepath)

    # print profit sum
    pf_sum = get_profit_sum(df)
    print(f'Profit sum = {pf_sum}')


if __name__ == '__main__':
    main()
