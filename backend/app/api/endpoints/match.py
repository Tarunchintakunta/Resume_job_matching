from fastapi import APIRouter
from app.services.match_evaluation import precision_at_k, recall_at_k, f1_at_k, ndcg_at_k
import numpy as np
import pandas as pd

router = APIRouter()

@router.get('/evaluate')
def evaluate():
    df = pd.read_csv('data/labeled_pairs.csv')
    y_true = df['match_score'].values > 0.5
    y_pred = df['predicted_score'].values
    k = 5
    return {
        'precision@k': precision_at_k(y_true, y_pred, k),
        'recall@k': recall_at_k(y_true, y_pred, k),
        'f1@k': f1_at_k(y_true, y_pred, k),
        'ndcg@k': ndcg_at_k(y_true, y_pred, k)
    } 