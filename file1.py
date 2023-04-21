import numpy as np
from matplotlib import pyplot as plt
import sys
 
# if the user includes the flag -h or --help print the options
if '-h' in sys.argv or '--help' in sys.argv:
    print ("Usage: %s [-seed number],%s [-Alpha]" % sys.argv[0])
    print
    sys.exit(1)
    
class CoinFlips:
 
    def __init__(self, Alpha, seed=None):
        self.Alpha = Alpha
        self.seed = seed
        np.random.seed(seed)
 
    def Flip(self, N):
        # coin tosses simulator
        outcomes = np.random.binomial(N, self.Alpha)
 
        # Return the total number of heads observed
        Head = np.sum(outcomes)
    
        return Head
        
 
    def likelihood1(self, Alpha, N, data_observed):
        # Probability of getting heads is alpha
 
        # likelihood of observing the data given alpha
        likeli = (Alpha ** data_observed) * ((1 - Alpha) ** (N - data_observed))

 
        return likeli
 
    def Likeli_Ratio(self, Alpha, Alpha_hat, N, data_observed):
    # Calculate the probability of heads for both the null and alternative hypotheses
        p_null = alpha_hat
        p_alt = Alpha
    
    # Calculate the likelihood ratio statistic's numerator and denominator.
        numerator = (p_null ** data_observed) * ((1 - p_null) ** (N - data_observed))
        denominator = (p_alt ** data_observed) * ((1 - p_alt) ** (N - data_observed))
    
    # Check that denominator is non-zero before calculating L
        if denominator == 0:
            L = float('inf')
        else:
            L = 2 * np.log(numerator / denominator)
    
        return L

 
    def estimate_alpha(self, N, data_observed):
        # Make an array of 100 alpha values between 0 and 1
        alphas = np.linspace(0, 1, 100)
    
        # Calculate the likelihood of observing the data for each alpha value
        likelihoods = [self.likelihood1(Alpha, N, data_observed) for Alpha in alphas]
    
        # Determine the alpha value that maximizes likelihood
        max_likelihood_index = np.argmax(likelihoods)
        alpha_hat = alphas[max_likelihood_index]
        print(f"Estimated alpha for {N} tosses: {alpha_hat}")
        return alpha_hat

 
    def confidence_interval(self, alpha_hat, N, data_observed, alpha_level=0.05):
        # Calculate the likelihood ratio statistic for various values of alpha
        alphas = np.linspace(0, 1, 100)
        L = [self.Likeli_Ratio(Alpha, alpha_hat, N, data_observed) for Alpha in alphas]
 
        # Determine the likelihood ratio statistic's critical value.
        k = 1  # one parameter to estimate
        criticalValue = np.quantile(np.random.chisquare(k), 1 - alpha_level)
 
        # Compute the confidence interval
        mini = alpha_hat - np.sqrt(criticalValue / N)
        maxi = alpha_hat + np.sqrt(criticalValue / N)
 
        return mini, maxi
 
 
# Create a simulation of the coin flip experiment using alpha=0.65 and different numbers of flips
Nflips_list = [10,25,50,75, 100,500, 1000]
#Default alpha
Alpha = 0.65
#Default seed
seed=5555
# read the user-provided seed from the command line (if there)
if '-seed' in sys.argv:
    p = sys.argv.index('-seed')
    seed = int(sys.argv[p+1])

if '-Alpha' in sys.argv:
    p = sys.argv.index('-Alpha')
    alpha =int(sys.argv[p+1])

# Determine the confidence interval and alpha for each number of flips.
alpha_hats = []
CInterval = []

cf = CoinFlips(Alpha, seed)
for n in Nflips_list:
    data1 = cf.Flip(n)
    alpha_hat = cf.estimate_alpha(n, data1)
    mini, maxi = cf.confidence_interval(alpha_hat, n, data1)
    alpha_hats.append(alpha_hat)
    CInterval.append((mini, maxi))
 
# Save the results to a text file
with open('errbar.txt', 'w') as filex:
    for i, n in enumerate(Nflips_list):
        filex.write(f"{Nflips_list[i]} {alpha_hats[i]} {CInterval[i][0]} {CInterval[i][1]}\n")


# Create a figure showing the likelihood curves for different values of n
plt.figure(figsize=(8, 8))

# plot the likelihood curve for each n
for j, n in enumerate(Nflips_list):
    data1 = cf.Flip(n)
    alphas = np.linspace(0, 1, 100)
    likelihoods = [cf.likelihood1(Alpha, n, data1) for Alpha in alphas]
    plt.subplot( 3, 3,j+1)
    plt.plot(alphas, likelihoods, color='green')
    plt.axvline(alpha_hats[j], color='r', linestyle='--', label='Estimated alpha')
    plt.axvline(Alpha, color='k', linestyle='--', label='True alpha')
    plt.title(f'n = {n}')
    plt.xlabel('Probability of heads (alphas)')
    plt.ylabel('likelihood function')
    plt.legend()

plt.tight_layout()
plt.show()


