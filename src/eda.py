import click
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import os

@click.command()
@click.option("--input",
              default="data/processed/iris_clean.csv",
              help="Path to cleaned dataset.")
@click.option("--output-dir",
              default="results/figures",
              help="Directory to save EDA figures.")
def main(input, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load cleaned data
    df = pd.read_csv(input)

    # Scatter plot: Petal length vs Petal width by species
    print("Creating scatter plot...")
    scatter = alt.Chart(df).mark_circle(size=120).encode(
        x=alt.X("petal_length", title="Petal Length (cm)"),
        y=alt.Y("petal_width", title="Petal Width (cm)"),
        color=alt.Color("species", title="Species"),
        tooltip=["species", "petal_length", "petal_width"]
    ).properties(
        width=500,
        height=400,
        title="Petal Length vs Petal Width by Species"
    ).interactive()
    scatter_path = os.path.join(output_dir, "scatter_petal.png")
    scatter.save(scatter_path)
    print(f"Scatter plot saved to: {scatter_path}")

    # Boxplots
    print("Creating boxplots...")
    df_melt = df.melt(id_vars="species", var_name="feature", value_name="value")
    boxplot = alt.Chart(df_melt).mark_boxplot(size=40).encode(
        y=alt.Y("species:N", title="Species"),
        x=alt.X("value:Q", title="Measurement (cm)"),
        color=alt.Color("species:N", legend=None)
    ).properties(
        width=400,
        height=150
    ).facet(
        row=alt.Row("feature:N", title="Feature")
    )
    boxplot_path = os.path.join(output_dir, "boxplots.png")
    boxplot.save(boxplot_path)
    print(f"Boxplots saved to: {boxplot_path}")

    # Correlation heatmap
    print("Creating correlation heatmap...")
    corr = df.drop(columns="species").corr().stack().reset_index()
    corr.columns = ["feature1", "feature2", "correlation"]

    heatmap = alt.Chart(corr).mark_rect().encode(
        x=alt.X("feature1:N", title="Feature"),
        y=alt.Y("feature2:N", title="Feature"),
        color=alt.Color("correlation:Q", scale=alt.Scale(scheme="redblue"), title="Correlation")
    ).properties(
        width=300,
        height=300,
        title="Correlation Heatmap of Iris Features"
    )

    text = alt.Chart(corr).mark_text(size=14).encode(
        x="feature1:N",
        y="feature2:N",
        text=alt.Text("correlation:Q", format=".2f"),
        color=alt.condition(
            "datum.correlation > 0.5",
            alt.value("white"),
            alt.value("black")
        )
    )

    heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
    (heatmap + text).save(heatmap_path)
    print(f"Correlation heatmap saved to: {heatmap_path}")

if __name__ == "__main__":
    main()
