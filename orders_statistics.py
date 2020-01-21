import pandas as pd
from typing import Dict


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


def get_best_and_worst_products(df: pd.DataFrame) -> Dict:
    """
    this function extract best and worst products
    by sold count and by profit value
    """
    result = dict() # type: Dict

    # dataframe grouped by product id
    grouped_by_product = df[['Product ID']].groupby(['Product ID'])['Product ID']

    # get max and min product repeats values
    products_counted = grouped_by_product.count().reset_index(name='count')
    sold_max = products_counted['count'].max()
    sold_min = products_counted['count'].min()

    # filter dataframe by max and min repeats value
    products_sold_max = products_counted.loc[products_counted['count'] == sold_max]
    products_sold_min = products_counted.loc[products_counted['count'] == sold_min]
    result['products_sold_max'] = products_sold_max['Product ID'].values.tolist()
    result['products_sold_min'] = products_sold_min['Product ID'].values.tolist()

    return result


def main():
    # TODO: parse path from args
    filepath = 'Orders.csv'
    df = get_dataframe(filepath)

    # - посчитать общий профит с точностью до цента
    pf_sum = get_profit_sum(df)
    print(f'Profit sum = {pf_sum}')

    # - найти самые лучшие продукты по продажам,
    #   по количеству продаж и по профиту соответственно
    ratings = get_best_and_worst_products(df)
    print('The best products by sold count')
    for p in ratings['products_sold_max']:
        print(f'   {p}')

    print('The worst products by sold count')
    for p in ratings['products_sold_min']:
        print(f'   {p}')


if __name__ == '__main__':
    main()
