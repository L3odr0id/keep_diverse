from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from .save_plot_safely import save_plot_safely
from .knee import Knee


@dataclass
class DisplayKneeArgs:
    total_files_count: int
    split_by: int
    relative_eps: float
    max_tries: int
    min_indices_count: int
    filter_rounds: int

    def to_string(self) -> str:
        return f"/{self.filter_rounds} rounds. Total files count: {self.total_files_count}. Split by: {self.split_by}. Relative eps: {self.relative_eps}. Max tries: {self.max_tries}. Min indices count: {self.min_indices_count}."


def knee_plot(ax1, knee: Knee):
    ax1.clear()
    ax1.plot(
        knee.x_values,
        knee.y_values,
        "b-",
        linewidth=2,
        label="File's removal frequency",
    )

    pct = knee.value / len(knee.y_values) * 100

    ax1.axvline(
        x=knee.value,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Knee point: {knee.value} ({pct:.1f}%)",
    )

    ax1.set_xlabel("File")
    ax1.set_ylabel("Times to remove")
    ax1.set_title("Knee Detection Plot")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))


def sems_plot(ax2, sems_list: list[float]):
    ax2.clear()
    rounds = list(range(len(sems_list)))
    ax2.plot(rounds, sems_list, "g-", linewidth=2)
    ax2.set_xlabel("Round")
    ax2.set_ylabel("SEM of knee point")
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))


class Plot:
    def __init__(self, output_file: str, display_knee_args: DisplayKneeArgs):
        self.output_file = output_file
        self.display_knee_args = display_knee_args

    def draw(self, knee: Knee, sems_list: list[float], round_number: int):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
        plt.subplots_adjust(bottom=0.1)

        knee_plot(ax1, knee)
        sems_plot(ax2, sems_list)

        ax2.text(
            0.5,
            -0.15,
            f"{round_number}" + self.display_knee_args.to_string(),
            transform=ax2.transAxes,
            ha="center",
            fontsize=8,
            style="italic",
        )

        save_plot_safely(fig, self.output_file)


class NoOutputKneePlot(Plot):
    def __init__(self):
        pass

    def draw(self, knee: Knee, sems_list: list[float], round_number: int):
        pass
