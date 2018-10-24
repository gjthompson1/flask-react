import sys
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

clf = LogisticRegression()

clf_std = Pipeline([
    ('vect', StandardScaler()),
    ('clf', LogisticRegression())
    ])

MODEL_COLUMNS = [
    'vote_average',
    'vote_count',
    # 'revenue',
    # 'runtime',
    # 'budget',
    # 'popularity',
    'release_year',
]

MODEL_COLUMNS_SCALED = ['scaled_{}'.format(x) for x in MODEL_COLUMNS]

def train_model(goods, bads):

    good_df = pd.DataFrame(goods)
    bad_df = pd.DataFrame(bads)

    good_df = good_df[MODEL_COLUMNS]
    bad_df = bad_df[MODEL_COLUMNS]

    good_df['is_good'] = 1
    bad_df['is_good'] = 0

    df = pd.concat([good_df,bad_df],axis=0)
    # df = df.apply(lambda x: x.fillna(x.mean()),axis=0)
    # print(df, file=sys.stderr)
    clf.fit(df[MODEL_COLUMNS], df['is_good'])
    clf_std.fit(df[MODEL_COLUMNS], df['is_good'])

    # [{'importance':x,'variable':y} for x, y in zip(logit_model.steps[1][1].coef_[0],MODEL_COLUMNS)]
    return {
        # 'coef': {x:y for x,y in zip(MODEL_COLUMNS,clf.steps[1][1].coef_[0])},
        # 'intercept': clf.steps[1][1].intercept_[0],
        'coef': {x:y for x,y in zip(MODEL_COLUMNS,clf.coef_[0])},
        'intercept': clf.intercept_[0],
    }

def score_records(records):

    if 'coef_' in clf_std.steps[1][1].__dict__:
    # if 'coef_' in clf.__dict__:
        df = pd.DataFrame(records)
        # print(df.columns, file=sys.stderr)
        df = df.reindex(columns=MODEL_COLUMNS)
        # df = df.apply(lambda x: x.fillna(x.mean()),axis=0)
        res1 = clf.predict_proba(df)
        for x, y in zip(records,res1):
            x['score_manual'] = y[1]

        res2 = clf_std.predict_proba(df)
        for x, y in zip(records,res2):
            x['score_manual_scaled'] = y[1]

    return records
