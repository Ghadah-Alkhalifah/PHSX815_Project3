import numpy as np
import matplotlib.pyplot as plt

def coin_toss(n, alpha):
    # n: number of coin tosses
    # alpha: probability of landing heads
    
    # Simulate coin tosses
    tosses = np.random.binomial(n, alpha)
    
    # Return the number of heads observed
    return tosses

def likelihood(alpha, n, data):
    # alpha: probability of landing heads
    # n: number of coin tosses
    # data: number of heads observed
    
    # Probability of landing heads
    p = alpha
    
    # Probability of observing the data given alpha
    likelihood = p**data * (1-p)**(n-data)
    
    return likelihood


def likelihood_ratio(alpha, alpha_hat, n, data):
    # alpha: true probability of landing heads
    # alpha_hat: estimated probability of landing heads
    # n: number of coin tosses
    # data: number of heads observed
    
    # Compute the likelihood of the null hypothesis (alpha=alpha_hat)
    null_likelihood = likelihood(alpha_hat, n, data) + 1e-10
    
    # Compute the likelihood of the alternative hypothesis (alpha=alpha)
    alt_likelihood = likelihood(alpha, n, data) + 1e-10
    
    # Compute the likelihood ratio statistic
    L = 2 * np.log(null_likelihood / alt_likelihood)
    
    return L

def estimate_alpha(n, data):
    # n: number of coin tosses
    # data: number of heads observed
    
    # Define the range of alpha values to consider
    alphas = np.linspace(0, 1, 1000)
    
    # Compute the likelihood of observing the data for each alpha
    likelihoods = [likelihood(alpha, n, data) for alpha in alphas]
    
    # Find the alpha value that maximizes the likelihood
    max_likelihood = max(likelihoods)
    index = likelihoods.index(max_likelihood)
    alpha_hat = alphas[index]
    
    return alpha_hat 

def confidence_interval(alpha_hat, n, data, alpha_level=0.05):
    # alpha_hat: estimated probability of landing heads
    # n: number of coin tosses
    # data: number of heads observed
    # alpha_level: significance level
    
    # Compute the likelihood ratio statistic for different values of alpha
    alphas = np.linspace(0, 1, 1000)
    L = [likelihood_ratio(alpha, alpha_hat, n, data) for alpha in alphas]
    
    # Find the critical value of the likelihood ratio statistic
    k = 1  # one parameter to estimate
    critical_value = np.quantile(np.random.chisquare(k), 1-alpha_level)
    
    # Find the confidence interval
    lower = alpha_hat - np.sqrt(critical_value / n)
    upper = alpha_hat + np.sqrt(critical_value / n)
    
    return lower, upper


# Simulate the coin toss experiment with alpha=0.7 and different numbers of tosses
n_list = [10, 20, 50, 100, 200, 500]
alpha = 0.7

# Estimate alpha and the confidence interval for each number of tosses
alpha_hats = []
CIs = []
for n in n_list:
    data = coin_toss(n, alpha)
    alpha_hat = estimate_alpha(n, data)
    lower, upper = confidence_interval(alpha_hat, n, data)
    alpha_hats.append(alpha_hat)
    CIs.append((lower, upper))
    
# Plot the estimated alpha and the confidence interval
plt.errorbar(n_list, alpha_hats, yerr=np.array(CIs).T, fmt='o')
plt.axhline(alpha, color='r', linestyle='--', label='True alpha')
plt.legend()
plt.xlabel('Number of tosses')
plt.ylabel('Estimated alpha')
plt.ylim([0, 1])
plt.show()





