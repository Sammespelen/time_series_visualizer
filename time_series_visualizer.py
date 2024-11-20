import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True, index_col=[0])

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(18, 6))
    
    # Plot the data
    ax.plot(df.index, df['value'], color='red', linewidth=1.5)
    
    # Set the title and labels
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontsize=14)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Page Views", fontsize=12)
    
    # Improve the appearance of the x-axis ticks
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Year'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.month
    
    df_monthly_avg = df_bar.groupby(['Year', 'Month'])['value'].mean().unstack(level=1)
 
    # Create a mapping for month numbers to month names
    month_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    # Replace month numbers (1-12) with month names
    df_monthly_avg.columns = df_monthly_avg.columns.map(month_map)

    # Plot the bar chart
    fig, ax = plt.subplots(figsize=(10, 10))
    df_monthly_avg.plot(kind='bar', ax=ax, width=0.8, colormap='tab10')

    ax.set_title("Average Daily Page Views per Month", fontsize=16)
    ax.set_xlabel("Years", fontsize=14)
    ax.set_ylabel("Average Page Views", fontsize=14)

    ax.legend(title="Months", title_fontsize='13', fontsize='11', loc='center left', bbox_to_anchor=(0, 0.75))

    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # views per year
    sns.boxplot(data=df_box, x='year', y='value', ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # views per month
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    sns.boxplot(data=df_box, x='month', y='value', ax=axes[1], order=month_order)
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig