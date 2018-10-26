import pandas as pd
from scipy import stats
from scipy.stats import chisquare
import scipy

from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.pyplot as plt

a=stats.chi2.cdf(2 , 2)
b=stats.chi2.cdf(4 , 2)
c=b-a
#print(a)
#print(b)
#print(c)
#-------------------------------------------------------------------------------
a= chisquare([795, 705], f_exp=[750, 750])
#print(a)
#---------------------------------------------------------------------------------
#Сопряженные таблицы:отклонить или принять нулевую гипотезу
from scipy.stats import chi2_contingency
from scipy.stats import chisquare

table = [[20,15],[11,12],[7,9]] #загружаем исходную табличку
chi2, prob, df, expected = scipy.stats.chi2_contingency(table) #рассчитываем параметры Хи-квадрат
#вывод:
output = "test Statistics: {}\ndegrees of freedom: {}\np-value: {}\n"
#print(output.format( chi2, df, prob))
#print(expected)
#------------------------------------------------------------------------------------
#Сопряженные таблицы: построить мозаичную таблицу
#воссоздадим таблицу (и подпишем строки и столбцы)
patients = pd.DataFrame({"Thrombosis": ["Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","No","No","No","No","No","No","No","No","No","No","No","No","No","No","No","No","No","No","No","No"], "Group": ["Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Placebo","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin","Aspirin"]})
#посмотрим на сводную таблицу пересечения признаков
print(pd.pivot_table(patients, index=["Group"], columns=["Thrombosis"], aggfunc=lambda x: len(x)))
#строим график
from statsmodels.graphics.mosaicplot import mosaic
import matplotlib.pyplot as plt
mosaic(patients, ["Thrombosis","Group"], gap=0.01)
plt.show()









