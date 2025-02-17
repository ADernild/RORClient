# RORClient

🚀 **A Python client for interacting with the ROR API.**
RORClient provides a simple, efficient way to query the [Research Organization Registry (ROR)](https://ror.org) API using **HTTPX** and **Pydantic**.

---

## 📖 Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Synchronous Client](#synchronous-client)
- [Asynchronous Client](#asynchronous-client)
- [Models](#models)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## ⚡ Installation
> ⚠ **Work in Progress**: RORClient is not yet available via PyPI.
> Clone the repository and install dependencies manually:

```sh
git clone https://github.com/ADernild/rorclient.git
cd rorclient
pip install -r requirements.txt
```
---

## 🚀 Quick Start

### Synchronous Client
```python
from rorclient import RORClient

client = RORClient()

# get institution details
org = client.get_institution("03yrm5c26")
if org:
    print(f"Found institution: {org.name}")

multiple_orgs = client.get_multiple_institutions(["03yrm5c26", "029z82x56"])
print(f"Fetched {len(multiple_orgs)} institutions")
```

### Asynchronous Client
```python
import asyncio
from rorclient import AsyncRORClient

async def main():
    client = AsyncRORClient()

    # Get institution details
    org = await client.get_institution("03yrm5c26")
    if org:
        print(f"Found institution: {org.name}")

    # Fetch multiple institutions
    multiple_orgs = await client.get_multiple_institutions(["03yrm5c26", "029z82x56"])
    print(f"Fetched {len(multiple_orgs)} institutions")

    await client.close()  # Ensure the client session is closed

asyncio.run(main())
```

---

## 🏛 Models
RORClient uses **Pydantic** models to structure API responses. The main model is `Institution`, which represents an organization in ROR.

Example usage:

```python
from rorclient import RORClient

client = RORClient()
org = client.get_institution("03yrm5c26")

if org:
    print(org.name)  # Stanford University
    print(org.external_ids)  # External identifiers like GRID, ISNI
    print(org.location.country)  # Country of the institution
```

For a full list of available fields, see the [models.py](rorclient/models/institution.py) file.
You can also have a look at the [ROR API documentation](https://ror.readme.io/v2/docs/data-structure)

---

## 🧪 Testing

To run the test suite, run:

```sh
python -m unittest discover
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
