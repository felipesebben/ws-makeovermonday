# Web Scraping | Makeovermonday 2024/wk06 Data

## Introduction ##
This repository aims to scrape data from a website using Python, Selenium, and other relevant libraries. The scraped data will then undergo quality controls using Pydantic, Pandas, and other data processing tools. The project also includes automated tests using pytest and taskipy to ensure the accuracy and reliability of the scraped data. 

Please refer to the documentation and code in this repository for more details on the implementation and usage.
This repository aims to scrape data from a website and perform quality controls on it.

## Instructions ##
1. Clone the repository:
```bash
git clone https://github.com/felipesebben/ws-makeovermonday.git
cd ws-makeovermonday

```
2. Configure the right python version with `pyenv`:
```bash
pyenv install 3.11.3
pyenv local 3.11.3
```
3. Install the project dependencies:
```bash
poetry install
```
4. Activate the virtual environment:
```bash
poetry shell
```
5. Execute the tests to make sure that everything is working as expected:
```bash
task test
```
6. Execute the command to see the project documentation:
```bash
task doc
```
7. Execute the command to peform the ETL:
```bash
task run
```
8. Check in the data/output folder if the file has been correctly generated.

## Contato
In case of any doubts, questions, or suggestions:

Felipe Sebben - felipesebben@yahoo.com.br / sebbencomdoisb@gmail.com
