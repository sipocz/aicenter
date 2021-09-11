from flask import Flask
from flask import render_template_string
from flask import render_template

import os
app = Flask(__name__)

import requests
from bs4 import  BeautifulSoup
app.logger.error('testing error log')
app.logger.info('testing info log')


def ansicode(sti):
    outstr=""
    for i in sti:
        a=i
        if i=="á":
            a="a"
        if i=="Á":
            a="A"
        if i=="é":
            a="e"
        if i=="É":
            a="E"
        if i=="í":
            a="I"
        if i=="Í":
            a="I"
        if i=="ö":
            a="o"
        if i=="Ö":
            a="O"
        if i=="ő":
            a="o"
        if i=="Ő":
            a="O"
        if i=="ó":
            a="o"
        if i=="Ó":
            a="O"
        if i=="ü":
            a="u"
        if i=="Ü":
            a="u"
        if i=="ú":
            a="u"
        if i=="Ú":
            a="u"
        outstr=outstr+a
    return(outstr)




def ingatlantajolo_querycity(city):
    out=""
    
    out+="<be>"
    out+="<H1>"+city.capitalize()+"</H1><br>"
    city=ansicode(city)
    city=city.lower()

    url="https://www.ingatlantajolo.hu/"+city+"+elado+haz-hazresz"
    res=requests.get(url)
    #print (res.text)
    soup=BeautifulSoup(res.text,"html.parser")
    link=soup.select(".moreDetailsBox > a[href] ")
    urllist=soup.find_all("a", class_="results__item")
    #print(urllist)
    
    pricelist=soup.find_all("p", class_="property-card__price")
    print(len(pricelist))


    out1=[]
    out2={}
    
    for i in enumerate(urllist):
        link=""+i[1]['href']
        #print (link[0:5])
        if link[0:5]=="https":
            
            print(i[0],". ",pricelist[i[0]].text.strip().replace("\n","").replace("\t","").replace(" Ft","Ft "),link)
            out+=str(i[0])+". "+pricelist[i[0]].text.strip().replace("\n","").replace("\t","").replace(" Ft","Ft ")+'<br><a href="'+link+'">'+link+"</a>" +"<br>"
            out1.append([pricelist[i[0]].text,link])

        #out.append([urllist[i],pricelist[i]])
    
    print("----------------  END  ------------------------")
    return(out1)





def ingatlan_com_pages(city):
    

    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
    
    url="https://ingatlan.com/lista/elado+haz+"+city+"+ar-szerint-csokkeno?page=1"
    print(url)
    res=requests.get(url,headers=header)
    soup=BeautifulSoup(res.text,"html.parser")
    pages=soup.find_all("div",class_="pagination__page-number")

    if len(pages) < 1 :
        return(1)
    pages_txt=pages[0].text
    pages_num=pages_txt.split(" ")
    pages_num_int=int(pages_num[3])
    if pages_num_int>30:
       pages_num_int=1
    return(pages_num_int)

def ingatlan_com_querycity_page(city,page):
    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
    
    
   
    city=ansicode(city)
    url="https://ingatlan.com/lista/elado+haz+"+city+"+ar-szerint-csokkeno?page="+str(page)
    #print(url)
    res=requests.get(url,headers=header)
    soup=BeautifulSoup(res.text,"html.parser")
    link=soup.select(".moreDetailsBox > a[href] ")
    urllist=soup.find_all("a", class_="listing__link")

    price=soup.select("span ")
    pricelist=soup.find_all("div",class_="price")

    #print(urllist)
    #print(pricelist)

    out1=[]
    out2={}
    
    for i in enumerate(urllist):
        link="https://ingatlan.com"+i[1]['href']
        #print(f"+{i[0]:>4}. {pricelist[i[0]].text:>18} :  {link:<1000}")
        #print(i[0],". ",pricelist[i[0]].text,link)
      
      
        out1.append([pricelist[i[0]].text,link])

        #out.append([urllist[i],pricelist[i]])
    print(out1)
    return (out1)

def ingatlan_com_querycity(city):
    ansicity=ansicode(city)
    maxpage=ingatlan_com_pages(ansicity)
    print(maxpage)
    o=[]
    for i in range(maxpage):
        o+=ingatlan_com_querycity_page(ansicity,i+1)
    return(o)

def ingatlannet_pages(city):
    
    #return(1)
    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
    url0="https://www.ingatlannet.hu/elad%C3%B3/h%C3%A1z/"


    url=url0+city+"?page=1&per-page=25&sort=-ar"
    
    res=requests.get(url,headers=header)
    
    soup=BeautifulSoup(res.text,"html.parser")
    pages=soup.find_all("div",class_="page-counter")
    
    pages_txt=pages[0].text.strip()
    
    pages_num=pages_txt.split(" ")
   
    
    pages_num=pages_num[0]
    
    pages_num=pages_num.split("/")[1]
    pages_num_int=int(pages_num)
    if pages_num_int>30:
       pages_num_int=1
    return(pages_num_int)

