from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import pandas as pd
import math
from collections import Counter
import nltk
import pickle
import phonenumbers
from phonenumbers import carrier, timezone, geocoder
## required nltk packages

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')


DETECTION_THRESHOLD = 0.03

lemmatizer = WordNetLemmatizer()
vectorizer = CountVectorizer(max_features=1500)
classifier = MultinomialNB(alpha=0.01)

def porn_score(text):
    data = re.sub('[^\w\s]', '', text)
    data = data.lower()
    data = word_tokenize(data)
    data = [lemmatizer.lemmatize(word) for word in data if word not in set(stopwords.words('english'))]

    """## Classification Pornography"""

    df_train=pd.read_csv('porn.csv')

    training_vectors = vectorizer.fit_transform(df_train.Contents)
    classifier.fit(training_vectors, df_train.Labels)

    test_vectors = vectorizer.transform(data)

    predict = classifier.predict(test_vectors)

    ratio = float(format((sum(predict)/len(predict)), ".2f"))

    detected = ratio >= DETECTION_THRESHOLD
    print("\nRatio:", ratio)
    print("Detected", detected)
    # return {"child pornography":str(ratio)}
    return str(ratio)


# def load_model():
#     global vectorizer
#     global classifier
#     vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
#     classifier = pickle.load(open('classifier.pkl', 'rb'))
# def save_model():
#     pickle.dump(vectorizer, open('vectorizer.pkl', 'wb'))
#     pickle.dump(classifier, open('classifier.pkl', 'wb'))
    
def drug_score(text):
    data = re.sub('[^\w\s]', '', text)
    data = data.lower()
    data = word_tokenize(data)
    data = [lemmatizer.lemmatize(word) for word in data if word not in set(stopwords.words('english'))]
    df_train=pd.read_csv('drugs.csv')
    training_vectors = vectorizer.fit_transform(df_train.text)
    classifier.fit(training_vectors, df_train.category)
    test_vectors = vectorizer.transform(data)
    predict = classifier.predict(test_vectors)

    ratio = float(format((sum(predict)/len(predict)), ".2f"))

    detected = ratio >= DETECTION_THRESHOLD
    print("\nRatio:", ratio)
    print("Detected", detected)
    # return {"drugs":str(ratio)}
    return str(ratio)

# def intelligence(text):
#     intelligence_data={}
#     text_block = text
#     #r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
#     #phone_numbers = r.findall(text_block)
#     #print(phone_numbers)
#     for match in phonenumbers.PhoneNumberMatcher(text_block, ""):
#         number=(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
#         my_number = phonenumbers.parse(number)
#         number_info+=my_number
#         if phonenumbers.is_valid_number(my_number):
#             number_info+=","+(carrier.name_for_number(my_number, "en"))
#             number_info+=","+timezone.time_zones_for_number(my_number)
#             number_info+=","+(geocoder.description_for_number(my_number, 'en'))
#         intelligence_data['phone_numbers']=number_info
    
#     r = re.compile(r'[\w\.-]+@[\w\.-]+')
#     emails=r.findall(text_block)
#     intelligence_data['emails']=emails
#     print(emails)
    
#     names = []
#     sentences = ie_preprocess(text_block)
#     for tagged_sentence in sentences:
#         for chunk in nltk.ne_chunk(tagged_sentence):
#             if type(chunk) == nltk.tree.Tree:
#                 if chunk.label() == 'PERSON':
#                     names.append(' '.join([c[0] for c in chunk]))
#     intelligence_data['names']=names
    
#     return intelligence_data

def intelligence(text):
    text_block = text
    #r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    #phone_numbers = r.findall(text_block)
    #print(phone_numbers)
    for match in phonenumbers.PhoneNumberMatcher(text_block, ""):
        number=(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
        my_number = phonenumbers.parse(number)
        number_info+=my_number
        if phonenumbers.is_valid_number(my_number):
            number_info+=","+(carrier.name_for_number(my_number, "en"))
            number_info+=","+timezone.time_zones_for_number(my_number)
            number_info+=","+(geocoder.description_for_number(my_number, 'en'))
        intelligence_data += number_info
    
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    emails=r.findall(text_block)
    intelligence += "\n"
    for(email in emails):
        intelligence+=email
        intelligence+=" "
    print(emails)
    
    names = []
    sentences = ie_preprocess(text_block)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    intelligence+=" "
    for(name in names):
        intelligence+=str(name)
    return intelligence


def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in set(stopwords.words('english'))])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences
    
