import requests
import subprocess
import re

def run_powershell_command(command):
    """Executa um comando PowerShell e retorna a saída."""
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando PowerShell: {e}")
        return None

def format_disk_capacity(sizeGB):
    """Formata a capacidade do disco para categorias especificadas."""
    if sizeGB < 256:
        return "256 GB"
    elif sizeGB < 500:
        return "512 GB"
    elif sizeGB < 1000:
        return "1 TB"
    elif sizeGB < 2000:
        return "2 TB"
    elif sizeGB < 4000:
        return "4 TB"
    else:
        return "4 TB"

def get_memory_info():
    """Obtém informações de memória incluindo a capacidade total e frequência."""
    command = """
    Get-WmiObject Win32_PhysicalMemory | ForEach-Object {
        $capacityGB = [math]::round($_.Capacity / 1GB, 2)
        $speedMHz = $_.Speed
        Write-Output "$($_.BankLabel): Capacidade: $capacityGB GB, Velocidade: $speedMHz MHz, Fabricante: $($_.Manufacturer), Número de Série: $($_.SerialNumber)"
    }
    """
    output = run_powershell_command(command)
    if not output:
        return "Não foi possível obter informações de memória.", 0, set()
    
    memory_info = []
    total_capacity = 0
    speeds = set()
    
    for line in output.splitlines():
        if "Capacidade:" in line:
            try:
                capacity = float(re.search(r"Capacidade: (\d+(\.\d+)?) GB", line).group(1))
                total_capacity += capacity
            except (ValueError, AttributeError):
                pass
        if "Velocidade:" in line:
            speed_match = re.search(r"Velocidade: (\d+) MHz", line)
            if speed_match:
                speeds.add(speed_match.group(1))
        memory_info.append(line)
    
    formatted_memory_info = "\n".join(memory_info)
    return formatted_memory_info, total_capacity, speeds

def get_disk_info():
    """Obtém informações de armazenamento do disco incluindo o número de série."""
    command = """
    Get-WmiObject Win32_DiskDrive | ForEach-Object {
        $sizeGB = [math]::round($_.Size / 1GB, 2)
        Write-Output "Modelo: $($_.Model)"
        Write-Output "Interface: $($_.InterfaceType)"
        Write-Output "Capacidade: $sizeGB GB"
        Write-Output "Partições: $($_.Partitions)"
        Write-Output "Número de Série: $($_.SerialNumber)"
    }
    """
    output = run_powershell_command(command)
    if not output:
        return "Não foi possível obter informações de disco.", ""
    
    lines = output.splitlines()
    formatted_lines = []
    for line in lines:
        if line.startswith("Capacidade:"):
            try:
                sizeGB = float(re.search(r"(\d+(\.\d+)?)", line).group())
                formatted_lines.append(f"Capacidade: {format_disk_capacity(sizeGB)}")
            except (ValueError, AttributeError):
                formatted_lines.append(line)
        else:
            formatted_lines.append(line)
    return "\n".join(formatted_lines)

def get_processor_info():
    """Obtém informações do processador incluindo o número de série."""
    command = """
    Get-WmiObject Win32_Processor | ForEach-Object {
        Write-Output "Nome: $($_.Name)"
        Write-Output "Número de Núcleos: $($_.NumberOfCores)"
        Write-Output "Velocidade Máxima: $($_.MaxClockSpeed) MHz"
        Write-Output "Arquitetura: $($_.Architecture)"
        Write-Output "Número de Série: $($_.ProcessorId)"
    }
    """
    output = run_powershell_command(command)
    if not output:
        return "Não foi possível obter informações do processador."
    
    # Extrair apenas o modelo do processador
    processor_name_match = re.search(r"Nome:\s*(.+)", output)
    if processor_name_match:
        processor_name = processor_name_match.group(1)
        # Extrair apenas o modelo do processador
        processor_model_match = re.search(r'i\d{1,2}-\d{4,5}HX|i\d{1,2}-\d{4,5}H|i\d{1,2}\w*|\w{2,5}-\d{4,5}', processor_name, re.IGNORECASE)
        if processor_model_match:
            return processor_model_match.group(0).strip().upper()
    return "Desconhecido"

