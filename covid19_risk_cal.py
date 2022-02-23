import pandas as pd

# covid19_risk_age_cal()
# input - age
# output - risk_age

def covid19_risk_age_cal(age):
    risk_age = 0
    if age >= 0 and age <= 17:
        risk_age = 0.09
    elif age >= 18 and age <= 29:
        risk_age = 0.239
    elif age >= 30 and age <= 39:
        risk_age = 0.165
    elif age >= 40 and age <= 49:
        risk_age = 0.152
    elif age >= 50 and age <= 64:
        risk_age = 0.205
    elif age >= 65 and age <= 74:
        risk_age = 0.076
    elif age >= 75 and age <= 84:
        risk_age = 0.043
    elif age >= 85:
        risk_age = 0.029
    else:
        print("not acceptable value, please try again")

    return risk_age

def covid19_risk_mask_cal(mask):
    risk_mask = 0
    if mask == 'Yes':
        risk_mask = 0.175
    elif mask == 'No':
        risk_mask = 0.825
    else:
        print("Please enter 'Yes' or 'No' ")

    return risk_mask

def covid19_risk_vaccination_cal(vaccination):
    risk_vaccination = 0
    if vaccination == 'Yes':
        risk_vaccination = 0.15
    elif vaccination == 'No':
        risk_vaccination = 0.85
    else:
        print("Please enter 'Yes' or 'No' ")
    
    return risk_vaccination

df = pd.read_csv("RiskCategoryforGeolocation.csv") 
def state_data(state_name):
    for i in range(len(df.State)):
        if state_name == df.State[i]:
            ratio = df.Ratio[i]
            return ratio                            

def covid19_risk_ratio_cal(ratio):
    risk_level = 0
    if ratio >= 0 and ratio <= 10:
        risk_level = 0.015
    elif ratio >= 11 and ratio <= 20:
        risk_level = 0.035
    elif ratio >= 21 and ratio <= 35:
        risk_level = 0.1
    elif ratio >= 36 and ratio <= 50:
        risk_level = 0.15
    elif ratio >= 51 and ratio <= 100:
        risk_level = 0.7
    else:
        print("invalid input value, please try again")
    return risk_level

def covid19_risk_geolocation_cal(geolocation):
    x = state_data(geolocation)
    risk_level = covid19_risk_ratio_cal(x)
    return risk_level


w0, w1, w2, w3 = (0.1,0.20,0.30,0.20)
def risk_cal(age, mask, vaccination, geolocation):
    risk_value_1 = covid19_risk_age_cal(age)
    risk_value_2 = covid19_risk_mask_cal(mask)
    risk_value_3 = covid19_risk_vaccination_cal(vaccination)
    risk_value_4 = covid19_risk_geolocation_cal(geolocation)
    risk_overall = (w0*risk_value_1+w1*risk_value_2+w2*risk_value_3+w3*risk_value_4)*100
    
    return risk_overall

