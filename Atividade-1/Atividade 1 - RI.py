
# coding: utf-8

# In[162]:


import nltk
import pandas as pd
import io
import requests


# In[163]:


AND = 1
OR = 2


# In[164]:


# Download o dado CSV
def download_csv():
    r = requests.get('https://drive.google.com/a/ccc.ufcg.edu.br/uc?authuser=0&id=1YqUakSw2BLj-Hgz_oPntvHWwK6vKxjOb&output=csv')
    data = r.content
    return data


# In[165]:


#Formata o CSV como um Data Frame 
# Contéudo do DF:
# titulo: Titulo da Noticia
# conteudo: Contéudo da Noticia
# idNoticia: Id da noticia
# content: O titulo + ' ' conteudo (Concatenção do titulo e do conteudo separado por um ' ') 
def getCSVFormattedAsDF():
    data = download_csv()
    df = pd.read_csv(io.BytesIO(data))
    df["content"] = df["titulo"] + ' ' + df["conteudo"]
    return df


# In[170]:


#Cria e retorna um dicionario de tokens. Cada chave do dicionario possui como valor um conjunto(set) de noticias em que 
# este token aparece. 
def init_tokens():
    tokens = {}
    df = getCSVFormattedAsDF()
    sizeDF = len(df["idNoticia"])
    
    for idx in range(sizeDF):
        content = df["content"][idx]
        words = nltk.word_tokenize(content)
        for word in words:
            word = word.lower()
            try:
                tokens[word].add(df["idNoticia"][idx]) 
            except KeyError:
                tokens[word] = set()
                tokens[word].add(df["idNoticia"][idx]) 
            
    return tokens


# In[167]:


# Retorna o conjunto de tokens da operação pesquisa. 
def search(ipt, tokens):
    if (ipt.strip() == ""):
        return "Please, inform at least one token"
    
    ipt = ipt.split(" ")
    init = ipt[0].lower()
    size = len(ipt)
    
    if (size == 1) :
        if init not in tokens:
            return "This token is not present in any news"
        else:
            return tokens[init]
    else:
        result = set(tokens[init])
        comand = ""
        for index in range(1,size):
            if ipt[index] == "AND":
                comand = AND
            elif ipt[index] == "OR":
                comand = OR
            elif ipt[index].lower() in tokens:
                if comand == AND:
                    result = (tokens[ipt[index].lower()]  & result)
                elif comand == OR:
                    result |= (tokens[ipt[index].lower()] | result)
                comand = ""
            else:
                comand = ""
        return result
        


# In[171]:


# Inicia o dicionario de tokens
tokens = init_tokens()


# In[173]:


assert len(search("Campina AND Grande", tokens)) == 12
assert len(search("debate OR presidencial", tokens)) == 1770
assert len(search("debate AND presidencial", tokens)) == 201
assert len(search("presidenciáveis OR corruptos", tokens)) == 164
assert len(search("presidenciáveis AND corruptos", tokens)) == 0
assert len(search("Belo OR Horizonte", tokens)) == 331
assert len(search("Belo AND Horizonte", tokens)) == 242

