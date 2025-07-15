from fastapi import APIRouter
from app.services.match_evaluation import precision_at_k, recall_at_k, f1_at_k, ndcg_at_k
import numpy as np
import pandas as pd

router = APIRouter()

@router.get('/evaluate')
def evaluate():
    try:
        df = pd.read_csv('data/labeled_pairs.csv')
        y_true = df['match_score'].values > 0.5
        y_pred = df['predicted_score'].values
        
        # Ensure we have data
        if len(y_true) == 0 or len(y_pred) == 0:
            return {"error": "No evaluation data available"}
        
        k = min(5, len(y_true))  # Don't exceed data size
        
        return {
            'precision@k': precision_at_k(y_true, y_pred, k),
            'recall@k': recall_at_k(y_true, y_pred, k),
            'f1@k': f1_at_k(y_true, y_pred, k),
            'ndcg@k': ndcg_at_k(y_true, y_pred, k),
            'data_points': len(y_true),
            'k_used': k
        }
    except FileNotFoundError:
        return {"error": "Evaluation data file not found. Please run model training first."}
    except Exception as e:
        return {"error": f"Evaluation failed: {str(e)}"} 