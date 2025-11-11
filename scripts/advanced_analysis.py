import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from python_sql_queries import TorontoParkingDB
import os

# Set style for better-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)

# Ensure output directories exist
os.makedirs('visuals', exist_ok=True)
os.makedirs('sql_outputs', exist_ok=True)

# ============================================
# CHART 1: Top 15 Infraction Types
# ============================================

def create_chart1_top_infractions():
    """Chart 1: Top 15 Infraction Types - Horizontal Bar Chart"""
    print("📊 Creating Chart 1: Top Infractions...")
    
    db = TorontoParkingDB(password='1234567890')
    db.connect()
    df = db.get_top_infractions(limit=15)
    db.disconnect()
    
    if df is None or len(df) == 0:
        print("❌ No data for Chart 1")
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Sort by count for better visualization
    df = df.sort_values('count', ascending=True)
    
    # Create horizontal bar chart
    ax.barh(df['infraction_description'], df['count'], color='steelblue')
    ax.set_xlabel('Number of Tickets', fontsize=12, fontweight='bold')
    ax.set_ylabel('Infraction Type', fontsize=12, fontweight='bold')
    ax.set_title('Top 15 Most Common Parking Infractions in Toronto', fontsize=14, fontweight='bold')
    
    # Add value labels on bars
    for i, v in enumerate(df['count']):
        ax.text(v + 200, i, str(int(v)), va='center')
    
    plt.tight_layout()
    plt.savefig('visuals/chart1_top_infractions.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 1 saved: chart1_top_infractions.png")
    plt.close()


# ============================================
# CHART 2: Fine Amount Distribution (Pie Chart)
# ============================================

def create_chart2_fine_distribution():
    """Chart 2: Fine Amount Distribution - Pie Chart"""
    print("📊 Creating Chart 2: Fine Distribution...")
    
    db = TorontoParkingDB(password='1234567890')
    db.connect()
    df = db.get_fine_distribution()
    db.disconnect()
    
    if df is None or len(df) == 0:
        print("❌ No data for Chart 2")
        return
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Define colors
    colors = ['#2ecc71', '#f39c12', '#e74c3c', '#c0392b', '#8B0000']
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        df['count'], 
        labels=df['fine_range'], 
        autopct='%1.1f%%',
        colors=colors[:len(df)],
        startangle=90,
        textprops={'fontsize': 11}
    )
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Distribution of Parking Fine Amounts', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('visuals/chart2_fine_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 2 saved: chart2_fine_distribution.png")
    plt.close()


# ============================================
# CHART 3: Monthly Trend (Line Chart)
# ============================================

