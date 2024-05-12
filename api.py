import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
LANG = "ru"
APP_ID = "79d1ca96933b0328e1c7e3e7a26cb347"


class Response:
    def __init__(self, temp, temp_feels, temp_min, temp_max, description):
        self.temp = temp
        self.temp_min = temp_min
        self.temp_feels = temp_feels
        self.temp_max = temp_max
        self.description = description


def get_weather_by_city(name_city) -> Response:
    url = f"{BASE_URL}?q={name_city}&units=metric&lang={LANG}&appid={APP_ID}"
    response = requests.get(url).json()

    return Response(
        temp=response["main"]["temp"],
        temp_min=response["main"]["temp_min"],
        temp_max=response["main"]["temp_max"],
        temp_feels=response["main"]["feels_like"],
        description=[resp["description"] for resp in response["weather"]]
    )


if __name__ == "__main__":
    city = input("Введите название города -> ")
    resp = get_weather_by_city(city)

    print(f"Погода в городе {city}")
    print(f"Температура {resp.temp}°C")
    print(f"Ощущается как {resp.temp_feels}°C")
    print(f"Описание: {', '.join(resp.description)}")
