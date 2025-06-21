# Telegram E-commerce Analytics
This project focuses on fine-tuning  LLM’s for Amharic Named Entity Recognition (NER) system that extracts key business entities such as product names, prices, and Locations, from text, images, and documents shared across these Telegram channels. 
The extracted data will be used to populate EthioMart's centralised database, making it a comprehensive e-commerce hub.

This repository contains scripts for analyzing e-commerce data from Telegram channels.

## Features

- Data extraction from Telegram channels
- Data cleaning and preprocessing
- Analytics and visualization scripts

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Teddy-GH/Telegram-e-commerce-analytics.git
    ```
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure your Telegram API credentials** in `config.py`.

## Usage

Run the main script:
```bash
python main.py
```

## Folder Structure

- `data/` - Raw and processed data
- `scripts/` - Analysis scripts
- `notebooks/` - Jupyter notebooks for exploration

## Contributing

Pull requests are welcome. For major changes, open an issue first.

## License

This project is licensed under the MIT License.