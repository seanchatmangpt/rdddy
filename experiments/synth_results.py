import numpy as np
import pandas as pd

# Define the number of synthetic samples
num_samples = 100

# Generate synthetic customer IDs
customer_ids = np.arange(1, num_samples + 1)

# Generate baseline satisfaction scores (before new design)
baseline_scores = np.random.randint(
    1, 6, num_samples
)  # Assuming a 5-point satisfaction scale

# Generate post-design satisfaction scores (after new design)
post_design_scores = np.random.randint(
    3, 6, num_samples
)  # Higher scores after the design change

# Create a DataFrame to store the synthetic results
synthetic_results = pd.DataFrame(
    {
        "Customer ID": customer_ids,
        "Baseline Satisfaction Score": baseline_scores,
        "Post-Design Satisfaction Score": post_design_scores,
    }
)

# Save the synthetic results to a CSV file
synthetic_results.to_csv("synthetic_experiment_results.csv", index=False)
