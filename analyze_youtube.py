import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import isodate

# 1. LOAD DATA
try:
    df = pd.read_csv('youtube_data.csv')
except FileNotFoundError:
    print("Error: Run the extractor script first!")
    exit()

# 2. FEATURE ENGINEERING
def parse_duration(duration_iso):
    try:
        dur = isodate.parse_duration(duration_iso)
        return dur.total_seconds() / 60
    except:
        return 0

df['Duration_Minutes'] = df['Duration_ISO'].apply(parse_duration)
df['Engagement_Rate'] = ((df['Likes'] + df['Comments']) / df['Views']) * 100
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['Short_Title'] = df['Title'].apply(lambda x: x[:35] + '...' if len(x) > 35 else x)

# 3. BUILD DASHBOARD (Dark Mode)
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "📈 Views Trend (Last 50 Videos)", 
        "🎯 Strategy: Duration vs Views (Color = Engagement)", 
        "🏆 Top 5 Most Viewed Videos", 
        "🔥 Correlation Matrix"
    ),
    vertical_spacing=0.15,
    horizontal_spacing=0.1,
    specs=[[{"type": "scatter"}, {"type": "scatter"}],
           [{"type": "bar"}, {"type": "heatmap"}]]
)

# Chart 1: Time Series (Neon Cyan Line)
df_sorted = df.sort_values('Date')
fig.add_trace(
    go.Scatter(
        x=df_sorted['Date'], 
        y=df_sorted['Views'], 
        mode='lines+markers', 
        name='Views', 
        line=dict(color='#00FFFF', width=3), # Neon Cyan
        marker=dict(size=6, color='white')
    ),
    row=1, col=1
)

# Chart 2: Duration vs Views
fig.add_trace(
    go.Scatter(
        x=df['Duration_Minutes'], 
        y=df['Views'], 
        mode='markers',
        marker=dict(
            size=df['Likes'], 
            sizemode='area', 
            sizeref=2.*max(df['Likes'])/(50.**2), 
            sizemin=6,
            color=df['Engagement_Rate'], 
            colorscale='Turbo', # Vibrant Rainbow
            showscale=True, 
            colorbar=dict(title="Eng. Rate %", len=0.4, y=0.8, tickfont=dict(color='white')),
            line=dict(width=1, color='white') # White border around dots
        ),
        text=df['Title'], 
        name='Video'
    ),
    row=1, col=2
)

# Chart 3: Leaderboard (FIXED COLORSCALE HERE)
top_videos = df.sort_values(by='Views', ascending=True).tail(5) 
fig.add_trace(
    go.Bar(
        y=top_videos['Short_Title'], 
        x=top_videos['Views'], 
        orientation='h',
        text=top_videos['Views'], 
        textposition='auto',
        # --- THE FIX: Changed 'Cool' (Invalid) to 'Ice' (Valid) ---
        marker=dict(color=top_videos['Views'], colorscale='Ice'), 
        name='Top Videos'
    ),
    row=2, col=1
)

# Chart 4: Correlation Heatmap
corr = df[['Views', 'Likes', 'Comments', 'Duration_Minutes', 'Engagement_Rate']].corr()
fig.add_trace(
    go.Heatmap(
        z=corr.values, 
        x=corr.columns, 
        y=corr.columns,
        colorscale='RdBu_r', 
        zmin=-1, zmax=1, 
        text=corr.values.round(2), 
        texttemplate="%{text}",
        name='Correlation'
    ),
    row=2, col=2
)

# 4. FINAL LAYOUT (Dark Theme Settings)
fig.update_layout(
    title_text="<b>🚀 YouTube Content Strategy Dashboard</b>",
    title_font_size=24,
    title_x=0.5,
    height=900, 
    width=1400,
    showlegend=False,
    template="plotly_dark", # DARK MODE
    paper_bgcolor='#111111', # Very Dark Grey Background
    plot_bgcolor='#111111',
    margin=dict(l=50, r=50, t=100, b=50)
)

# Update Font Colors to White
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#333333', tickfont=dict(color='white'))
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333333', tickfont=dict(color='white'), tickformat=",d")
fig.update_xaxes(tickformat=",d", row=1, col=2)
fig.update_xaxes(tickformat=",d", row=2, col=1)

fig.write_html("youtube_dashboard_dark_v2.html")
print("SUCCESS! Fixed colors. Open 'youtube_dashboard_dark_v2.html'")
