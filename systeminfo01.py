import subprocess
import re


def run_powershell_command(command):
    """Run a PowerShell command and return the output."""
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    return result.stdout.strip()

def format_disk_capacity(sizeGB):
    """Format the disk capacity to specified categories."""
    if sizeGB < 256:
        return "256GB"
    elif sizeGB < 500:
        return "512GB"
    elif sizeGB < 1000:
        return "1TB"
    elif sizeGB < 2000:
        return "2TB"
    elif sizeGB < 4000:
        return "4TB"
    else:
        return "4TB"

def get_memory_info():
    """Get memory information including serial number."""
    command = """
    Get-WmiObject Win32_PhysicalMemory | ForEach-Object {
        $capacityGB = [math]::round($_.Capacity / 1GB, 2)
        Write-Output "BankLabel: $($_.BankLabel)"
        Write-Output "Capacity: $capacityGB GB"
        Write-Output "Speed: $($_.Speed) MHz"
        Write-Output "Manufacturer: $($_.Manufacturer)"
        Write-Output "Serial Number: $($_.SerialNumber)"
        Write-Output "`n"
    }
    """
    return run_powershell_command(command)

def get_disk_info():
    """Get disk storage information including serial number."""
    command = """
    Get-WmiObject Win32_DiskDrive | ForEach-Object {
        $sizeGB = [math]::round($_.Size / 1GB, 2)
        Write-Output "Model: $($_.Model)"
        Write-Output "Interface: $($_.InterfaceType)"
        Write-Output "Capacity: $sizeGB GB"
        Write-Output "Partitions: $($_.Partitions)"
        Write-Output "Serial Number: $($_.SerialNumber)"
        Write-Output "`n"
    }
    """
    output = run_powershell_command(command)
    lines = output.splitlines()
    formatted_lines = []
    for line in lines:
        if line.startswith("Capacity:"):
            try:
                # Extract the numeric part of the capacity
                sizeGB = float(re.search(r"(\d+(\.\d+)?)", line).group())
                formatted_lines.append(f"Capacity: {format_disk_capacity(sizeGB)}")
            except (ValueError, AttributeError):
                # Handle cases where conversion fails
                formatted_lines.append(line)
        else:
            formatted_lines.append(line)
    return "\n".join(formatted_lines)

def get_processor_info():
    """Get processor information including serial number."""
    command = """
    Get-WmiObject Win32_Processor | ForEach-Object {
        Write-Output "Name: $($_.Name)"
        Write-Output "Number of Cores: $($_.NumberOfCores)"
        Write-Output "Clock Speed: $($_.MaxClockSpeed) MHz"
        Write-Output "Architecture: $($_.Architecture)"
        Write-Output "Serial Number: $($_.ProcessorId)"
        Write-Output "`n"
    }
    """
    return run_powershell_command(command)

def get_system_info():
    """Get all system information: memory, disk, processor."""
    memory_info = get_memory_info()
    disk_info = get_disk_info()
    processor_info = get_processor_info()

    return f"Memory Information:\n{memory_info}\n\nDisk Information:\n{disk_info}\n\nProcessor Information:\n{processor_info}"

if __name__ == "__main__":
    system_info = get_system_info()
    print(system_info)
