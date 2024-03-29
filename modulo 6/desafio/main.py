#!/usr/bin/env python
# coding: utf-8

# # Desafio 5
# 
# Neste desafio, vamos praticar sobre redução de dimensionalidade com PCA e seleção de variáveis com RFE. Utilizaremos o _data set_ [Fifa 2019](https://www.kaggle.com/karangadiya/fifa19), contendo originalmente 89 variáveis de mais de 18 mil jogadores do _game_ FIFA 2019.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Setup_ geral

# In[2]:


from math import sqrt

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sct
import seaborn as sns
import statsmodels.api as sm
import statsmodels.stats as st
from sklearn.decomposition import PCA

from loguru import logger


# In[3]:


# Algumas configurações para o matplotlib.
#%matplotlib inline

from IPython.core.pylabtools import figsize


figsize(12, 8)

sns.set()


# In[4]:


fifa = pd.read_csv("fifa.csv")


# In[5]:


columns_to_drop = ["Unnamed: 0", "ID", "Name", "Photo", "Nationality", "Flag",
                   "Club", "Club Logo", "Value", "Wage", "Special", "Preferred Foot",
                   "International Reputation", "Weak Foot", "Skill Moves", "Work Rate",
                   "Body Type", "Real Face", "Position", "Jersey Number", "Joined",
                   "Loaned From", "Contract Valid Until", "Height", "Weight", "LS",
                   "ST", "RS", "LW", "LF", "CF", "RF", "RW", "LAM", "CAM", "RAM", "LM",
                   "LCM", "CM", "RCM", "RM", "LWB", "LDM", "CDM", "RDM", "RWB", "LB", "LCB",
                   "CB", "RCB", "RB", "Release Clause"
]

try:
    fifa.drop(columns_to_drop, axis=1, inplace=True)
except KeyError:
    logger.warning(f"Columns already dropped")


# ## Inicia sua análise a partir daqui

# In[7]:


pd.options.display.max_columns = None


# In[8]:


fifa.head()


# In[9]:


fifa.describe().T


# In[24]:


fifa.isna().sum()


# In[29]:


fifa.dropna(inplace=True)


# In[113]:


def pca(datas, **kwargs):
    return PCA(**kwargs).fit(datas)


# ## Questão 1
# 
# Qual fração da variância consegue ser explicada pelo primeiro componente principal de `fifa`? Responda como um único float (entre 0 e 1) arredondado para três casas decimais.

# In[114]:


def q1():
    fit_pca = pca(fifa, n_components=1)
    fit_pca.transform(fifa)
    variance = fit_pca.explained_variance_ratio_[0]
    return float(np.round(variance, 3))
q1()


# ## Questão 2
# 
# Quantos componentes principais precisamos para explicar 95% da variância total? Responda como un único escalar inteiro.

# In[98]:


fit_pca = pca(fifa, n_components=.95)
evr = fit_pca.explained_variance_ratio_


# In[99]:


plot = sns.lineplot(np.arange(len(evr)), np.cumsum(evr))
plot.axes.axhline(.95, ls='--', color='#000000')
plt.xlabel('Número de componentes')
plt.ylabel('Variância explicada acumulativa')
#plt.show()


# In[127]:


def q2():
    fit_pca = pca(fifa, n_components=.95)    
    return len(fit_pca.components_)
q2()


# ## Questão 3
# 
# Qual são as coordenadas (primeiro e segundo componentes principais) do ponto `x` abaixo? O vetor abaixo já está centralizado. Cuidado para __não__ centralizar o vetor novamente (por exemplo, invocando `PCA.transform()` nele). Responda como uma tupla de float arredondados para três casas decimais.

# In[76]:


x = [0.87747123,  -1.24990363,  -1.3191255, -36.7341814,
     -35.55091139, -37.29814417, -28.68671182, -30.90902583,
     -42.37100061, -32.17082438, -28.86315326, -22.71193348,
     -38.36945867, -20.61407566, -22.72696734, -25.50360703,
     2.16339005, -27.96657305, -33.46004736,  -5.08943224,
     -30.21994603,   3.68803348, -36.10997302, -30.86899058,
     -22.69827634, -37.95847789, -22.40090313, -30.54859849,
     -26.64827358, -19.28162344, -34.69783578, -34.6614351,
     48.38377664,  47.60840355,  45.76793876,  44.61110193,
     49.28911284
]


# In[144]:


def q3():
    pca_component_1 = pca(fifa, n_components=2)
    coors = np.dot(pca_component_1.components_, x).round(3).reshape(1, -1)[0]
    
    return coors[0], coors[1]
    
q3()


# ## Questão 4
# 
# Realiza RFE com estimador de regressão linear para selecionar cinco variáveis, eliminando uma a uma. Quais são as variáveis selecionadas? Responda como uma lista de nomes de variáveis.

# In[145]:


from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE


# In[146]:


regressor = LinearRegression()


# In[155]:


X = fifa.drop('Overall', axis=1)
y = fifa['Overall']


# In[156]:


rfe = RFE(regressor, n_features_to_select=5)
rfe.fit(X, y)


# In[184]:


rfe.get_support()


# In[185]:


X.columns[rfe.get_support()]


# In[183]:


def q4():
    return list(X.columns[rfe.get_support()])
q4()

