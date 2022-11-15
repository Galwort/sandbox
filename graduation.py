from random import uniform
import seaborn as sns

grade = 1
passing_score = 0.5
score = 0
curve = 0
year = 0


while passing_score < 1:
    for x in range(1000):
        while grade <= 12:
            score = uniform(curve, 1)
            if score > passing_score:
                grade += 1
                curve = score - 0.5
                year += 1
            elif score <= passing_score:
                year += 1