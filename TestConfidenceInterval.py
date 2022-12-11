import matplotlib.pyplot as plt
import numpy as np
from deampy.plots.plot_support import output_figure

import MultiSurvivalModelClasses as Cls

MORTALITY_PROB = 0.1    # probability of death over each time-step
POP_SIZE = 250         # population size
TIME_STEPS = 100        # length of simulation
ALPHA = 0.05            # significance level for calculating confidence intervals
NUM_CIs = 100           # number of confidence intervals to visualize


def plot_cis(n, alpha):
    """
    plot 100 confidence intervals for the provided sample size and significance level
    :param n: (int) sample size
    :param alpha: (double) significance level
    """

    # create a multi cohort object
    multiCohort = Cls.MultiCohort(
        ids=range(0, NUM_CIs),  # [0, 1, 2 ..., NUM_CIs]
        pop_sizes=[n] * NUM_CIs,  # [n, n, ..., n]
        mortality_probs=[MORTALITY_PROB] * NUM_CIs)  # [p, p, ....]

    # simulate the multiple cohorts
    multiCohort.simulate(TIME_STEPS)

    # create the figure
    fig, ax = plt.subplots(figsize=(4, 3.5))
    # fig = plt.figure('t-confidence intervals', figsize=(4, 3.5))
    ax.set_title('{:.0%} Confidence Intervals'.format(1-alpha))
    ax.set_xlim([0.5*1 / MORTALITY_PROB, 1.5 * 1 / MORTALITY_PROB])   # range of x-axis
    ax.set_ylim([0, NUM_CIs+1])            # range of y-axis

    # add confidence intervals to the figure
    for i in range(0, NUM_CIs):
        # mean survival time
        mean = multiCohort.multiCohortOutcomes.meanSurvivalTimes[i]
        # confidence interval of mean survival time
        CI = multiCohort.multiCohortOutcomes.get_cohort_CI_mean_survival(i, alpha)
        # plot the confidence interval
        x = np.linspace(CI[0], CI[1], 2)
        y = np.ones(2)
        ax.plot(x, y+i)

    # adding a vertical line to show the true survival mean
    ax.axvline(1 / MORTALITY_PROB, color='b')

    # labels
    ax.set_ylabel('Trials')
    ax.set_xlabel('Survival time' + ' (true mean = ' + str(1 / MORTALITY_PROB) + ' years)')
    output_figure(plt=fig, filename='figs/{:.0f}ci with n={}.png'.format(100*(1-alpha), n))


plot_cis(n=POP_SIZE, alpha=ALPHA)
plot_cis(n=POP_SIZE*4, alpha=ALPHA)
plot_cis(n=POP_SIZE*4, alpha=0.01)
