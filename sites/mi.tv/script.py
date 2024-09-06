import xml.etree.ElementTree as ET
import copy

def clone_and_modify_channel(channel):
    # Clonar o elemento channel
    new_channel = copy.deepcopy(channel)
    
    # Modificar o atributo 'site_id'
    site_id = new_channel.get('site_id', '')
    if site_id.endswith('-hd'):
        site_id = site_id[:-3]  # Remove o '-hd' do final
    new_channel.set('site_id', site_id + '-fhd')
    
    # Modificar o nome do canal
    channel_name = new_channel.text or ''
    if 'HD' in channel_name:
        new_channel.text = channel_name.replace('HD', 'FHD')
    else:
        new_channel.text = channel_name + ' FHD'
    
    return new_channel

try:
    # Carregar o XML
    tree = ET.parse('mi.tv_br.channels.xml')
    root = tree.getroot()

    # Encontrar o elemento pai que contém todos os canais
    channels_parent = root.find('.//channels')
    if channels_parent is None:
        channels_parent = root  # Se não houver um elemento 'channels', usamos o root

    # Encontrar todos os elementos 'channel'
    channels = channels_parent.findall('channel')
    
    if not channels:
        print("Não foram encontrados elementos 'channel'. Verifique a estrutura do XML.")
    else:
        print(f"Encontrados {len(channels)} elementos 'channel'.")

        # Lista para manter todos os elementos na ordem correta
        new_elements = []

        # Iterar sobre todos os elementos 'channel'
        for channel in channels:
            # Adicionar o canal original à nova lista
            new_elements.append(channel)
            
            # Criar e adicionar o novo canal FHD
            new_channel = clone_and_modify_channel(channel)
            new_elements.append(new_channel)

        # Limpar o elemento pai e adicionar todos os elementos da nova lista
        channels_parent.clear()
        for element in new_elements:
            channels_parent.append(element)

        # Salvar o XML modificado
        tree.write('seu_arquivo_modificado.xml', encoding='UTF-8', xml_declaration=True)
        print("XML modificado salvo com sucesso.")

except ET.ParseError as e:
    print(f"Erro ao analisar o XML: {e}")
except FileNotFoundError:
    print("Arquivo XML não encontrado. Verifique se o caminho está correto.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")