import argparse
import pandas as pd

from typing import Dict, Tuple


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
    products_counted = grouped_by_product['Product ID'].count().reset_index(
        name='count')

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


def get_delivery_time_mean_and_std(df: pd.DataFrame) -> Tuple:
    df['Delivery Time'] = df['Ship Date'] - df['Order Date']
    return df['Delivery Time'].mean(), df['Delivery Time'].std()


def write_products_counts_and_profit(
        df: pd.DataFrame,
        outfile: str = 'out_products.csv'
) -> None:
    """
    Function create dataframe with
    id, Product ID, Sells Count, Profit Sum columns
    and write it to <outfile> csv file
    """
    grouped_by_product = df[['Product ID', 'Profit']].groupby(['Product ID'])
    # get ordered by product id dataframe Product Id - Sells Count
    products_counted = grouped_by_product['Product ID'].count().reset_index(
        name='Sells Count').sort_values(by=['Product ID'], ascending=True)

    # get ordered by product id dataframe Product Id - Profit Sum
    profit_sums = grouped_by_product['Profit'].sum().reset_index(
        name='Profit Sum').sort_values(by=['Product ID'], ascending=True)

    # add Profit Sum column to products_counted dataframe
    products_counted['Profit Sum'] = profit_sums['Profit Sum']
    products_counted.to_csv(outfile)
    print('******* Файл out_products.csv сохранен в директории проекта *******')


def get_and_print_results(df: pd.DataFrame) -> None:

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
    delivery_mean, delivery_std = get_delivery_time_mean_and_std(df)
    print('******* Средний срок доставки товара клиенту *******')
    print(f'{delivery_mean} ,(total_seconds={delivery_mean.total_seconds()})\n')

    # - найти стандартное отклонение от среднего срока доставки товара клиенту
    print('******* Стандартное отклонение от среднего срока доставки товара '
          'клиенту *******')
    print(f'{delivery_std}, (total_seconds={delivery_std.total_seconds()})\n')


def main():
    parser = argparse.ArgumentParser(
        description='Print some statistics from csv file')
    parser.add_argument(
        '--csv_file',
        type=str,
        required=True,
        help='path to csv file'
    )
    args = parser.parse_args()

    filepath = args.csv_file
    df = get_dataframe(filepath)
    # print all results we need
    get_and_print_results(df)

    # - посчитать и вывести в CSV-файл продажи,
    #   количество продаж и профит по каждому продукту
    write_products_counts_and_profit(df)


if __name__ == '__main__':
    main()
