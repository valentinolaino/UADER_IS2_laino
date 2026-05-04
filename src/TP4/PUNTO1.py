import subprocess
import platform

class Ping:
    def __init__(self):
        self._is_windows = platform.system().lower() == "windows"

    def execute(self, ip: str):
        # Control para solo permitir IPs que comiencen con "192."
        if not ip.startswith("192."):
            raise ValueError("IP no permitida")
        return self._ping(ip)

    def executefree(self, ip: str):
        # A diferencia de la anterior, esta no tiene control
        return self._ping(ip)

    def _ping(self, target: str):
        try:
            # Cambia la flag dependiendo del SO
            count_flag = "-n" if self._is_windows else "-c"

            result = subprocess.run(
                ["ping", count_flag, "10", target],
                capture_output=True,
                text=True
            )

            return result.stdout

        except Exception as e:
            return str(e)

class PingProxy:
    def __init__(self):
        self._ping = Ping()

    def execute(self, ip: str):
        if ip == "192.168.0.254":
            # Redirección especial
            return self._ping.executefree("www.google.com")
        else:
            return self._ping.execute(ip)

if __name__ == "__main__":
    proxy = PingProxy()

    print(proxy.execute("192.168.0.1"))      # OK
    print(proxy.execute("192.168.0.254"))    # redirige a Google
    print(proxy.execute("8.8.8.8"))          # error