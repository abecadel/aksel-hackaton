import pandas as pd


class MercCategories():
    def __init__(self, cat_file):
        self.cats = pd.read_csv(cat_file)

    def find_by_cat3(self, cat):
        ret = self.cats[self.cats['cat_3'].str.lower() == cat.lower()]
        if len(ret) > 0:
            return ret.iloc[0].values
        else:
            ret = self.cats[self.cats['cat_2'].str.lower() == cat.lower()]
            if len(ret) > 0:
                return ret.iloc[0].values
            else:
                return ['N/A', 'N/A', 'N/A']


if __name__ == "__main__":
    m = MercCategories('../mercari_cats.csv')
    print(m.find_by_cat3('Cup'))
