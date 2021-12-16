# Twitter Analysis of COVID-19 Discussions

This repository contains the code and report for a project aimed at making sense of discussions regarding COVID-19 on Twitter.

## Usage
Follow the steps in the sections below to conduct the experiments as described in the report with your own tweet data. Alternatively, see the [Generate Analytical Information](https://github.com/aaronlohner/comp598-project#generate-analytical-information) section below to use the data provided.

### Obtain New Tweets
1. Create a [Twitter Developer Account](https://developer.twitter.com/en) with elevated access.
2. Populate the necessary fields from your Twitter account in `config.json`.
3. Execute `collect.py` (run `collect.py --help` for more information).

### Annotate Tweets
1. Export the generated CSV file to an Excel file.
2. Create two new columns at the right end of the table.
3. Annotate the tweets, indicating their category (1-5) in the first new column and their sentiment in the second new column (`g` for positive, `b` for negative, `n` for neutral). See the report for details on the category designations and see `tweets3_excel.xlsx` for an example (some tweets may be skipped while annotating).

### Generate Analytical Information
1. Replace the filename on line 20 in `annotated_tweet_handler.py` with the annotated file.
2. Execute `annotated_tweet_handler.py` (interactively or via command line).