import requests

from core.config import config


class HCAIBrain:
    def __init__(self):
        if not config.HCAI_API_KEY:
            raise ValueError("HCAI_API_KEY is missing. Add it to your .env file.")

        self.api_key = config.HCAI_API_KEY
        self.model = config.HCAI_MODEL
        self.url = f"{config.HCAI_BASE_URL}/chat/completions"
        self.session = requests.Session()

    def ask(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt,}],
            "stream": False,
        }

        try:
            response = self.session.post(self.url,headers=headers,json=payload,timeout=120,)
            response.raise_for_status()
            data = response.json() 
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            return "HCAI request timed out."

        except requests.exceptions.HTTPError as e:
            return (f"HCAI HTTP error: {e.response.status_code}\n {e.response.text}")

        except requests.exceptions.RequestException as e:
            return f"HCAI connection error: {e}"

        except (KeyError, IndexError, TypeError) as e:
            return f"Unexpected HCAI response: {e}"