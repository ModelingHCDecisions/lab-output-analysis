import numpy as np
import matplotlib.pyplot as plt
import MultiSurvivalModelClasses as Cls

MORTALITY_PROB = 0.1    # probability of death over each time-step
POP_SIZE = 500         # population size
TIME_STEPS = 100        # length of simulation
ALPHA = 0.05            # significance level for calculating confidence intervals
NUM_CIs = 100           # number of confidence intervals to visualize

# create a multi cohort object
multiCohort = Cls.MultiCohort(
    ids=range(0, NUM_CIs),  # [0, 1, 2 ..., NUM_CIs]
    pop_sizes=[POP_SIZE] * NUM_CIs,  # [POP_SIZE, POP_SIZE, ..., POP_SIZE]
    mortality_probs=[MORTALITY_PROB] * NUM_CIs)  # [p, p, ....]

# simulate the multiple cohorts
multiCohort.simulate(TIME_STEPS)

# create the figure
fig = plt.figure('t-confidence intervals', figsize=(4.5, 4))
plt.title('{:.0%} Confidence Intervals'.format(1-ALPHA))
plt.xlim([0.5*1 / MORTALITY_PROB, 1.5 * 1 / MORTALITY_PROB])   # range of x-axis
plt.ylim([0, NUM_CIs+1])            # range of y-axis

# add confidence intervals to the figure
for i in range(0, NUM_CIs):
    # mean survival time
    mean = multiCohort.multiCohortOutcomes.meanSurvivalTimes[i]
    # confidence interval of mean survival time
    CI = multiCohort.multiCohortOutcomes.get_cohort_CI_mean_survival(i, ALPHA)
    # plot the confidence interval
    x = np.linspace(CI[0], CI[1], 2)
    y = np.ones(2)
    plt.plot(x, y+i)

# adding a vertical line to show the true survival mean
plt.axvline(1 / MORTALITY_PROB, color='b')

# labels
plt.ylabel('Trials')
plt.xlabel('Survival time' + ' (true mean = ' + str(1 / MORTALITY_PROB) + ' years)')
plt.show()
