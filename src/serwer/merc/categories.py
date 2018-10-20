import pandas as pd


class MercCategories():
    def __init__(self, cat_file):
        self.cats = pd.read_csv(cat_file)

    def prep_query(self, cat):
        print(cat)
        if cat == "coffee_mug":
            cat = "cup"
        elif cat == "granny_smith":
            cat = "apple"
        elif cat == "cowboy_boot":
            cat = "boots"

        return cat

    def prep_resp(self, ret):
        a = {
            'category_name': ret['category_name'],
            'stars': ret['normalized_ratio'],
            'sale_time': ret['median']
        }
        print(a)
        return a

    def find_by_cat3(self, cat):
        cat = self.prep_query(cat)
        ret = self.cats[self.cats['cat_3'].str.lower().str.contains(cat.lower())]
        if len(ret) > 0:
            return self.prep_resp(ret.iloc[0])
        else:
            ret = self.cats[self.cats['cat_2'].str.lower().str.contains(cat.lower())]
            if len(ret) > 0:
                return self.prep_resp(ret.iloc[0])
            else:
                return {
                    'category_name': 'N/A',
                    'stars': 0,
                    'sale_time': 0
                }


if __name__ == "__main__":
    m = MercCategories('../sales_to_list_ratio.csv')
    print(m.find_by_cat3('Cup'))