def ingatlannet_querycity_page(city,page):
    #city=ansicode(city)
    
    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
    url0="https://www.ingatlannet.hu/elad%C3%B3/h%C3%A1z"
    url=url0+"/"+city+"?page="+str(page)+"&per-page=25&sort=-ar"
   
   
    print(url)
    res=requests.get(url,headers=header)
    soup=BeautifulSoup(res.text,"html.parser")
  
    urllist=soup.find_all(attrs={"data-behavior":"estate-view","target":"_blank"}) # data-behavior="estate-view"
    
 
   
   

    price=soup.find_all("p", class_="h2 d-none d-md-block price-text mt-3 mb-3")
    

    #print(urllist)
    

    outp=[]
    outl=[]
    url0="https://www.ingatlannet.hu"
    for i in urllist:
        link=url0+i['href']
        if link in outl:
            pass
        else:
            outl.append(link)

        #print(f"+{i[0]:>4}. {pricelist[i[0]].text:>18} :  {link:<1000}")
        #print(i[0],". ",pricelist[i[0]].text,link)
      
    for i in price:
        outp.append(i.text.strip())
    o=[]
    for i,link in enumerate(outl):
        o.append([outp[i],link])
        #out.append([urllist[i],pricelist[i]])
    #print(outp)
    #print(outl)
  
    return (o)


def ingatlannet_querycity(city):
    maxpage=ingatlannet_pages(city)
    print(maxpage)
    ing=[]
    for i in range(maxpage):
        ing_list=ingatlannet_querycity_page(city,i+1)
        print(ing_list)
        ing+=ing_list
    return(ing)

def arxiv_pages(code):
    

    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
    url=f"https://arxiv.org/search/?query={code}&searchtype=all&abstracts=hide&order=-announced_date_first&size=50"


    
    #print(url)
    res=requests.get(url,headers=header)
    
    soup=BeautifulSoup(res.text,"html.parser")
    pdfs=soup.find_all("p",class_="list-title is-inline-block")
    pdflist=[]
    for pdf in pdfs:
        st=pdf.a["href"]
        st=st.replace("abs","pdf")
        pdflist+=[st]
    #pages_txt=pages[0].text.strip()
    #print(pages_txt)
    titles=soup.find_all("p",class_="title is-5 mathjax")
    titlelist=[]
    
    for title in titles:
        st=title.text.strip()
        
        titlelist+=[st]

    dates=soup.find_all("p",class_="is-size-7")
    datelist=[]
    montslist=["January","February","March","April","May","June","July","August", "September","October","November","December"]
    for date in dates:
        st=date.text
        if "Submitted" in st:
            st=st.split(";")
            st=st[0][10:].strip()
            date=st.split(" ")
            monts=date[1][:-1]
            #print(monts)
            if monts in montslist and st[0] in "123456789":
               datelist+=[st]
    o=[]
    for i,title in enumerate(titlelist):
        o.append([datelist[i],title,pdflist[i]])
    return(o)

def getBalance(currency):
    data={"currency":currency}
    basestr="https://tradeogre.com/api/v1/"
    apicmd="account/balance"
    url=basestr+f"{apicmd}"
    print(url)
    api=requests.post(url,data=data,auth=(key,secret),)
    return(api)


def getBalances():
    
    basestr="https://tradeogre.com/api/v1/"
    apicmd="account/balances"
    url=basestr+f"{apicmd}"
    print(url)
    api=requests.get(url,auth=(key,secret),)
    return(api)

def getTicker(currency):
    basestr="https://tradeogre.com/api/v1/"
    apicmd=f"ticker/{currency}"
    url=basestr+f"{apicmd}"
    #print(url)
    api=requests.get(url,auth=(key,secret),)
    return(api)


def getallcoin():
    balance=getBalances()
    balance=balance.json()
    #print(balance)
    nonzero={i:float(balance["balances"][i]) for i in balance["balances"].keys() if float(balance["balances"][i])>0.0}
    arr=[]
    for i in nonzero.keys():
        if i !="BTC":
            t_ext="BTC"
            ti=t_ext+"-"+i
        else:
            t_ext="USDT"
            ti=t_ext+"-"+i
        o=getTicker(ti)
        o=o.json()
        #print(o)
        #print(f'Ticker: {i} : {o["price"]}')
        coinBalance=float(balance["balances"][i])
        coinPrice=float(o["price"])
        BTCprice=46850
        if t_ext=="USDT":

            USDP=coinBalance*coinPrice
        else:
            USDP=coinBalance*coinPrice*BTCprice


        imgurl="https://tradeogre.com/img/coins/"+i+".png"
        arr.append([imgurl,ti, f'{coinPrice:.9f}',t_ext,coinBalance,f'{USDP:.3f} $',USDP])
        

    arr.sort(key=lambda arr:arr[6],reverse=True)
        
    return(arr)











#render_template_string(html_template,ingatlan_com=ingatlan_com_table)

@app.route('/city/<city>')

def getcity(city="bajna"):
   outstr=render_template("html_template_city.html",
                                 city_name=city.capitalize(),
                                 ingatlanCom=ingatlan_com_querycity(city),
                                 ingatlantajolo=ingatlantajolo_querycity(city),
                                 ingatlannet=ingatlannet_querycity(city))
   print(outstr)
   return outstr

@app.route('/arxiv/<query>')

def getarxiv(query="python"):
   outstr=render_template("html_template_arxiv.html",
                                 query_in=query,
                                 arxiv_in=arxiv_pages(query)
                                 )
                                 
   #print(outstr)
   return outstr

@app.route('/crypto')

def getcrypto(ticker=""):
   outstr=render_template("html_template_crypto.html",
                                 query_in=ticker,
                                 crypto_in=getallcoin()
                                 )
                                 
   #print(outstr)
   return outstr




key="71191d9fd891eb083d06b48d064f81d1"
secret="25b896c1a197071156c3804b43c2f84c"
headers = {'X-ApiKeys' : 'Key=' + key + '; Secret=' + secret}


@app.route('/')
def hello_world():
   return "usage: https://pythonalarm.herokuapp.com/city/cityname <br>https://pythonalarm.herokuapp.com/arxiv/query+string  "

if __name__ == '__main__':
   porto = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=porto)
