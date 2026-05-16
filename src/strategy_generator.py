from strategies.base_strategies import BaseStrategies


class StrategyGenerator:
    """Provides a list of strategy dicts for the backtester."""

    @staticmethod
    def generate_all_strategies():
        strategies = []
        for name, func in BaseStrategies.get_all():
            strategies.append({"name": name, "signal_func": func})
        return strategies