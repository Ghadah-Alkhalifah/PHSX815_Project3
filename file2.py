
import numpy as np
import matplotlib.pyplot as plt

# Read the data from the text file
data = np.loadtxt('errbar.txt')

# Extract the number of flips, estimated alphas, and confidence intervals
Nflips_list = data[:, 0].astype(int)
alpha_hats = data[:, 1]
mini_CIs = data[:, 2]
maxi_CIs = data[:, 3]

# Plot the estimated alpha and the confidence interval
plt.errorbar(Nflips_list, alpha_hats, yerr=[alpha_hats - mini_CIs, maxi_CIs - alpha_hats], fmt='o', color='green')
plt.axhline(0.65, color='r', linestyle='--', label='True alpha')
plt.legend()
plt.xlabel('Number of flips')
plt.ylabel('Estimated probability of heads(alpha)')
plt.ylim([0, 1])
plt.show()





