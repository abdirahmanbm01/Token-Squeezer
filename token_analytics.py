import numpy as np
from typing import List, Dict
from compression_engine import CompressionResult

class TokenAnalytics:
    GPT4_INPUT_COST_PER_1K = 0.03

    def __init__(self, input_cost_per_1k: float = GPT4_INPUT_COST_PER_1K):
        self.input_cost_per_1k = input_cost_per_1k
        self.results_history: List[CompressionResult] = []

    def add_result(self, result: CompressionResult):
        self.results_history.append(result)

    def calculate_cost_savings(self, result: CompressionResult) -> Dict[str, float]:
        original_cost = (result.original_tokens / 1000) * self.input_cost_per_1k
        compressed_cost = (result.compressed_tokens / 1000) * self.input_cost_per_1k
        savings = original_cost - compressed_cost
        return {
            'original_cost': original_cost,
            'compressed_cost': compressed_cost,
            'savings': savings,
            'savings_percentage': (savings / original_cost * 100) if original_cost > 0 else 0
        }

    def get_aggregate_stats(self) -> Dict:
        if not self.results_history:
            return {}
        total_original_tokens = sum(r.original_tokens for r in self.results_history)
        total_compressed_tokens = sum(r.compressed_tokens for r in self.results_history)
        total_savings = sum(self.calculate_cost_savings(r)['savings'] for r in self.results_history)
        avg_compression_ratio = np.mean([r.savings_ratio for r in self.results_history])
        return {
            'total_original_tokens': total_original_tokens,
            'total_compressed_tokens': total_compressed_tokens,
            'total_cost_savings': total_savings,
            'average_compression_ratio': avg_compression_ratio,
            'num_compressions': len(self.results_history)
        }