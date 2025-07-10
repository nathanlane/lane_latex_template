#!/usr/bin/env python3
"""
example_analysis.py - Template for data analysis following CLAUDE.md guidelines

This script demonstrates:
- PEP 8 compliant code (use black formatter)
- seaborn-v0_8-paper style for publication-quality plots
- Colorblind-friendly palettes (viridis)
- High-resolution output (1500 DPI)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Tuple, Optional

# Configure plotting defaults
plt.style.use("seaborn-v0_8-paper")
sns.set_palette("viridis")

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
FIGURES_DIR = PROJECT_ROOT / "figures"

# Ensure output directory exists
FIGURES_DIR.mkdir(exist_ok=True)


def load_data(filename: str) -> pd.DataFrame:
    """
    Load data from the processed data directory.
    
    Parameters
    ----------
    filename : str
        Name of the data file to load
        
    Returns
    -------
    pd.DataFrame
        Loaded data
    """
    filepath = DATA_DIR / "processed" / filename
    
    if not filepath.exists():
        # Create example data for demonstration
        print(f"Creating example data (file not found: {filepath})")
        return create_example_data()
    
    return pd.read_csv(filepath)


def create_example_data() -> pd.DataFrame:
    """Create example data for demonstration purposes."""
    np.random.seed(42)
    
    n_countries = 6
    years = range(1960, 2001)
    
    # Simulate GDP growth data for East Asian countries
    countries = ["Japan", "South Korea", "Taiwan", "Singapore", "Hong Kong", "Malaysia"]
    
    data = []
    for country in countries:
        # Different growth trajectories
        base_growth = np.random.uniform(0.03, 0.06)
        volatility = np.random.uniform(0.01, 0.02)
        
        for year in years:
            growth_rate = base_growth + np.random.normal(0, volatility)
            # Add country-specific patterns
            if country in ["Japan"] and year > 1990:
                growth_rate *= 0.3  # Lost decade
            elif country in ["South Korea", "Taiwan"] and year > 1985:
                growth_rate *= 1.5  # Rapid industrialization
                
            data.append({
                "country": country,
                "year": year,
                "gdp_growth": growth_rate * 100,  # Convert to percentage
                "gdp_per_capita": 1000 * (1 + growth_rate) ** (year - 1960)
            })
    
    return pd.DataFrame(data)


def create_growth_comparison_plot(
    data: pd.DataFrame,
    figsize: Tuple[float, float] = (10, 6)
) -> plt.Figure:
    """
    Create a comparison plot of GDP growth rates.
    
    Parameters
    ----------
    data : pd.DataFrame
        Data containing growth rates
    figsize : tuple
        Figure size in inches
        
    Returns
    -------
    plt.Figure
        The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot each country's growth trajectory
    for country in data["country"].unique():
        country_data = data[data["country"] == country]
        ax.plot(
            country_data["year"],
            country_data["gdp_growth"].rolling(window=3).mean(),  # 3-year moving average
            label=country,
            linewidth=2,
            alpha=0.8
        )
    
    # Formatting
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("GDP Growth Rate (%, 3-year MA)", fontsize=12)
    ax.set_title("East Asian Economic Growth Trajectories", fontsize=14, pad=20)
    ax.legend(loc="best", frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(data["year"].min(), data["year"].max())
    
    # Add annotation for Asian Financial Crisis
    ax.axvline(x=1997, color="red", linestyle="--", alpha=0.5)
    ax.text(1997.5, ax.get_ylim()[1] * 0.9, "Asian\nFinancial\nCrisis",
            fontsize=10, ha="left", va="top", color="red", alpha=0.7)
    
    plt.tight_layout()
    return fig


def create_gdp_per_capita_plot(
    data: pd.DataFrame,
    figsize: Tuple[float, float] = (10, 6)
) -> plt.Figure:
    """
    Create a plot showing GDP per capita evolution.
    
    Parameters
    ----------
    data : pd.DataFrame
        Data containing GDP per capita
    figsize : tuple
        Figure size in inches
        
    Returns
    -------
    plt.Figure
        The created figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Use seaborn for better styling
    pivot_data = data.pivot(index="year", columns="country", values="gdp_per_capita")
    
    # Plot with log scale for better visualization
    for country in pivot_data.columns:
        ax.semilogy(pivot_data.index, pivot_data[country], 
                   label=country, linewidth=2.5, marker="o", markersize=3,
                   markevery=5)  # Markers every 5 years
    
    # Formatting
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("GDP per Capita (USD, log scale)", fontsize=12)
    ax.set_title("Convergence in East Asian Economies", fontsize=14, pad=20)
    ax.legend(loc="lower right", frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.3, which="both")
    ax.set_xlim(data["year"].min(), data["year"].max())
    
    plt.tight_layout()
    return fig


def save_figure(fig: plt.Figure, filename: str, dpi: int = 1500) -> None:
    """
    Save figure in both PNG and PDF formats.
    
    Parameters
    ----------
    fig : plt.Figure
        Figure to save
    filename : str
        Base filename (without extension)
    dpi : int
        Resolution for PNG output
    """
    # Save as high-resolution PNG
    png_path = FIGURES_DIR / f"{filename}.png"
    fig.savefig(png_path, dpi=dpi, bbox_inches="tight")
    print(f"Saved: {png_path}")
    
    # Save as PDF for LaTeX inclusion
    pdf_path = FIGURES_DIR / f"{filename}.pdf"
    fig.savefig(pdf_path, bbox_inches="tight")
    print(f"Saved: {pdf_path}")


def main():
    """Main analysis workflow."""
    print("Running East Asian Miracle analysis...")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Figures will be saved to: {FIGURES_DIR}")
    
    # Load or create data
    data = load_data("east_asia_gdp.csv")
    print(f"\nData shape: {data.shape}")
    print(f"Countries: {', '.join(data['country'].unique())}")
    print(f"Years: {data['year'].min()}-{data['year'].max()}")
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    # 1. Growth rate comparison
    fig1 = create_growth_comparison_plot(data)
    save_figure(fig1, "gdp_growth_comparison")
    plt.close(fig1)
    
    # 2. GDP per capita evolution
    fig2 = create_gdp_per_capita_plot(data)
    save_figure(fig2, "gdp_per_capita_evolution")
    plt.close(fig2)
    
    # Summary statistics
    print("\nSummary Statistics:")
    summary = data.groupby("country")["gdp_growth"].agg(["mean", "std", "min", "max"])
    print(summary.round(2))
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()