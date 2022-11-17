from random import uniform
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

passing_score = 0.5
curve = 0
report_card = pd.DataFrame(columns=["passing_score", "student", "years"])
year = 0
grade = 1

while passing_score < 1:
    for students in range(10):
        grade = 1
        while grade <= 12:
            score = uniform(curve, 1)
            if score > passing_score:
                grade += 1
                curve = score - 0.5
                year += 1
            elif score <= passing_score:
                year += 1
        x_df = pd.DataFrame({"passing_score": passing_score,
                             "student": students,
                             "years": year},
                             index=[0])
        report_card = pd.concat([report_card,x_df], ignore_index=True)
    passing_score += 0.1
report_card.to_csv("report_card.csv")