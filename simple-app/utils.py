from sklearn.preprocessing import LabelEncoder

def encode_cat_variables(data, fnames_cat, le=None):
    data_ = data.copy()
    if le is None:
        le = {}
        for fname in fnames_cat:
            series = data[fname].astype(str)
            le_i = LabelEncoder().fit(series)
            data_[fname] = le_i.transform(series)
            le[fname] = le_i
    else:
        for fname in fnames_cat:
            le_i = le[fname]
            data_[fname] = le_i.transform(data[fname].astype(str))
    return data_, le