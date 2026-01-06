
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path("d:/Backup/Projects/work/Posters Evaluation/posters_evaluation")))

from src.strategies import get_strategy, DirectStrategy, ReasoningStrategy, DeepAnalysisStrategy, StrictStrategy

def test_strategy_factory():
    print("Testing Strategy Factory...")
    
    s1 = get_strategy("direct")
    assert isinstance(s1, DirectStrategy), f"Expected DirectStrategy, got {type(s1)}"
    print("[OK] direct -> DirectStrategy")
    
    s2 = get_strategy("reasoning")
    assert isinstance(s2, ReasoningStrategy), f"Expected ReasoningStrategy, got {type(s2)}"
    print("[OK] reasoning -> ReasoningStrategy")
    
    s3 = get_strategy("deep_analysis")
    assert isinstance(s3, DeepAnalysisStrategy), f"Expected DeepAnalysisStrategy, got {type(s3)}"
    print("[OK] deep_analysis -> DeepAnalysisStrategy")

    s4 = get_strategy("strict")
    assert isinstance(s4, StrictStrategy), f"Expected StrictStrategy, got {type(s4)}"
    print("[OK] strict -> StrictStrategy")
    
    s5 = get_strategy("unknown_strategy")
    assert isinstance(s5, DirectStrategy), f"Expected default DirectStrategy, got {type(s5)}"
    print("[OK] unknown -> DirectStrategy (Default)")

if __name__ == "__main__":
    try:
        test_strategy_factory()
        print("\nALL CHECKS PASSED")
    except Exception as e:
        print(f"\nFAILED: {e}")
        sys.exit(1)
