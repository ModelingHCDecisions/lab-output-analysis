import matplotlib.pyplot as plt
import numpy as np
from deampy.plots.plot_support import output_figure

from MultiSurvivalModelClasses import MultiCohort

MORTALITY_PROB = 0.1    # probability of death over each time-step
TIME_STEPS = 100        # length of simulation
ALPHA = 0.05            # significance level for calculating confidence intervals
COHORT_POP_SIZE = 100      # population size of the cohort


nSimCohorts = []    # number of simulated cohorts used to make predictions
# will be populated with [2^2, 2^3, 2^4, ... , 2^13 = 8,192]
for i in range(2, 10):
    nSimCohorts.append(pow(2, i))

# create the figure
fig = plt.figure('Prediction Intervals', figsize=(4, 3.5))
plt.title('{:.0%} Prediction Intervals'.format(1-ALPHA))
plt.xlim([max(1/MORTALITY_PROB - 5, 0), 1/MORTALITY_PROB + 5])   # range of x-axis
plt.ylim([nSimCohorts[0]/2, nSimCohorts[-1]*2])     # range of y-axis

# calculate prediction intervals for different number of simulated cohorts
for n in nSimCohorts:

    # create a multi cohort object
    multiCohort = MultiCohort(
        ids=range(n),
        pop_sizes=[COHORT_POP_SIZE] * n,
        mortality_probs=[MORTALITY_PROB]*n)

    # simulate the multiple cohorts
    multiCohort.simulate(TIME_STEPS)

    # get the overall mean of survival times
    mean = multiCohort.multiCohortOutcomes.statMeanSurvivalTime.get_mean()
    # get the prediction interval for the mean survival time
    PI = multiCohort.multiCohortOutcomes.statMeanSurvivalTime.get_PI(ALPHA)

    # find the coordinates of the estimated mean and confidence intervals
    mean_x = mean   # mean of mean survival times
    mean_y = n   # population size
    PI_xs = np.linspace(PI[0], PI[1], 2)  # [lower upper] of the prediction interval
    PI_ys = mean_y * np.ones(2)  # [popSize popSize]

    plt.semilogy(mean_x, mean_y, 'ko', base=2)  # draw the estimated mean (in log scale)
    plt.semilogy(PI_xs, PI_ys, 'k', base=2)     # draw the confidence interval (in log scale)

plt.axvline(1/MORTALITY_PROB, color='b', ls='--', linewidth=.5)

# labels
plt.ylabel('Number of Simulated Cohorts')
plt.xlabel('Survival Time (Years)') #+ ' (Expected Value = ' + str(1/MORTALITY_PROB) + ')'
plt.tight_layout()
output_figure(plt=plt, filename='figs/pi by n.png', dpi=300)
