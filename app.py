import pandas as pd 
import numpy as np 
import pickle as pk 
import streamlit as st
import locale

locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8') #Fiyatı yazarken aralara nokta koyması için.

model = pk.load(open('model.pkl','rb'))

st.header('Araba Fiyat Tahmin Modeli')

cars_data = pd.read_csv('Cardetails.csv')

def get_brand_name(car_name):
    car_name = car_name.split(' ')[0]
    return car_name.strip()
cars_data['name'] = cars_data['name'].apply(get_brand_name)

# Türkçe çeviri için bir sözlük oluşturun
transmission_translations = {"Manual": "Manuel", "Automatic": "Otomatik"}
sellerType_translations = {"Individual": "Sahibinden", "Dealer": "Galeriden", "Trustmark Dealer": "Yetkili Bayiden"}
owner_translations = {"First Owner": "İlk Sahibinden", "Second Owner": "İkinci Sahibinden", "Third Owner": "Üçüncü Sahibinden",
                       "Fourth & Above Owner": "4. veya Daha Sahibinden", "Test Drive Car": "Test Aracı"}
fuel_translations = {"Diesel": "Dizel", "Petrol": "Benzin", "LPG": "LPG", "CNG": "CNG"}
# Çevirili seçenekleri yeni bir listeye kaydedin
translated_transmission_options = [transmission_translations[transmission] for transmission in cars_data['transmission'].unique()]
translated_sellerType_options = [sellerType_translations[seller_type] for seller_type in cars_data['seller_type'].unique()]
translated_owner_options = [owner_translations[owner] for owner in cars_data['owner'].unique()]
translated_fuel_options = [fuel_translations[fuel] for fuel in cars_data['fuel'].unique()]

name = st.selectbox('Aracınızın Markası', sorted(cars_data['name'].unique()))
year = st.slider('Model Yılı', 1994,2024)
km_driven = st.slider('Kilometre', 0,300000)
fuel = st.selectbox('Yakıt Türü', sorted(translated_fuel_options))
seller_type = st.selectbox('Satıcı Tipi', translated_sellerType_options)
transmission = st.selectbox('Vites', translated_transmission_options)
owner = st.selectbox('Kaçıncı Sahip', translated_owner_options)
mileage = st.slider('1 Litre ile Kaç KM (Milage)', 10,40)
engine = st.slider('Motor CC', 700,5000)
max_power = st.slider('Beygir Gücü', 0,200)
seats = st.slider('Kaç Koltuklu', 5,10)


if st.button("Hesapla"):
    input_data_model = pd.DataFrame(
    [[name,year,km_driven,fuel,seller_type,transmission,owner,mileage,engine,max_power,seats]],
    columns=['name','year','km_driven','fuel','seller_type','transmission','owner','mileage','engine','max_power','seats'])
    
    input_data_model['owner'].replace(['İlk Sahibinden', 'İkinci Sahibinden', 'Üçüncü Sahibinden',
       '4. veya Daha Sahibinden', 'Test Aracı'],
                           [1,2,3,4,5], inplace=True)
    input_data_model['fuel'].replace(['Dizel', 'Benzin', 'LPG', 'CNG'],[1,2,3,4], inplace=True)
    input_data_model['seller_type'].replace(['Sahibinden', 'Galeriden', 'Yetkili Bayiden'],[1,2,3], inplace=True)
    input_data_model['transmission'].replace(['Manuel', 'Otomatik'],[1,2], inplace=True)
    input_data_model['name'].replace(['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault',
       'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
       'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus',
       'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
       'Ambassador', 'Ashok', 'Isuzu', 'Opel'],
                          [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
                          ,inplace=True)

    car_price = model.predict(input_data_model)
    car_price_rounded = round(car_price[0])
    
    formatli_sayi = locale.format_string('%d', car_price_rounded, grouping=True)
    st.header('Tahmini Araç Fiyatı: ' + formatli_sayi + ' TL')

st.text("Credit by Selin ÇABUK, M.Ali TONGA")