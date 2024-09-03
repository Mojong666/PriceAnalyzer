import os
import csv
import html


class PriceAnalyzer:
    def __init__(self, directory):
        self.directory = directory
        self.products = []

    def load_prices(self):
        for filename in os.listdir(self.directory):
            if "price" in filename.lower():
                self._process_file(os.path.join(self.directory, filename))

    def _process_file(self, filepath):
        try:
            with open(filepath, mode='r', encoding='utf-8', errors='replace') as file:
                reader = csv.reader(file, delimiter=self._detect_delimiter(file))
                headers = self._normalize_headers(next(reader))

                name_idx = self._get_index(headers, ['название', 'продукт', 'товар', 'наименование'])
                price_idx = self._get_index(headers, ['цена', 'розница'])
                weight_idx = self._get_index(headers, ['фасовка', 'масса', 'вес'])

                for row in reader:
                    try:
                        name = row[name_idx].strip()
                        price = float(row[price_idx].strip().replace(',', '.'))
                        weight = float(row[weight_idx].strip().replace(',', '.'))
                        price_per_kg = price / weight if weight != 0 else 0
                        self.products.append({
                            "name": name,
                            "price": price,
                            "weight": weight,
                            "file": os.path.basename(filepath),
                            "price_per_kg": price_per_kg
                        })
                    except (ValueError, IndexError) as e:
                        print(f"Ошибка при обработке строки в файле {filepath}: {e}")

        except FileNotFoundError:
            print(f"Файл не найден: {filepath}")
        except UnicodeDecodeError:
            print(f"Ошибка кодировки при чтении файла: {filepath}")

    def _detect_delimiter(self, file):
        sample_line = file.readline()
        file.seek(0)  # Возвращаемся в начало файла
        if ',' in sample_line:
            return ','
        elif ';' in sample_line:
            return ';'
        else:
            return ','  # Или выбросить исключение, если разделитель неизвестен

    def _normalize_headers(self, headers):
        headers = headers[0].split(',') if len(headers) == 1 else headers
        return [header.strip().lower() for header in headers]

    def _get_index(self, headers, possible_names):
        for name in possible_names:
            if name in headers:
                return headers.index(name)
        print(f"Не удалось найти необходимые столбцы. Заголовки: {headers}")
        return None

    def find_text(self, text):
        text = text.lower()
        result = [product for product in self.products if text in product['name'].lower()]
        result.sort(key=lambda x: x['price_per_kg'])
        return result

    def export_to_html(self, data, filename='output.html'):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('<table border="1">\n')
            file.write(
                '<tr><th>№</th><th>Наименование</th><th>Цена</th><th>Вес</th><th>Файл</th><th>Цена за кг</th></tr>\n')
            for i, product in enumerate(data, 1):
                file.write(f"<tr><td>{i}</td><td>{html.escape(product['name'])}</td><td>{product['price']}</td>"
                           f"<td>{product['weight']}</td><td>{product['file']}</td><td>{product['price_per_kg']:.2f}</td></tr>\n")
            file.write('</table>\n')


def main():
    analyzer = PriceAnalyzer(directory="Укажите путь к файлам CSV")
    analyzer.load_prices()

    while True:
        query = input("Введите название товара для поиска (или 'exit' для выхода): ")
        if query.lower() == 'exit':
            print("Работа завершена.")
            break
        results = analyzer.find_text(query)
        if results:
            for i, product in enumerate(results, 1):
                print(
                    f"{i:2}. {product['name']:<40} {product['price']:>7} {product['weight']:>5} {product['file']} {product['price_per_kg']:>7.2f}")
            analyzer.export_to_html(results)
            print("Результаты экспортированы в файл 'output.html'.")
        else:
            print("Товары не найдены.")


if __name__ == "__main__":
    main()
