import pandas as pd
import plotly.express as px

df = pd.read_csv('/mnt/data/sqllab_query_mainsurvey_20251126T054812.csv')

figs = []

# Bar charts
figs.append(px.bar(df, x="Gender", title="Count by Gender"))
figs.append(px.bar(df, x="Business Type / Trade", title="Business Type Distribution"))
figs.append(px.bar(df, x="Location (Area in Vijayawada)", title="Location Distribution"))

# Histograms
figs.append(px.histogram(df, x="Age Group", title="Age Group Distribution"))
figs.append(px.histogram(df, x="Number of years in business", title="Experience Distribution"))

# Pie charts
figs.append(px.pie(df, names="Gender", title="Gender Split"))
figs.append(px.pie(df, names="Have you heard of the term “Trademark”?",
                   title="Trademark Awareness"))
figs.append(px.pie(df, names="Gender", hole=0.5, title="Gender Split (Donut)"))

# Box & Violin
col_rating = "Rate the importance of trademark awareness on a scale of 1–5"
if col_rating in df.columns:
    figs.append(px.box(df, y=col_rating, title="Importance Rating (Box Plot)"))
    figs.append(px.violin(df, y=col_rating, title="Importance Rating (Violin Plot)"))

# Treemap
figs.append(px.treemap(
    df,
    path=["Business Type / Trade", "Number of years in business"],
    title="Treemap: Business Type by Experience"
))

# Sunburst
figs.append(px.sunburst(
    df,
    path=["Gender", "Business Type / Trade", "Number of years in business"],
    title="Sunburst: Gender → Trade → Experience"
))

# Heatmap
pivot = pd.crosstab(df["Gender"], df["Business Type / Trade"])
figs.append(px.imshow(pivot, text_auto=True, title="Heatmap: Gender vs Business Type"))

# Scatter with category codes
df["GenderCode"] = df["Gender"].astype('category').cat.codes
df["BusinessCode"] = df["Business Type / Trade"].astype('category').cat.codes
figs.append(px.scatter(
    df,
    x="GenderCode",
    y="BusinessCode",
    color="Age Group",
    title="Scatter of Encoded Categories"
))

# Parallel categories
figs.append(px.parallel_categories(
    df[["Gender", "Age Group", "Business Type / Trade", "Location (Area in Vijayawada)"]],
    title="Parallel Categories"
))

# Show figures
for fig in figs:
    fig.show()