if __name__ == "__main__":
    print(porn_score('Skip to content  Login   Register   Cart   Checkout   Black MarketBuy Guns,Buy Cocaine,Buy Counterfeit money,Search for:AllUncategorizedCounterfeit BanknotesDocuments for SaleDrugs for SaleCannabis for SaleGuns for SaleMoney TransfersPhysical Clone CardsCOVID19 CARDSAMMOBITCOIN MINING MACHINES  Mail Us: alexweeds00@gmail.com 0TOTAL$0.00 HomeMy accountShopGuns for SaleMoney TransfersPhysical Clone CardsDocuments for SaleDrugs for SaleStore List  Cloned Cards Vendors providing all sorts of physical cloned cards Shop now  Guns Trusted sellers of guns are available here shop now   America Express Prepaid card $7000 Balance x1$325.00Add to cartStore:  BestCarder 0 out of 5				WESTERN UNION TRANSFER $3000$400.00Add to cartStore:  The Carder 0 out of 5				Taurus G2C Black 9mm Pistol – Blue/Black, 3.2″ Barrel, 12+1 Rounds, Polymer Grips, 3-Dot SightsRated 5.00 out of 5$245.00Add to cartRuger SFAR For SaleRated 5.00 out of 5$990.00Add to cartFentanyl Liquid For Sale(250vials)$1,000.00Add to cartCalifornia Weed$800.00Add to cartStore:  DOPETREES 0 out of 5				PayPal Account $300-399 Balance$99.00Add to cartStore:  PayPal Mafia 0 out of 5				Buy Crystal Meth Online(10grams)$350.00Add to cartAvalon A1166 Pro 78th Canaan Avalon BTC Asic Miner SHA-256Rated 5.00 out of 5$3,500.00Add to cartStore:  Cartel Darknet Shop 0 out of 5				Smith and Wesson 686 magnum 357.Rated 5.00 out of 5$800.00Add to cartStore:  Glock404 0 out of 5				BUY UK DRIVING LICENSERated 5.00 out of 5$1,000.00Add to cartStore:  Document Doctor 0 out of 5				BUY LITHUANIAN DRIVING LICENSE$780.00Add to cartStore:  Document Doctor 0 out of 5				BUY BELGIAN DRIVING LICENSE$850.00Add to cartStore:  Document Doctor 0 out of 5				Sale!Buy 100 ml Phenobarbital sodium Nembutal Oral liquidRated 5.00 out of 5$650.00 $450.00Add to cartStore:  Lab King 0 out of 5				Buy 50 Suicide Nembutal Phenobarbital Sodium Pills 100mg OnlineRated 5.00 out of 5$400.00Add to cartStore:  Lab King 0 out of 5				AllPhysical Clone Cards Money Transfers Uncategorized Guns for Sale Cannabis for Sale Drugs for Sale BITCOIN MINING MACHINES Documents for Sale   Best Selling ProductsSale ProductsFeatured ProductsRecent ProductsTop Rated Products  Show AllPayPal Account with 899$ balance$89.00Add to cartStore:  DYGMORE 5 out of 5				PayPal Account with 1000$ balanceRated 5.00 out of 5$100.00Add to cartStore:  DYGMORE 5 out of 5				PayPal Account with 2500$ balanceRated 5.00 out of 5$250.00Add to cartStore:  DYGMORE 5 out of 5				COVID19 VACCINE CARDRated 4.43 out of 5$300.00Add to cartStore:  The Doc Guy 0 out of 5				BERETTA 92 FS INOXRated 5.00 out of 5$648.70Add to cartStore:  Glock404 0 out of 5				Buy 50 Suicide Nembutal Phenobarbital Sodium Pills 100mg OnlineRated 5.00 out of 5$400.00Add to cartStore:  Lab King 0 out of 5				Pure Cocaine For Sale Online15grams (1grams= 25$)Rated 5.00 out of 5$350.00Add to cartTaurus G2C Black 9mm Pistol – Blue/Black, 3.2″ Barrel, 12+1 Rounds, Polymer Grips, 3-Dot SightsRated 5.00 out of 5$245.00Add to cart Sale!Registered UK passportRated 4.00 out of 5$3,500.00 $2,500.00Add to cartStore:  The Doc Guy 0 out of 5				Sale!Undetectable fake ID cardsRated 3.00 out of 5$300.00 $199.00Add to cartStore:  The Doc Guy 0 out of 5				Sale!Buy Registered Australian PassportsRated 5.00 out of 5$2,700.00 $2,250.00Add to cartSale!Buy Counterfeit Euro Banknotes(50s)5000euroRated 5.00 out of 5$2,000.00 $1,000.00Add to cartSale!Buy Counterfeit 20s euro bills(5000euro)Rated 5.00 out of 5$1,500.00 $800.00Add to cartSale!buy counterfeit 50s British pounds (5000GBP)$1,500.00 $800.00Add to cartSale!Buy Fake 100 Canadian Dollar bills(2000$)$800.00 $400.00Add to cartSale!Amnesia Haze (30grams)$350.00 $220.00Add to cart  Google Play gift code 500$ (instant Delivery)$99.00 – $499.00Select optionsStore:  The Beast 0 out of 5				iTunes Gift Card$99.00 – $499.00Select optionsStore:  The Beast 0 out of 5				International Wire | Bank Transfer 2020$200.00 – $1,500.00Select optionsStore:  The Carder 0 out of 5				MoneyGram Transfers$99.00 – $499.00Select optionsStore:  The Carder 0 out of 5				PayPal Transfers$120.00 – $500.00Select optionsStore:  The Carder 0 out of 5				Heroin Lab tested ⦿ USA /EU stockRated 4.00 out of 5$220.00 – $699.00Select optionsStore:  Lab King 0 out of 5				Sale!Registered UK passportRated 4.00 out of 5$3,500.00 $2,500.00Add to cartStore:  The Doc Guy 0 out of 5				Sale!Undetectable fake ID cardsRated 3.00 out of 5$300.00 $199.00Add to cartStore:  The Doc Guy 0 out of 5				 Buy 50 Suicide Nembutal Phenobarbital Sodium Pills 100mg OnlineRated 5.00 out of 5$400.00Add to cartStore:  Lab King 0 out of 5				Ruger SFAR For SaleRated 5.00 out of 5$990.00Add to cartSale!Buy Registered Australian PassportsRated 5.00 out of 5$2,700.00 $2,250.00Add to cartSale!Buy 100 ml Phenobarbital sodium Nembutal Oral liquidRated 5.00 out of 5$650.00 $450.00Add to cartStore:  Lab King 0 out of 5				Pure Cocaine For Sale Online15grams (1grams= 25$)Rated 5.00 out of 5$350.00Add to cartTaurus G2C Black 9mm Pistol – Blue/Black, 3.2″ Barrel, 12+1 Rounds, Polymer Grips, 3-Dot SightsRated 5.00 out of 5$245.00Add to cartSale!Buy Counterfeit Euro Banknotes(50s)5000euroRated 5.00 out of 5$2,000.00 $1,000.00Add to cartPayPal Account with 1000$ balanceRated 5.00 out of 5$100.00Add to cartStore:  DYGMORE 5 out of 5				 How To Use Our Market Euro banknotes | USD banknotes | fake Australia dollars| fake British Pounds| Canadian dollars,Visit our Blog for more InfoContact UsWickr ID :blackmart Email: alexweeds00@gmail.com © 2023 Black Market | Theme by Theme Farmer"'))
    print("Loading model...")
