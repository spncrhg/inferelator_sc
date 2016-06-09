import pandas as pd

class TimeSeries:

    def __init__(self, first_condition):
        first_condition_name = first_condition.name
        self.first_condition_name = first_condition_name
        self._condition_name_to_next_condition_name = {}
        self._conditions_by_name = {first_condition_name: first_condition}
        self._time_interval_before_condition = {}
        self._condition_name_order = None
        self._time_interval_order = None
        
    def get_condition_name_order(self, force=False):
        if not force and self._condition_name_order is not None:
            return self._condition_name_order
        conditions_seen = set()
        this_condition = self.first_condition_name
        name_order = []
        next_condition = self._condition_name_to_next_condition_name
        interval_before = self._time_interval_before_condition
        interval_order = [0]  # no time elapsed before first condition (?)
        while this_condition is not None:
            conditions_seen.add(this_condition)
            name_order.append(this_condition)
            this_condition = next_condition.get(this_condition)
            assert this_condition not in conditions_seen, (
                "Cycle found in timeseries condition description. " + repr((name_order, this_condition)))
            if this_condition is not None:
                interval = interval_before[this_condition]   # raises KeyError if missing.
                interval_order.append(interval)
        assert set(self._conditions_by_name) == conditions_seen, (
            "not all conditions ordered:" + repr(set(self._conditions_by_name), conditions_seen))
        self._condition_name_order = name_order
        self._time_interval_order = interval_order
        return name_order
        
    def get_interval_order(self):
        self.get_condition_name_order()
        return self._time_interval_order
        
    def add_condition(self, prev_condition_name, condition, time_interval_before_condition):
        assert self._condition_name_order is None, (
            "Cannot modify time series after it has been compiled into an ordered sequence."
        )
        name = condition.name
        assert name not in self._conditions_by_name, (
            "duplicate condition: " + repr(name)
        )
        self._conditions_by_name[name] = condition
        self._time_interval_before_condition[name] = time_interval_before_condition
        assert prev_condition_name not in self._condition_name_to_next_condition_name, (
            "duplicate following condition " + repr(prev_condition_name, name)
        )
        self._condition_name_to_next_condition_name[prev_condition_name] = name
 