def get_system_data():
    """Obtém todas as informações do sistema: memória, disco, processador."""
    memory_info, total_memory, memory_speeds = get_memory_info()
    disk_info = get_disk_info()
    processor_info = get_processor_info()

    return {
        'Memória': memory_info,
        'Memória Total': total_memory,
        'Velocidades Memória': memory_speeds,
        'Disco': disk_info,
        'Processador': processor_info
    }

def query_api(serial_number):
    """Consulta a API usando o número de série fornecido."""
    api_url = f"http://avell.ramo.com.br:8089/?token=ZJBIx0ML8zf9xML5d4fjnRzZGToe538UDAep0q2yfYxSk9OE3togCd5IyjmsdlEh&query=ConsultaSerial({serial_number})"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Levantar uma exceção para erros HTTP
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao consultar a API: {e}")
        return []

def extract_processor_model(product_name):
    """Extrai o modelo do processador do nome do produto, tratando variações de maiúsculas e minúsculas."""
    # Converter nome do produto para minúsculas e remover espaços
    product_name = product_name.lower().replace(" ", "")
    # Buscar padrões de processador
    match = re.search(r'i\d{1,2}-\d{4,5}hx|i\d{1,2}-\d{4,5}h|i\d{1,2}', product_name, re.IGNORECASE)
    if match:
        return match.group(0).strip().upper()
    return "Desconhecido"

def compare_data(system_data, api_data):
    """Compara os dados do sistema com os dados da API SAP."""
    differences = []

    if not api_data:
        print("Dados da API não encontrados.")
        return ["Dados da API não encontrados."]

    api_product_info = api_data[0] if api_data else {}
    api_processor = extract_processor_model(api_product_info.get('NOMEPRODUTO', ''))
    api_memory = api_product_info.get('NOME_MEM', '')
    api_disk = api_product_info.get('NOME_SSD1', '')

    system_processor = system_data['Processador']
    system_memory_total = system_data['Memória Total']
    system_memory_speeds = system_data['Velocidades Memória']
    system_disk = re.search(r"Capacidade: (.+)", system_data['Disco']).group(1) if re.search(r"Capacidade: (.+)", system_data['Disco']) else "Desconhecido"

    if api_processor.lower() != system_processor.lower():
        differences.append(f"Processador difere: Sistema - {system_processor}, SAP - {api_processor}")
    else:
        differences.append(f"Processador compatível: Sistema - {system_processor}, SAP - {api_processor}")

    if api_memory.lower() != f"{system_memory_total} GB".lower():
        differences.append(f"Memória difere: Sistema - {system_memory_total} GB, SAP - {api_memory}")
    else:
        differences.append(f"Memória compatível: Sistema - {system_memory_total} GB, SAP - {api_memory}")

    api_memory_speed = re.search(r"\d+ MHz", api_memory)
    if api_memory_speed:
        api_memory_speed = api_memory_speed.group(0).replace(" MHz", "")
    for speed in system_data['Velocidades Memória']:
        if api_memory_speed and speed != api_memory_speed:
            differences.append(f"Velocidade da memória difere: Sistema - {speed} MHz, SAP - {api_memory_speed} MHz")
        else:
            differences.append(f"Velocidade da memória compatível: Sistema - {speed} MHz, SAP - {api_memory_speed} MHz")

    if api_disk.lower() != system_disk.lower():
        differences.append(f"Disco difere: Sistema - {system_disk}, SAP - {api_disk}")
    else:
        differences.append(f"Disco compatível: Sistema - {system_disk}, SAP - {api_disk}")

    return differences

def get_serial_number():
    """Obtém o número de série do sistema usando PowerShell."""
    command = "Get-WmiObject -Class Win32_BIOS | Select-Object -ExpandProperty SerialNumber"
    serial_number = run_powershell_command(command)
    if serial_number:
        return serial_number.strip()
    else:
        print("Não foi possível obter o número de série.")
        return None

def main():
    """Função principal para executar o script."""
    serial_number = get_serial_number()
    if serial_number:
        print(f"Número de série: {serial_number}")

        system_data = get_system_data()
        print("Informações do sistema obtidas com sucesso.")

        api_data = query_api(serial_number)
        print("Dados da API obtidos com sucesso.")

        differences = compare_data(system_data, api_data)
        print("Comparação de resultados:")
        for difference in differences:
            print(difference)
    else:
        print("O script não pode prosseguir sem o número de série.")

if __name__ == "__main__":
    main()
