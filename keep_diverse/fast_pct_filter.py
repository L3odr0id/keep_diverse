import random

import numpy as np

from .poisson_metric import poisson_metric_value
from .logger import get_logger


def distances_without_idxs(
    old_distances: dict[tuple[int, int], float], idxs_to_remove: list[int]
) -> dict[tuple[int, int], float]:
    new_distances = {}

    for idx1, idx2 in old_distances.keys():
        if idx1 not in idxs_to_remove and idx2 not in idxs_to_remove:
            new_distances[(idx1, idx2)] = old_distances[(idx1, idx2)]

    return new_distances


class FastPctFilter:
    def __init__(
        self,
        initial_indices: list[int],
        relative_eps: float,
        max_tries: int,
        min_indices_count: int,
        text_set_distances: dict[tuple[int, int], float],
    ):
        self.initial_indices = initial_indices
        self.current_idxs = self.initial_indices
        self.current_metric_value = poisson_metric_value(text_set_distances)
        self.relative_eps = relative_eps
        self.max_tries = max_tries
        self.min_indices_count = min_indices_count
        self.is_finished = False
        self.iteration = 0
        self.text_set_distances = text_set_distances
        self.last_removed_amount = -1
        self.logger = get_logger()

    def remove_idxs_attempt(
        self,
        current_idxs: list[int],
        removal_pct: float,
        current_value: float,
        num_to_remove: int,
        attempt: int,
    ) -> tuple[list[int], float] | None:
        indices_to_remove = random.sample(current_idxs, num_to_remove)

        new_distances = distances_without_idxs(
            self.text_set_distances, indices_to_remove
        )

        new_value = poisson_metric_value(new_distances)

        metric_change = current_value - new_value
        eps_change = self.relative_eps * current_value
        info = f"Try {attempt + 1}. Remove {removal_pct * 100}% ({num_to_remove}). Old {current_value}. New {new_value}. Diff: {metric_change}. relative_eps: {self.relative_eps}. Metric change: {metric_change}. relative_eps*prev_value: {eps_change}.  Is metric changed less than eps: {metric_change <= eps_change}"

        if metric_change <= eps_change:
            self.logger.debug(f"Attempt succeeded. {info}")
            self.last_removed_amount = num_to_remove
            remaining_indices = [
                idx for idx in current_idxs if idx not in indices_to_remove
            ]
            return remaining_indices, new_value
        else:
            self.logger.debug(f"Attempt failed. {info}")
            return None

    def try_to_remove_idxs(
        self,
        current_idxs: list[int],
        removal_pct: float,
        current_value: float,
    ) -> tuple[list[int], float, bool]:
        texts_count = len(current_idxs)
        num_to_remove = int(texts_count * removal_pct)

        if (
            texts_count <= 2
            or num_to_remove < 1
            or removal_pct == 1.0
            or texts_count - num_to_remove < self.min_indices_count
            or num_to_remove == self.last_removed_amount
        ):
            return current_idxs, current_value, True

        for attempt in range(self.max_tries):
            result = self.remove_idxs_attempt(
                current_idxs, removal_pct, current_value, num_to_remove, attempt
            )
            if result is not None:
                return result[0], result[1], False

        self.logger.debug(f"All attempts failed")
        return current_idxs, current_value, False

    def search_for_removal_percentage(
        self,
        initial_indices: list[int],
        initial_metric_value: float,
    ) -> tuple[list[int], float]:
        self.logger.debug(f"Start searching for removal percentage.")
        left = 0
        right = 100

        tmp_new_indicies = initial_indices
        tmp_new_metric_value = initial_metric_value

        while left <= right:
            mid = (left + right) // 2
            remove_pct = mid / 100

            self.logger.debug(f"Mid: {mid}. Left: {left}. Right: {right}.")

            new_remaining_indices, new_value, isFinished = self.try_to_remove_idxs(
                initial_indices,
                remove_pct,
                initial_metric_value,
            )

            if isFinished:
                self.logger.debug(f"Break.")
                return (tmp_new_indicies, tmp_new_metric_value)

            removed_successfully = len(new_remaining_indices) < len(initial_indices)

            if removed_successfully:
                tmp_new_indicies = new_remaining_indices
                tmp_new_metric_value = new_value
                self.logger.debug(
                    f"Removed {mid}%. New value: {new_value}. New texts count: {len(new_remaining_indices)}."
                )
                left = mid + 1
            else:
                self.logger.debug(f"Did not removed {mid}%.")
                right = mid - 1

        self.logger.debug(
            f"Finished. Removed {mid}%. New value: {tmp_new_metric_value}. New texts count: {len(tmp_new_indicies)}."
        )
        return (tmp_new_indicies, tmp_new_metric_value)

    def iterate(self):
        if self.is_finished:
            return

        self.iteration += 1

        new_remaining_indices, new_value = self.search_for_removal_percentage(
            self.current_idxs, self.current_metric_value
        )
        successfully_shrunk = len(new_remaining_indices) < len(self.current_idxs)

        self.logger.info(
            f"Iter {self.iteration}. Successfully shrinked: {successfully_shrunk}. New len: {len(new_remaining_indices)}. Old value: {self.current_metric_value} New value: {new_value}. Old count: {len(self.current_idxs)} New count: {len(new_remaining_indices)}."
        )

        if successfully_shrunk:
            self.current_idxs = new_remaining_indices
            self.current_metric_value = new_value
        else:
            self.is_finished = True
