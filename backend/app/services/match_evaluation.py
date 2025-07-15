import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score

def precision_at_k(y_true, y_pred, k):
    top_k = np.argsort(y_pred)[::-1][:k]
    # Ensure we don't exceed the length of y_true
    actual_k = min(k, len(y_true))
    top_k = top_k[:actual_k]
    return precision_score(y_true[top_k], np.ones(actual_k))

def recall_at_k(y_true, y_pred, k):
    top_k = np.argsort(y_pred)[::-1][:k]
    # Ensure we don't exceed the length of y_true
    actual_k = min(k, len(y_true))
    top_k = top_k[:actual_k]
    return recall_score(y_true[top_k], np.ones(actual_k))

def f1_at_k(y_true, y_pred, k):
    p = precision_at_k(y_true, y_pred, k)
    r = recall_at_k(y_true, y_pred, k)
    return 2 * p * r / (p + r + 1e-8)

def ndcg_at_k(y_true, y_pred, k):
    order = np.argsort(y_pred)[::-1]
    y_true = np.take(y_true, order[:k])
    gains = 2 ** y_true - 1
    discounts = np.log2(np.arange(len(y_true)) + 2)
    dcg = np.sum(gains / discounts)
    ideal_gains = 2 ** np.sort(y_true)[::-1] - 1
    ideal_dcg = np.sum(ideal_gains / discounts)
    return dcg / (ideal_dcg + 1e-8) 