import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_plots():
    """
    Reads the benchmark_results.csv file and generates two professional
    academic plots (Average Code Length and Compression Ratio).
    Saves the plots as high-resolution PNG files in the 'figures' directory.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, "results")
    figures_dir = os.path.join(base_dir, "figures")
    csv_path = os.path.join(results_dir, "benchmark_results.csv")
    
    # Ensure the figures directory exists
    os.makedirs(figures_dir, exist_ok=True)
    
    # Load data
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}. Please run benchmark.py first.")
        return

    # Set the visual style for academic plots
    sns.set_theme(style="whitegrid", palette="muted")
    
    # ==========================================
    # Plot 1: Average Code Length Comparison
    # ==========================================
    plt.figure(figsize=(10, 6))
    
    # Melt dataframe for seaborn grouped bar chart
    df_L = df.melt(id_vars="File_Name", 
                   value_vars=["Shannon_H", "Huffman_L", "LZW_L"],
                   var_name="Metric", 
                   value_name="Bits_per_Symbol")
    
    # Rename metrics for better legend readability
    df_L['Metric'] = df_L['Metric'].replace({
        'Shannon_H': 'Shannon Entropy (H)',
        'Huffman_L': 'Huffman Length (L)',
        'LZW_L': 'LZW Length (L)'
    })
    
    ax1 = sns.barplot(x="File_Name", y="Bits_per_Symbol", hue="Metric", data=df_L)
    
    # Add a horizontal dashed line representing the uncompressed baseline (8 bits/byte)
    plt.axhline(y=8, color='red', linestyle='--', linewidth=1.5, label='Uncompressed (8 bits)')
    
    plt.title("Empirical Average Code Length vs. Shannon Entropy", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Test Files", fontsize=12)
    plt.ylabel("Average Bits per Symbol", fontsize=12)
    plt.legend(title="Metrics", loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    
    plot1_path = os.path.join(figures_dir, "code_length_comparison.png")
    plt.savefig(plot1_path, dpi=300, bbox_inches='tight')
    print(f"[SUCCESS] Saved Code Length plot to: {plot1_path}")
    plt.close()

    # ==========================================
    # Plot 2: Compression Ratio Comparison
    # ==========================================
    plt.figure(figsize=(10, 6))
    
    df_CR = df.melt(id_vars="File_Name", 
                    value_vars=["Huffman_CR", "LZW_CR"],
                    var_name="Algorithm", 
                    value_name="Compression_Ratio")
    
    df_CR['Algorithm'] = df_CR['Algorithm'].replace({
        'Huffman_CR': 'Huffman',
        'LZW_CR': 'LZW'
    })
    
    ax2 = sns.barplot(x="File_Name", y="Compression_Ratio", hue="Algorithm", data=df_CR)
    
    # Add a horizontal dashed line representing CR = 1 (No compression limit)
    plt.axhline(y=1, color='red', linestyle='--', linewidth=1.5, label='CR = 1.0 (No Compression)')
    
    plt.title("Compression Ratio (CR) Comparison", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Test Files", fontsize=12)
    plt.ylabel("Compression Ratio (Larger is Better)", fontsize=12)
    plt.legend(title="Algorithm", loc="upper right")
    plt.tight_layout()
    
    plot2_path = os.path.join(figures_dir, "compression_ratio_comparison.png")
    plt.savefig(plot2_path, dpi=300, bbox_inches='tight')
    print(f"[SUCCESS] Saved Compression Ratio plot to: {plot2_path}")
    plt.close()

if __name__ == "__main__":
    generate_plots()