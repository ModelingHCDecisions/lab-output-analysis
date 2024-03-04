import matplotlib.pyplot as plt
import numpy as np
from deampy.plots.plot_support import output_figure

from MultiSurvivalModelClasses import MultiCohort

# to test the hypothesis that true mean survival time is not equal to the null
NULL_SURVIVAL_TIME = 9      # null hypothesis
SIM_POP_SIZES = [10, 100, 1000, 10000]  # population size of simulated cohorts to test the null hypothesis
MORTALITY_PROB = 0.1    # probability of death over each time-step
TIME_STEPS = 100        # length of simulation
ALPHA = 0.05            # significance level for calculating confidence intervals

# create a multi cohort object
multiCohort = MultiCohort(
    ids=[1] * len(SIM_POP_SIZES),  # [1, 1, ..., 1] using the same random number generator seed for all cohorts
    pop_sizes=SIM_POP_SIZES,
    mortality_probs=[MORTALITY_PROB]*len(SIM_POP_SIZES))

# simulate the multiple cohorts
multiCohort.simulate(TIME_STEPS)

# create the figure
fig = plt.figure('t-Confidence Intervals', figsize=(4, 3.5))
plt.title('{:.0%} Confidence Intervals'.format(1-ALPHA))
plt.xlim([0, 2*1/MORTALITY_PROB])   # range of x-axis
plt.ylim([min(SIM_POP_SIZES) / 10, max(SIM_POP_SIZES) * 10])  # range of y-axis

# add confidence intervals to the figure
for i in range(len(SIM_POP_SIZES) - 1, -1, -1):
    # mean survival time
    mean = multiCohort.multiCohortOutcomes.meanSurvivalTimes[i]
    # confidence interval
    CI = multiCohort.multiCohortOutcomes.get_cohort_CI_mean_survival(i, ALPHA)

    # find the coordinates of the estimated mean and confidence intervals
    mean_x = mean           # mean survival time
    mean_y = SIM_POP_SIZES[i]   # population size of this cohort
    CI_xs = np.linspace(CI[0], CI[1], 2) # [lower upper] of the confidence interval
    CI_ys = mean_y*np.ones(2)    # [popSize popSize]

    print(SIM_POP_SIZES[i], round(0.5*(CI[1]-CI[0]), 3))

    plt.semilogy(mean_x, mean_y, 'ko')  # draw the estimated mean (in log scale)
    plt.semilogy(CI_xs, CI_ys, 'k')     # draw the confidence interval (in log scale)

# adding a blue vertical line to show the null value
# plt.axvline(NULL_SURVIVAL_TIME, color='b', linewidth =.5)
# adding a black dashed vertical line to show the true survival mean
plt.axvline(1/MORTALITY_PROB, color='b', ls='--', linewidth=.5)

# get y limits in order to position annotations
axes = plt.gca()
y_min, y_max = axes.get_ylim()

# adding annotation near the top of the plot, y_max, and close to the vertical line @ 1/MORTALITY_PROB
# plt.annotate(' True Unknown Mean ',
#              xy=(1/MORTALITY_PROB, y_max),
#              xytext=(1/MORTALITY_PROB, y_min),
#              color='b',
#              rotation=90,
#              fontsize=7,
#              verticalalignment='bottom',
#              horizontalalignment='right', )

# labels
plt.ylabel('Population Size of the Simulated Cohort')
plt.xlabel('Mean Survival Time')
output_figure(plt, filename='figs/ci by n.png')
