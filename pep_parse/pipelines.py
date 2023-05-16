import datetime as dt
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:

    statuses = {}

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item['status'] not in self.statuses.keys():
            self.statuses[item['status']] = 1
        else:
            self.statuses[item['status']] += 1
        res_dir = BASE_DIR / 'results'
        res_dir.mkdir(exist_ok=True)
        time = dt.datetime.now()
        time = time.strftime('%Y-%m-%d_%H-%M')
        filename = res_dir / f'status_summary_{time}.csv'
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for key, value in self.statuses.items():
                f.write(f'{key},{value}\n')
            f.write(f'Total,{sum(self.statuses.values())}\n')
        return item

    def close_spider(self, spider):
        pass
