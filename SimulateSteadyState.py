import deampy.plots.histogram as hist
import deampy.plots.sample_paths as path
import deampy.statistics as stat

from SurvivalModelClasses import Cohort

MORTALITY_PROB = 0.1    # annual probability of death
TIME_STEPS = 100        # years
SIM_POP_SIZE = 1000     # population size of the simulated cohort

# create a cohort
myCohort = Cohort(id=1, pop_size=SIM_POP_SIZE, mortality_prob=MORTALITY_PROB)

# simulate the cohort over the specified time steps
myCohort.simulate(n_time_steps=TIME_STEPS)

# plot the sample path
path.plot_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve',
    x_label='Time-Step (Year)',
    y_label='Number Survived')

# plot the histogram
hist.plot_histogram(
    data=myCohort.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time',
    x_label='Survival Time (Year)',
    y_label='Count')

# create a summary statistics for observations of survival times
survivalTimeStat = stat.SummaryStat(name='Summary statistics of survival time',
                                    data=myCohort.cohortOutcomes.survivalTimes)

# print the summary statistics
print('Mean survival time (years):', survivalTimeStat.get_mean())
print('95% confidence interval of mean survival time (years):',
      survivalTimeStat.get_t_CI(alpha=0.05))
