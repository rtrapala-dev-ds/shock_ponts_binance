import config
import time

from binance.futures import Futures
from colorama import init
from colorama import Fore, Back, Style


def get_ticker_symbol():
    '''
    Ask for the ticker symbol as it appears in Binance Futures
    Returns the ticker symbol in upper case
    '''
    ticker_symbol = input("Ingresa el ticker symbol -> ")
    return ticker_symbol.upper()


def get_client():
    '''
    Connect to the Binance Futures API to the account and retunrs that conection
    '''
    return Futures(key = config.API_KEY, secret = config.API_SECRET)


def get_best_ask_bid(client, ticker):
    '''
    Returns the best ask bid data for the ticker sent
    '''
    return client.book_ticker(symbol = ticker)


def get_order_book(client, ticker):
    try:
        order_book =  client.depth(symbol = ticker)
        return order_book['bids'], order_book['asks']
    except Exception as e:
        print(e)


def get_shock_points(bids, asks):
    '''
    buy = [maximo, mmedio, minimo], 0,1,2
    sell = [maximo, mmedio, minimo], 0,1,2
    '''
    buy = [ [0.0, 0.0], [0.0, 0.0], [0.0, 0.0] ]
    sell = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0] ]

    for l in bids:
        cantidad_libro = float(l[1])
        if cantidad_libro >= float(buy[0][1]): #cantidad libro >= cantidad máxima
            buy[2] = buy[1] #la cant minima ahora es la que era la media
            buy[1] = buy[0] #la cant media ahora es la que era la máxima
            buy[0] = l #la cant máxima ahora es la del libro

        elif cantidad_libro >= float(buy[1][1]): #Si cantidad libro < cantidad máxima, revisamos si cantidad libro >= cantidad media
            buy[2] = buy[1] #la cant minima ahora es la que era la media
            buy[1] = l #la cant media ahora es la del libro
        
        elif cantidad_libro >= float(buy[2][1]): # Si la cantidad del libro es menor a la máxima y menor a la media, revisamos que sea mayor a la mínima
            buy[2] = l #la cantidad mínima ahora es la del libro
        

    for l in asks:
        cantidad_libro = float(l[1])
        if cantidad_libro >= float(sell[0][1]): #cantidad libro >= cantidad máxima
            sell[2] = sell[1] #la cant minima ahora es la que era la media
            sell[1] = sell[0] #la cant media ahora es la que era la máxima
            sell[0] = l #la cant máxima ahora es la del libro

        elif cantidad_libro >= float(sell[1][1]): #Si cantidad libro < cantidad máxima, revisamos si cantidad libro >= cantidad media
            sell[2] = sell[1] #la cant minima ahora es la que era la media
            sell[1] = l #la cant media ahora es la del libro
        
        elif cantidad_libro >= float(sell[2][1]): # Si la cantidad del libro es menor a la máxima y menor a la media, revisamos que sea mayor a la mínima
            sell[2] = l #la cantidad mínima ahora es la del libro

    return sorted(buy, reverse=True), sorted(sell, reverse=True)



def run():
    client = get_client()
    ticker = get_ticker_symbol()
    bids, asks = get_order_book(client, ticker)
    buy, sell = get_shock_points(bids, asks)
    print('\n')
    print(f'{"*" * 45}')
    print(f'{" "*15}SHOCK POINTS{" "*15}')
    print(f'{"*" * 45}')
    print('\n')
    print(f'Venta:')
    print(f'1- Precio: {sell[0][0]}, cantidad: {sell[0][1]}')
    print(f'2- Precio: {sell[1][0]}, cantidad: {sell[1][1]}')
    print(f'3- Precio: {sell[2][0]}, cantidad: {sell[2][1]}')
    print('\n')
    print(f'Compra:')
    print(f'1- Precio: {buy[0][0]}, cantidad: {buy[0][1]}')
    print(f'2- Precio: {buy[1][0]}, cantidad: {buy[1][1]}')
    print(f'3- Precio: {buy[2][0]}, cantidad: {buy[2][1]}')
    
    
    print('\n')
if __name__ == "__main__":
    run()
