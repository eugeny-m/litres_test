import pandas as pd
from typing import Dict


# get dataframe from csv file
def get_dataframe(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(
        filepath_or_buffer=filepath,
        sep=';',
        decimal=',',
        parse_dates=['Ship Date', 'Order Date'],
        date_parser=lambda x: pd.datetime.strptime(x, '%m/%d/%y')
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
    result = dict()  # type: Dict

    def extract_filtered_data(df, param):
        # get min and max param values
        min_val = df[param].min()
        max_val = df[param].max()

        # filter df by min and max value
        min_df = df.loc[df[param] == min_val]
        max_df = df.loc[df[param] == max_val]

        res = {
            'min': {
                'min_val': min_val,
                'objects': min_df['Product ID'].values.tolist()
            },
            'max': {
                'max_val': max_val,
                'objects': max_df['Product ID'].values.tolist()
            },
        }
        return res

    # dataframe grouped by product id
    grouped_by_product = df[['Product ID', 'Profit']].groupby(['Product ID'])

    # get dataframe with product repeats count
    products_counted = grouped_by_product['Product ID'].count().reset_index(name='count')

    # filter dataframe by max and min repeats value
    products_by_count = extract_filtered_data(
        df=products_counted,
        param='count'
    )
    result['products_by_count'] = products_by_count

    # get dataframe with products and Profit sums
    profit_sums = grouped_by_product['Profit'].sum().reset_index(name='sum')
    products_by_profit = extract_filtered_data(
        df=profit_sums,
        param='sum'
    )
    result['products_by_profit'] = products_by_profit

    return result


def get_delivery_time_mean(df: pd.DataFrame) -> pd.datetime:
    df['Delivery Time'] = df['Ship Date'] - df['Order Date']
    return df['Delivery Time'].mean()


def main():
    # TODO: parse path from args
    filepath = 'Orders.csv'
    df = get_dataframe(filepath)

    # - посчитать общий профит с точностью до цента
    pf_sum = get_profit_sum(df)
    print(f'******* Общий профит с точностью до цента *********')
    print(f'Профит: {pf_sum} \n')

    # get best and worst ratings
    ratings = get_best_and_worst_products(df)

    # - найти самые лучшие продукты по продажам,
    #   по количеству продаж и по профиту соответственно
    print('******* Лучшие товары *********')
    print('-По количеству продаж')
    print('Максимальное количество продаж одного товара:',
          ratings['products_by_count']['max']['max_val'])
    print('Product IDs:')
    for p in ratings['products_by_count']['max']['objects']:
        print(f'   {p}')
    print()
    print('-По суммарному профиту')
    print('Максимальный суммарный профит:',
          ratings['products_by_profit']['max']['max_val']
    )
    print('Product IDs:')
    for p in ratings['products_by_profit']['max']['objects']:
        print(f'   {p}')
    print()

    # - найти самые худшие продукты по продажам,
    #   по количеству продаж и по профиту соответственно
    print('******* Худшие товары *********')
    print('-По количеству продаж')
    print('Минимальное количество продаж одного товара:',
          ratings['products_by_count']['min']['min_val'])
    print('Product IDs:')
    print(', '.join(ratings['products_by_count']['min']['objects']))
    # for p in ratings['products_by_count']['min']['objects']:
    #     print(f'   {p}')
    print()

    print('-По суммарному профиту')
    print('Минимальный профит:',
          ratings['products_by_profit']['min']['min_val']
    )
    print('Product IDs:')
    for p in ratings['products_by_profit']['min']['objects']:
        print(f'   {p}')
    print()

    # - найти средний срок доставки товара клиенту
    delivery_time_mean = get_delivery_time_mean(df)
    print('******* Средний срок доставки товара клиенту *******')
    print(delivery_time_mean)


if __name__ == '__main__':
    main()
