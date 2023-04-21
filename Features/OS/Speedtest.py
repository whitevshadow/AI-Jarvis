import speedtest
from Body.Speaker import Speak


def Speed_test():
    try:
        test = speedtest.Speedtest()
        Speak("Loading Servers....")
        test.get_best_server()
        best = test.get_best_server()
        Speak(f"Found: {best['host']} located in {best['country']}. It would take few second for result !!")
        download_result = test.download()
        upload_result = test.upload()
        ping_result = test.results.ping
        Speed_Result = f'''Sir , Here are the following result for Speed Test.
                      Download speed is {download_result / 1024 / 1024 :.2f} Mb per second.
                      Upload speed is {upload_result / 1024 / 1024 :.2f} Mb per second.
                      Sir and the ping is {ping_result:.2f} ms.'''

        return Speed_Result

    except speedtest.ConfigRetrievalError or speedtest.SpeedtestException:
        Speed_test_error = "Sir there is a problem with your Internet Connection"
        return Speed_test_error


