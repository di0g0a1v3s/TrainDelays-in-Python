from urllib.request import Request, urlopen
from datetime import date
import json

station_query_url="https://www.infraestruturasdeportugal.pt/negocios-e-servicos/estacao-nome/{train_search_term}"
trips_info_query_url="https://www.infraestruturasdeportugal.pt/negocios-e-servicos/partidas-chegadas/{station_id}/{date_start}%20{hour_start}/{date_end}%20{hour_end}"
train_info_query_url="https://www.infraestruturasdeportugal.pt/negocios-e-servicos/horarios-ncombio/{train_id}/{date}"
station_info_query_url="https://www.infraestruturasdeportugal.pt/negocios-e-servicos/estacoes/getServicos/{station_id}"



def main():
    station_name = "vendas novas"
    station_id = getStationID(station_name)
    trips = getTripsFromStation(station_id)
    for trip in trips:
        print(" ")
        print(trip)
        
    


def getStationID(station_name):
    url = station_query_url.format(train_search_term = station_name.split(' ')[0])
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        result = urlopen(req)
    except:
        return None

    data = json.loads(result.read())

    for station in data['response']:
        if station['Nome'].lower() == station_name.lower():
            print("Nome Estacao: ", station['Nome'], " ID: ",station['NodeID'])
            return station['NodeID']
    
    if data['response']:
        station = data['response'][0]
        if station is not None:
            print("Nome Estacao: ", station['Nome'], " ID: ",station['NodeID'])
            return station['NodeID']

    return None



def getTripsFromStation(station_id):
    comboios_desc = []

    date_today = date.today()
    url = trips_info_query_url.format(station_id = station_id, date_start = date_today, hour_start = '00:00', date_end = date_today, hour_end = '23:59')
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        result = urlopen(req)
    except:
        return None

    data = json.loads(result.read())
    #print(data)
    for node in data['response']:
        if node['TipoPedido'] == 2: #chegadas
            for comboio in node['NodesComboioTabelsPartidasChegadas']:
                comboios_desc.append(getTrainInfo(comboio['NComboio1']))
    return comboios_desc




def getStationInfo(station_id):
    return 0

def getTrainInfo(train_id):
    train_desc = "Comboio "
    date_today = date.today()
    url = train_info_query_url.format(train_id = train_id, date = date_today)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        result = urlopen(req)
    except:
        return None

    data = json.loads(result.read())
    train_info = data["response"]
    train_desc = train_desc + " " + str(train_id) + " " + train_info["Operador"] + " " 
    train_desc = train_desc + train_info["TipoServico"] + " de " 
    train_desc = train_desc + train_info["Origem"] + " (" 
    train_desc = train_desc + train_info["DataHoraOrigem"] 
    train_desc = train_desc + ") para " + train_info["Destino"] 
    train_desc = train_desc + " (" + train_info["DataHoraDestino"] + ") " + train_info["SituacaoComboio"] + "\n"
    for paragem in train_info["NodesPassagemComboio"]:
        arrived_symbol = 'V' if paragem["ComboioPassou"] else 'X'
        train_desc = train_desc + "-> " + paragem["NomeEstacao"] +  " ("+paragem["HoraProgramada"]+")" + " ("+arrived_symbol+")"
    return train_desc


if __name__ == "__main__":
    main()