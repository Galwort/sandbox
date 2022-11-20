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
                curve = score - 50 #* grade
                year += 1
            elif score <= passing_score:
                year += 1
        x_df = pd.DataFrame({"passing_score": passing_score,
                             "student": student,
                             "years": year},
                             index=[0])
        report_card = pd.concat([report_card,x_df], ignore_index=True)
        student += 1
    passing_score += 10

sns_plot = sns.boxplot(x="passing_score", y="years", data=report_card)
sns_plot.set(xlabel='Passing Score', ylabel='Years to Graduate')
sns_plot.figure.savefig("graduation.png")
