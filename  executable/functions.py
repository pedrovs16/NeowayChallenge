from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


def StateChoice(uf, num, archiveName):
    print(f'----------------Pegando dados de {uf}----------------')
    # Para deixar o navegador invisível

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    # Abrindo o navegador
    try:
        driver = webdriver.Chrome('chromedriver.exe', options=options)
    except:
        print('Não foi possível acessar o site, verifique no seu navegador se o site está '
              'funcionando http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm.')
        return num

    # Entrando na página principal

    try:
        driver.get('http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm')
    except:
        print('Não foi possível acessar o site, verifique no seu navegador se o site está '
              'funcionando http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm.')
        return num

    # Escolhendo o estado
    try:
        if uf == 'RR':  # Se for digitado 'RR' pega as infos de 'RN' e se for 'RRRR' vai para 'RR'
            search = driver.find_element_by_class_name('f1col')
            search.send_keys('RRRR')
            search1 = driver.find_element_by_class_name('f6col')
            search1.send_keys(Keys.ENTER)
        else:
            search = driver.find_element_by_class_name('f1col')
            search.send_keys(uf)
            search1 = driver.find_element_by_class_name('f6col')
            search1.send_keys(Keys.ENTER)
    except:
        print('Não foi possível acessar o site, verifique no seu navegador se o site está '
              'funcionando http://www.buscacep.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm.')
        return num

    # Variáveis

    lists = []
    tmptabela = 2

    dictionary = {'uf': uf, 'id': '', 'localidade': '', 'faixa-de-cep': ''}

    # Pegando os dados da página

    print('Buscando dados...')
    while True:
        try:

            # Selecionando a área com os dados

            info = WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.XPATH, f"/html/body/div/div/div/div/div/div/div/"
                                                          f"div/table[{tmptabela}]/tbody"))
            )
        except:
            driver.quit()
            break

        tmptabela = 1

        # Modelando os dados para serem manipulados

        info = info.text
        info = info.split('\n')

        conditional = False
        for line in info[1:]:
            line = line[0:(line.find('-0') + 16)]
            line = line.replace(' a ', ';')
            for x in range(0, 9):
                line = line.replace(f' {x}', f'##{x}')
            line = line.replace(';', ' a ')
            line = line.split('##')

            # Adicionando ID
            if uf == 'DF':  # No distrito federal registra 2 Brasilias diferente com CEP DIFERENTES
                for county in lists:
                    if county[1] == line[0] and county[2] == line[1]:
                        conditional = True
            else:
                for county in lists:
                    if county[1] == line[0]:
                        conditional = True
            if not conditional:
                line.insert(0, num)
                num += 1
                lists.append(line)
                dictionary['localidade'] = line[1]
                dictionary['id'] = line[0]
                dictionary['faixa-de-cep'] = line[2]

                # Criando arquivo JSONL
                try:
                    archive = open(f'{archiveName}.jsonl', 'rt')
                    archive.close()
                except FileNotFoundError:
                    with open(f'{archiveName}.jsonl', 'w') as f:
                        json.dump(dictionary, f)
                        f.write('\n')
                else:
                    with open(f'{archiveName}.jsonl', 'at') as f:
                        json.dump(dictionary, f)
                        f.write('\n')
                print(dictionary)
            conditional = False
        try:

            # Trocar de página

            page = driver.find_element_by_xpath("/html/body/div/div/div/div/div/div/div/div/div[2]/a")
            page.click()
        except:  # Quando não conseguir mais trocar de página cancela a função
            driver.quit()
            return num
