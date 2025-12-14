import numpy as np
import pandas as pd


def euclidean_distance(
        vec1: np.ndarray, 
        vec2: np.ndarray
        ) -> float:
    """Calculate the Euclidean distance between two equal-length NumPy vectors."""
    vec1 = np.asarray(vec1, dtype=float)
    vec2 = np.asarray(vec2, dtype=float)

    if vec1.shape != vec2.shape:
        raise ValueError("Vectors must have the same shape.")

    return np.linalg.norm(vec1 - vec2)


def compute_distances(
        df_rag: pd.DataFrame, 
        query_embedding: list | np.ndarray,
        ) -> pd.DataFrame:
    """Computes euclidean distances"""
    embeddings = np.vstack(df_rag["embedding"].to_numpy())
    query = np.array(query_embedding)

    df_rag["distance"] = np.linalg.norm(embeddings - query, axis=1)
    return df_rag


def retrieve_top_k(
        df_rag: pd.DataFrame,
        query_embedding: list | np.ndarray,
        top_k: int = 3
        ) -> pd.DataFrame:
    """Retrieves top k based on embedding euclidean distance"""
    df_rag_distance = compute_distances(df_rag, query_embedding)
    df_rag_ranked = df_rag_distance.sort_values(
        'distance').reset_index().iloc[:top_k]
    return df_rag_ranked