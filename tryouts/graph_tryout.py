import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


data2 = {'Year': [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010],
         'Unemployment_Rate': [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3],
         'my_var': [19.8, 22, 18, 17.2, 16.9, 17, 16.5, 16.2, 15.5, 16.3]
         }


df2 = DataFrame(data2, columns=['Year', 'Unemployment_Rate', 'my_var'])

root = tk.Tk()

figure2 = plt.Figure(figsize=(5, 4), dpi=100)
plt.style.use('seaborn')
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, root)
line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
'''
ax2.plot(data2['Year'], data2['Unemployment_Rate'])
ax2.plot(data2['Year'], data2['my_var'])
'''
df2 = df2[['Year', 'Unemployment_Rate', 'my_var']].groupby('Year').sum()

df2.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
ax2.set_title('Year Vs. Unemployment Rate')


root.mainloop()
