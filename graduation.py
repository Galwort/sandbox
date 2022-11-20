from random import uniform
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

passing_score = 50
curve = 0
report_card = pd.DataFrame(columns=["passing_score", "student", "years"])
year = 0
grade = 1
student = 1

while passing_score < 100:
    student = 1
    while student < 1000:
        grade = 1
        year = 0
        while grade <= 12:
            score = uniform(curve, 100)
            if score > passing_score:
                grade += 1
                curve = score - 10 * grade
                year += 1
            elif score <= passing_score:
                year += 1
        x_df = pd.DataFrame({"passing_score": passing_score,
                             "student": student,
                             "years": year},
                             index=[0])
        report_card = pd.concat([report_card,x_df], ignore_index=True)
        student += 1
    passing_score += 1

# report_card.to_csv("report_card.csv", index=False)

sns.set_style("whitegrid")
sns.set_context("poster")
sns.set_palette("Set2")
sns.set_color_codes("pastel")
sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.set(font_scale=1.5)
sns.set_style("ticks")
sns.set_style({"xtick.direction": "in","ytick.direction": "in"})
sns.set_style({"xtick.major.size": 8, "ytick.major.size": 8})
sns.set_style({"xtick.minor.size": 4, "ytick.minor.size": 4})

sns_plot = sns.boxplot(x="passing_score", y="years", data=report_card)
sns_plot.set(xlabel='Passing Score', ylabel='Years to Graduate')
sns_plot.figure.savefig("graduation.png")
