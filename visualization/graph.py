import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_optimization_history(history, results_path):
    plt.figure(figsize=(10, 6))
    plt.plot(history, color='#2ca02c', linewidth=2.5, label='Fitness Convergence')
    plt.title('Optimization Fitness Score Over Generations (5-Variables GA)', fontsize=13, fontweight='bold')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Score')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    os.makedirs(results_path, exist_ok=True)
    plt.savefig(os.path.join(results_path, 'optimization_history.png'), dpi=300)
    plt.close()

def plot_optimal_ratios(ratios, results_path):
    labels = list(ratios.keys())
    sizes = [val * 100 for val in ratios.values()]
    colors = ['#ff7f0e', '#1f77b4', '#2ca02c']
    
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
            textprops={'fontsize': 12, 'fontweight': 'bold'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2.5})
    plt.title('Optimal Vehicle Composition Ratio (Yangsan)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    os.makedirs(results_path, exist_ok=True)
    plt.savefig(os.path.join(results_path, 'optimal_vehicle_ratios.png'), dpi=300)
    plt.close()
