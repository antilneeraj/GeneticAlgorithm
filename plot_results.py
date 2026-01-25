import json
import matplotlib.pyplot as plt
import os

STATS_FILE = os.path.join("data", "statistics", "evolution_stats.json")
OUTPUT_IMAGE = os.path.join("data", "statistics", "training_results.png")

def plot_evolution_stats():
    if not os.path.exists(STATS_FILE):
        print(f"❌ Error: Could not find {STATS_FILE}. Run the AI training first!")
        return

    with open(STATS_FILE, "r") as f:
        data = json.load(f)

    generations = [g["generation"] for g in data["generation_statistics"]]
    best_fitness = [g["best_fitness"] for g in data["generation_statistics"]]
    avg_fitness = [g["average_fitness"] for g in data["generation_statistics"]]
    diversity = [g["diversity"] for g in data["generation_statistics"]]


    plt.style.use('ggplot') # or 'seaborn-darkgrid' if available
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), sharex=True)
    
    # --- Fitness Curves ---
    ax1.plot(generations, best_fitness, color="#2ecc71", linewidth=2, label="Best Fitness (Elite)")
    ax1.plot(generations, avg_fitness, color="#3498db", linewidth=2, linestyle="--", label="Average Population Fitness")
    
    ax1.set_ylabel("Fitness Score (Survival + Pipes)", fontsize=12)
    ax1.set_title("Evolutionary Learning Curve", fontsize=14, pad=15)
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.3)
    
    # Add annotation for the "Mastery" point
    max_fit = max(best_fitness)
    max_gen = generations[best_fitness.index(max_fit)]
    ax1.annotate(f'Peak Performance\n(Gen {max_gen}, Score {int(max_fit)})', 
                 xy=(max_gen, max_fit), 
                 xytext=(max_gen - 50, max_fit - 5000),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    # --- Genetic Diversity ---
    ax2.plot(generations, diversity, color="#e74c3c", linewidth=1.5, label="Genetic Diversity")
    ax2.fill_between(generations, diversity, color="#e74c3c", alpha=0.1)
    
    ax2.set_xlabel("Generation", fontsize=12)
    ax2.set_ylabel("Population Diversity (Std Dev)", fontsize=12)
    ax2.set_title("Genetic Diversity & Convergence", fontsize=14, pad=15)
    ax2.legend(loc="upper right")
    ax2.grid(True, alpha=0.3)

    # Save & Show
    plt.tight_layout()
    
    # Ensure assets folder exists
    os.makedirs(os.path.dirname(OUTPUT_IMAGE), exist_ok=True)
    
    plt.savefig(OUTPUT_IMAGE, dpi=300)
    print(f"✅ Graph saved successfully to: {OUTPUT_IMAGE}")
    print("   (Link this image in your README for maximum impact!)")

if __name__ == "__main__":
    plot_evolution_stats()