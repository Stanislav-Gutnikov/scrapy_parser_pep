import datetime as dt
import csv
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:

    statuses = {}

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.statuses[item['status']] = self.statuses.get(
            item['status'], 0
        ) + 1
        res_dir = BASE_DIR / 'results'
        res_dir.mkdir(exist_ok=True)
        time = dt.datetime.now()
        time = time.strftime('%Y-%m-%d_%H-%M')
        filename = res_dir / f'status_summary_{time}.csv'
        with open(filename, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(
                (
                    ('Статус', 'Количество'),
                    *self.statuses.items(),
                    ('Total', sum(self.statuses.values()))
                )
            )
        return item

    def close_spider(self, spider):
        pass