def create_chart3_temporal_trend():
    """Chart 3: Monthly Trend - Line Chart"""
    print("📊 Creating Chart 3: Temporal Trend...")
    
    db = TorontoParkingDB(password='1234567890')
    db.connect()
    df = db.get_by_date()
    db.disconnect()
    
    if df is None or len(df) == 0:
        print("❌ No data for Chart 3")
        return
    
    # Convert to datetime and group by month
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['count'].sum().reset_index()
    monthly['month'] = monthly['month'].astype(str)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Create line chart
    ax.plot(monthly['month'], monthly['count'], 
            marker='o', linewidth=2.5, markersize=8, 
            color='#3498db', label='Tickets per Month')
    
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Tickets', fontsize=12, fontweight='bold')
    ax.set_title('Parking Tickets Trend Over Time (Monthly)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('visuals/chart3_temporal_trend.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 3 saved: chart3_temporal_trend.png")
    plt.close()


# ============================================
# CHART 4: Average Fine by Infraction (Horizontal Bar)
# ============================================

def create_chart4_avg_fine_by_infraction():
    """Chart 4: Average Fine Amount by Infraction - Horizontal Bar Chart"""
    print("📊 Creating Chart 4: Average Fine by Infraction...")
    
    db = TorontoParkingDB(password='1234567890')
    db.connect()
    df = db.get_top_infractions(limit=15)
    db.disconnect()
    
    if df is None or len(df) == 0:
        print("❌ No data for Chart 4")
        return
    
    # Sort by average fine
    df = df.sort_values('avg_fine', ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Use color gradient based on fine amount
    colors = plt.cm.RdYlGn_r(df['avg_fine'] / df['avg_fine'].max())
    ax.barh(df['infraction_description'], df['avg_fine'], color=colors)
    
    ax.set_xlabel('Average Fine Amount ($)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Infraction Type', fontsize=12, fontweight='bold')
    ax.set_title('Average Fine Amount by Infraction Type (Top 15)', fontsize=14, fontweight='bold')
    
    # Add value labels on bars
    for i, v in enumerate(df['avg_fine']):
        ax.text(v + 2, i, f'${v:.2f}', va='center')
    
    plt.tight_layout()
    plt.savefig('visuals/chart4_avg_fine_by_infraction.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 4 saved: chart4_avg_fine_by_infraction.png")
    plt.close()


# ============================================
# CHART 5: Day of Week Analysis (Bar Chart)
# ============================================

def create_chart5_day_of_week():
    """Chart 5: Day of Week Analysis - Bar Chart"""
    print("📊 Creating Chart 5: Day of Week Analysis...")
    
    db = TorontoParkingDB(password='1234567890')
    db.connect()
    
    # Custom query for day of week
    query = """
    SELECT 
        DAYNAME(date_of_infraction) as day_of_week,
        COUNT(*) as ticket_count,
        ROUND(AVG(set_fine_amount), 2) as avg_fine
    FROM parking_tickets
    WHERE date_of_infraction IS NOT NULL
    GROUP BY DAYNAME(date_of_infraction), DAYOFWEEK(date_of_infraction)
    ORDER BY DAYOFWEEK(date_of_infraction)
    """
    
    df = db.query_to_dataframe(query)
    db.disconnect()
    
    if df is None or len(df) == 0:
        print("❌ No data for Chart 5")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create bar chart
    bars = ax.bar(df['day_of_week'], df['ticket_count'], color='coral', edgecolor='darkred', linewidth=1.5)
    
    ax.set_xlabel('Day of Week', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Tickets', fontsize=12, fontweight='bold')
    ax.set_title('Parking Tickets by Day of Week', fontsize=14, fontweight='bold')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('visuals/chart5_day_of_week.png', dpi=300, bbox_inches='tight')
    print("✓ Chart 5 saved: chart5_day_of_week.png")
    plt.close()


# ============================================
# SUMMARY STATISTICS
# ============================================

def create_summary_stats():
    """Generate and save summary statistics to text file"""
    print("📄 Creating Summary Statistics...")
    
    db = TorontoParkingDB(password='1234567890')
    db.connect()
    
    stats = db.get_summary_stats()
    db.disconnect()
    
    if stats is None or len(stats) == 0:
        print("❌ No data for summary statistics")
        return
    
    # Save as text file
    with open('sql_outputs/summary_statistics.txt', 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("TORONTO PARKING ANALYSIS - SUMMARY STATISTICS\n")
        f.write("=" * 60 + "\n\n")
        f.write(stats.to_string(index=False))
        f.write("\n\n" + "=" * 60 + "\n")
    
    print("✓ Summary statistics saved: sql_outputs/summary_statistics.txt")
    print(f"\n{stats.to_string(index=False)}\n")


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("🚗 Toronto Parking Analysis - Advanced Analysis\n")
    print("=" * 60)
    
    try:
        # Create summary stats first
        create_summary_stats()
        
        # Create all 5 charts
        print("\n📊 Creating visualizations...\n")
        create_chart1_top_infractions()
        create_chart2_fine_distribution()
        create_chart3_temporal_trend()
        create_chart4_avg_fine_by_infraction()
        create_chart5_day_of_week()
        
        print("\n" + "=" * 60)
        print("✅ All analysis complete!")
        print("📁 Check 'visuals/' folder for charts")
        print("📄 Check 'sql_outputs/' folder for statistics")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()