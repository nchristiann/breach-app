from plyer import notification
import os
import platform

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='My App',
        timeout=10
    )
    
    # Additional code to send notification using PowerShell on Windows
    if platform.system() == "Windows":
        powershell_command = f'''
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
        $template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02
        $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template)
        $textNodes = $xml.GetElementsByTagName("text")
        $textNodes.Item(0).AppendChild($xml.CreateTextNode("{title}")) > $null
        $textNodes.Item(1).AppendChild($xml.CreateTextNode("{message}")) > $null
        $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
        $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("My App")
        $notifier.Show($toast)
        '''
        os.system(f'powershell -Command "{powershell_command}"')

# Exemplu de utilizare
if __name__ == "__main__":
    send_notification("Test Title", "This is a test notification")