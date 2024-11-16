import subprocess
import platform
import os

class NotificationSystem:
    def __init__(self):
        # Verificăm dacă rulăm în WSL
        self.is_wsl = 'microsoft-standard' in platform.uname().release.lower()
        
    def _send_windows_notification(self, title, message):
        """Trimite notificare în Windows folosind PowerShell."""
        # Folosim BurntToast pentru notificări Windows
        powershell_script = f'''
        $Title = "{title}"
        $Message = "{message}"
        
        $ErrorActionPreference = 'Stop'
        
        function Show-Notification {{
            param (
                [string]$Title,
                [string]$Message
            )
            
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
            [Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
            [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null

            $APP_ID = "Aplicatie"

            $template = @"
<toast>
    <visual>
        <binding template="ToastText02">
            <text id="1">$Title</text>
            <text id="2">$Message</text>
        </binding>
    </visual>
</toast>
"@

            $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
            $xml.LoadXml($template)
            $toast = New-Object Windows.UI.Notifications.ToastNotification($xml)
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($APP_ID).Show($toast)
        }}

        Show-Notification -Title $Title -Message $Message
        '''
        
        try:
            # Rulăm comanda PowerShell cu argumente corecte
            result = subprocess.run(
                ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-NoProfile', '-Command', powershell_script],
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stderr:
                print(f"PowerShell warning/error: {result.stderr}")
                
            return True
        except subprocess.CalledProcessError as e:
            print(f"Eroare PowerShell: {e.stderr}")
            return False
        except Exception as e:
            print(f"Eroare la trimiterea notificării Windows: {str(e)}")
            return False

    def _check_notify_send(self):
        """Verifică dacă notify-send este instalat și încearcă să-l instaleze dacă lipsește."""
        try:
            subprocess.run(['which', 'notify-send'], capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            print("notify-send nu este instalat. Încercăm să-l instalăm...")
            try:
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'libnotify-bin'], check=True)
                return True
            except subprocess.CalledProcessError as e:
                print(f"Nu s-a putut instala notify-send: {str(e)}")
                return False

    def _send_linux_notification(self, title, message):
        """Trimite notificare în Linux folosind notify-send."""
        if not self._check_notify_send():
            return False
            
        try:
            notify_send_path = subprocess.check_output(['which', 'notify-send']).decode().strip()
            subprocess.run([notify_send_path, title, message], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Eroare la trimiterea notificării Linux: {str(e)}")
            return False
        except Exception as e:
            print(f"Eroare neașteptată la trimiterea notificării Linux: {str(e)}")
            return False

    def send_notification(self, title, message, windows=True, linux=True):
        """
        Trimite notificări pe ambele sisteme de operare.
        
        Args:
            title (str): Titlul notificării
            message (str): Conținutul notificării
            windows (bool): Dacă să trimită notificare și pe Windows
            linux (bool): Dacă să trimită notificare și pe Linux
        """
        success = True
        
        if self.is_wsl and windows:
            success &= self._send_windows_notification(title, message)
            
        if linux:
            success &= self._send_linux_notification(title, message)
            
        return success

if __name__ == "__main__":
    notifier = NotificationSystem()
    print("Testăm sistemul de notificări...")
    
    test_message = "Aceasta este o notificare de test!"
    
    # Test pentru ambele sisteme
    notifier.send_notification(
        "Test Notificare", 
        test_message,
        windows=True,
        linux=True
    )