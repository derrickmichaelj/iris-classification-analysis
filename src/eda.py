import click
import pandas as pd
import altair as alt

@click.command()
@click.option("--input",
              default="data/processed/iris_processed.csv",
              help="Path to cleaned dataset.")
@click.option("--output-dir",
              default="results/figures",
              help="Directory to save figures.")
def main(input, output_dir):

    df = pd.read_csv(input)

    print("Creating scatter plot...")
    scatter = alt.Chart(df).mark_circle(size=120).encode(
        x="petal_length",
        y="petal_width",
        color="species",
        tooltip=["species", "petal_length", "petal_width"]
    ).properties(title="Petal Length vs Petal Width by Species")

    scatter.save(f"{output_dir}/scatter_petal.png")

    print("Creating boxplot grid...")
    melt = df.melt(id_vars="species",
                   var_name="feature",
                   value_name="value")

    boxplot = alt.Chart(melt).mark_boxplot(size=40).encode(
        y="species:N",
        x="value:Q",
        color="species:N"
    ).facet(row="feature:N")

    boxplot.save(f"{output_dir}/boxplots.png")

    print("Creating correlation heatmap...")
    corr = df.drop("species", axis=1).corr().stack().reset_index()
    corr.columns = ["feature1", "feature2", "correlation"]

    heatmap = alt.Chart(corr).mark_rect().encode(
        x="feature1",
        y="feature2",
        color="correlation:Q"
    )

    heatmap.save(f"{output_dir}/correlation_heatmap.png")

    print("EDA figures saved.")

if __name__ == "__main__":
    main()
